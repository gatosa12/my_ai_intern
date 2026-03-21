import os
import requests
from twilio.rest import Client
import openai
from retell import Retell

# ── ENV VARS ──────────────────────────────────────────────────────────────────
twilio_sid        = os.getenv('TWILIO_ACCOUNT_SID')
twilio_token      = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number     = os.getenv('TWILIO_PHONE_NUMBER')
elevenlabs_api_key   = os.getenv('ELEVENLABS_API_KEY')
elevenlabs_agent_id  = os.getenv('ELEVENLABS_AGENT_ID')
llm_api_key          = os.getenv('LLM_API_KEY')

retellai_api_key      = os.getenv('RETELLAI_API_KEY')
retellai_phone_number = os.getenv('RETELLAI_PHONE_NUMBER')
AGENT_IDS = {
    'sussex_staffing':  os.getenv('RETELLAI_SUSSEX_AGENT_ID'),
    'roofing_outbound': os.getenv('RETELLAI_ROOFING_AGENT_ID'),
    'roofing_inbound':  os.getenv('RETELLAI_ROOFING_AGENT_ID'),
}

# ── SYSTEM PROMPTS ────────────────────────────────────────────────────────────

# Prompt A – Sussex Staffing Solutions (outbound to care homes)
SUSSEX_STAFFING_SYSTEM_PROMPT = """
You are Ava, a professional AI assistant calling on behalf of
Sussex Staffing Solutions, a healthcare staffing agency based in Sussex, UK.
Your goal is to qualify care homes and book a callback with the director Hafid.

CALL FLOW:

1. OPENING:
   "Hi, could I speak with the Home Manager please?
    ...Hi, my name is Ava. I'm calling on behalf of Sussex Staffing Solutions,
    a local nursing and care staffing agency in Sussex.
    I'll only take a minute of your time — is that okay?"

2. QUALIFY (ask one question at a time, naturally):
   - "Do you currently use any staffing agencies for cover?"
   - "Which roles do you find hardest to fill at short notice — nurses or carers?"
   - "How much notice do you typically have when you need cover?"
   - "Are you open to a brief call with our director Hafid to see if we could help?"

3. BOOK:
   "Brilliant. I'll pass your details to Hafid now.
    He'll call you within 24 hours.
    What's the best number and time to reach you on?"

4. CLOSE:
   "Thank you so much for your time.
    You'll receive a confirmation text shortly. Have a wonderful day."

5. IF NOT INTERESTED:
   "No problem at all — completely understand.
    Could I send a short text with our details just in case?"

COMPLIANCE RULES:
- Always identify as an AI assistant if directly asked.
- State this call may be recorded for quality purposes.
- Respect opt-outs immediately and log them as DNC.
- Do not call numbers registered on TPS.
"""

# Prompt B – Roofing Company (inbound missed calls / overflow)
ROOFING_INBOUND_SYSTEM_PROMPT = """
You are Ava, the AI assistant for {company_name}, a local roofing company.
Your job is to answer inbound calls, qualify leads, and book site visits
or callbacks so the company never misses a job.

CALL FLOW:

1. GREETING:
   "Hi there! Thanks for calling {company_name}.
    My name is Ava, the virtual assistant.
    You've reached us outside of normal hours but don't worry —
    I can help you right now. Is that okay?"

2. QUALIFY (one question at a time):
   - "Could I get your name?"
   - "What's the address of the property?"
   - "Can you describe the issue — is it a leak, storm damage,
     missing tiles, or something else?"
   - "How urgent is it — do you need someone out this week,
     or is it more of a planned job?"
   - "Have you had any other quotes yet, or are we your first call?"

3. BOOK:
   "Great, thank you {lead_name}.
    I'm going to pass all of this straight to the team and have someone
    call you back within 2 hours during business hours.
    What's the best number to reach you on?"

4. CLOSE:
   "Perfect. You're all booked in.
    You'll receive a confirmation text shortly.
    Is there anything else I can help with?"

5. IF they ask about pricing:
   "I don't want to give you a number without someone seeing the job first —
    but the team does free no-obligation quotes.
    That's one of the reasons people love using {company_name}."

RULES:
- If asked directly whether you are AI: say
  'I'm a virtual assistant — the human team will call you back shortly.'
- Stay warm, friendly, and concise. Never ramble.
- Always confirm: name, address, issue type, urgency, callback number.
- Log all details at the end of every call.
"""

# Prompt C – Roofing Company (outbound lead gen / free inspection offer)
ROOFING_OUTBOUND_SYSTEM_PROMPT = """
You are Ava, calling homeowners on behalf of {company_name},
a local roofing company.

OPENING:
"Hi, is that {lead_name}?
 Hi {lead_name}, my name is Ava — I'm calling from {company_name},
 a local roofing company in your area.
 I'll only take 30 seconds of your time, I promise.
 We've been doing a number of roofing jobs nearby recently and we're
 offering free roof health checks this month —
 no obligation, no sales pressure, just a quick visual inspection
 while we're already in the area.
 Would that be something you'd be interested in?"

IF YES:
"Brilliant! Can I grab a good day and time for one of the team
 to swing by? We're flexible — mornings, afternoons, even Saturdays."

IF NO / NOT INTERESTED:
"No problem at all — I completely understand.
 Would it be okay if I send you a text with our details
 just in case you ever need us in future?"

LOG: name, address, outcome (booked / follow-up text / not interested),
callback number, preferred time slot.
"""


# ── LLM HELPER ────────────────────────────────────────────────────────────────

def get_llm_response(prompt, system_prompt=None, mode='sussex_staffing',
                    company_name='Sussex Staffing Solutions', lead_name='there'):
    """
    Generate a conversational AI response.
    mode options:
      'sussex_staffing'    – care home outbound
      'roofing_inbound'    – roofing missed call handler
      'roofing_outbound'   – roofing lead gen outbound
    """
    if system_prompt is None:
        if mode == 'roofing_inbound':
            system_prompt = ROOFING_INBOUND_SYSTEM_PROMPT.format(
                company_name=company_name, lead_name=lead_name)
        elif mode == 'roofing_outbound':
            system_prompt = ROOFING_OUTBOUND_SYSTEM_PROMPT.format(
                company_name=company_name, lead_name=lead_name)
        else:
            system_prompt = SUSSEX_STAFFING_SYSTEM_PROMPT

    openai.api_key = llm_api_key
    resp = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user',   'content': prompt}
        ]
    )
    return resp['choices'][0]['message']['content']


# ── ELEVENLABS TTS ────────────────────────────────────────────────────────────

def elevenlabs_tts(text):
    """Convert text to speech via ElevenLabs and return the audio URL."""
    url = f'https://api.elevenlabs.io/v1/agents/{elevenlabs_agent_id}/generate'
    headers = {
        'xi-api-key': elevenlabs_api_key,
        'Content-Type': 'application/json'
    }
    data = {'text': text}
    r = requests.post(url, headers=headers, json=data)
    if r.ok:
        return r.json().get('audio_url')
    return None


# ── RETELL CALL PLACER ────────────────────────────────────────────────────────

def retell_place_call(to_number, mode='sussex_staffing', dynamic_variables=None):
    """
    Place an outbound AI voice call via Retell AI.

    mode: 'sussex_staffing' | 'roofing_outbound' | 'roofing_inbound'
    dynamic_variables: dict of variables injected into the LLM prompt
                       e.g. {'lead_name': 'John', 'company_name': 'ABC Roofing'}
    Returns the Retell call_id.
    """
    agent_id = AGENT_IDS.get(mode)
    if not agent_id:
        raise ValueError(f"No Retell agent configured for mode '{mode}'")
    if not retellai_phone_number:
        raise ValueError("RETELLAI_PHONE_NUMBER not set")

    client = Retell(api_key=retellai_api_key)
    call = client.call.create_phone_call(
        from_number=retellai_phone_number,
        to_number=to_number,
        override_agent_id=agent_id,
        retell_llm_dynamic_variables=dynamic_variables or {},
        metadata={'mode': mode},
    )
    return call.call_id


# ── TWILIO/ELEVENLABS CALL PLACER (legacy) ────────────────────────────────────

def place_call(to_number, script):
    """
    Place an outbound call via Twilio.
    Converts the script to speech with ElevenLabs then plays it.
    """
    client = Client(twilio_sid, twilio_token)
    audio_url = elevenlabs_tts(script)
    if not audio_url:
        raise Exception('Failed to generate TTS audio from ElevenLabs')
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url=audio_url
    )
    return call.sid


def build_opening_script(lead, mode='sussex_staffing', company_name='Sussex Staffing Solutions'):
    """
    Build the initial spoken script for a call based on lead data and mode.
    """
    lead_name = lead.get('name', '').split()[0] if lead.get('name') else 'there'

    if mode == 'sussex_staffing':
        home_type = lead.get('category', 'care home')
        return (
            f"Hi, could I speak with the Home Manager please? "
            f"Hi, my name is Ava, I'm calling on behalf of Sussex Staffing Solutions, "
            f"a local nursing and care staffing agency in Sussex. "
            f"I understand you manage a {home_type} and I'd love to see if we can support "
            f"you with staffing. I'll only take a minute — is that okay?"
        )
    elif mode == 'roofing_outbound':
        return (
            f"Hi, is that {lead_name}? "
            f"Hi {lead_name}, my name is Ava — I'm calling from {company_name}, "
            f"a local roofing company in your area. "
            f"I'll only take 30 seconds of your time, I promise. "
            f"We're offering free roof health checks this month — "
            f"no obligation, no sales pressure. "
            f"Would that be something you'd be interested in?"
        )
    else:  # roofing_inbound
        return (
            f"Hi there! Thanks for calling {company_name}. "
            f"My name is Ava, the virtual assistant. "
            f"You've reached us outside of normal hours but don't worry — "
            f"I can help you right now. Is that okay?"
        )
