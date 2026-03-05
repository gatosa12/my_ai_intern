# AI Sales Intern (Ava) – Sussex Staffing Solutions + Roofing AI

An autonomous voice agent that scrapes healthcare/roofing leads, makes outbound calls, qualifies prospects, books meetings, and logs everything to a dashboard.

**Adapted for:**
- **Sussex Staffing Solutions** (care home outbound calling)
- **Roofing companies** (inbound missed calls + outbound lead gen)

---

## What It Does

This tool creates an AI-powered sales assistant that:

1. **Scrapes leads** from CQC (care homes) or Google Maps (homeowners needing roofing)
2. **Makes real phone calls** using natural-sounding AI voice (ElevenLabs + Twilio)
3. **Handles live conversations** with GPT-4 intelligence
4. **Books meetings** and logs outcomes to a dashboard
5. **Never misses a call** (24/7 availability)

---

## Real-World Results

In the original real estate test:
- **38 outbound calls** made
- **11 live conversations** held
- **4 meetings booked** ($149 each)
- **$596 revenue**, $578 profit
- **$18 total API cost**
- **10.5% conversion rate** (3x industry average)
- **TCPA compliant** with full disclosure

---

## Quick Start (Sussex Staffing Solutions)

### Step 1: Clone the Repository

```bash
git clone https://github.com/gatosa12/my_ai_intern.git
cd my_ai_intern
```

### Step 2: Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd ../frontend
npm install
```

### Step 3: Set Up Environment Variables

Create `backend/.env`:

```env
# Twilio (for making/receiving calls)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+441234567890

# ElevenLabs (natural voice TTS)
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_AGENT_ID=your_agent_id

# OpenAI GPT-4 (conversation AI)
LLM_API_KEY=your_openai_key

# Bright Data (scraping - optional)
BRIGHTDATA_API_TOKEN=your_token
BRIGHTDATA_WEB_UNLOCKER_ZONE=your_zone

# Database
DB_TYPE=sqlite
DATABASE_URL=sqlite:///leads.db
```

### Step 4: Run the Application

**Backend:**
```bash
cd backend
python app.py
```

**Frontend:**
```bash
cd frontend
npm start
```

Dashboard opens at `http://localhost:3000`

---

## How to Use

### For Sussex Staffing Solutions (Care Home Outbound):

1. **Scrape Care Homes:**
   - Click "Scrape New Leads" in dashboard
   - Set location: "Sussex, UK"
   - Set mode: "sussex_staffing"
   - Limit: 30 leads

2. **Review & Filter:**
   - Dashboard shows all scraped care homes
   - Filter by priority (HIGH = nursing homes, MEDIUM = residential)
   - Sort by location

3. **Make Calls:**
   - Select leads to call (start with 10-20)
   - Click "Call Selected"
   - Ava calls each home, asks for the manager, qualifies needs
   - Books callbacks with Hafid if interested

4. **Review Results:**
   - Check "Call Logs" tab for full transcripts
   - Booked meetings appear in your calendar
   - Export data to CRM (HubSpot, Pipedrive, etc.)

### For Roofing Companies (Inbound + Outbound):

**Inbound Mode (Never Miss a Call):**
- Route your business number through Twilio
- Ava answers every call 24/7
- Qualifies: name, address, issue type, urgency
- Books site visit or callback

**Outbound Mode (Lead Gen):**
- Scrape homeowners in storm-hit areas
- Ava calls offering free roof inspections
- Books appointments directly

---

## System Prompts

### Sussex Staffing (Care Home Outreach)

Ava's script:
1. "Hi, could I speak with the Home Manager please?"
2. Qualifies: current agencies used, hardest roles to fill, notice period
3. Books callback with Hafid
4. Sends confirmation text

### Roofing Inbound (Missed Call Handler)

Ava's script:
1. "Thanks for calling [Company]. I'm Ava, the virtual assistant."
2. Qualifies: name, address, issue, urgency
3. Books callback within 2 hours
4. Sends confirmation

### Roofing Outbound (Free Inspection Offer)

Ava's script:
1. "Hi [name], I'm calling from [Company], a local roofing company."
2. Offers free roof health check
3. Books site visit if interested
4. Sends follow-up text if not

---

## API Costs at Scale

| Volume | API Cost | Expected Bookings |
|---|---|---|
| 38 calls | ~£15 | 4 meetings |
| 100 calls/week | ~£40 | 10-11 meetings |
| 300 calls/week | ~£120 | 30+ meetings |

---

## UK Compliance (Critical)

- ✅ Pre-screen all numbers against [TPS](https://www.tpsonline.org.uk/)
- ✅ Ava discloses it's an AI assistant if asked
- ✅ Every call logged with full transcript
- ✅ Opt-outs actioned immediately
- ✅ ICO registration for data processing
- ✅ GDPR-compliant data storage

---

## Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** React
- **Voice:** ElevenLabs (TTS) + Twilio (calls)
- **AI:** OpenAI GPT-4
- **Scraping:** Bright Data MCP
- **Database:** SQLite (or PostgreSQL)

---

## File Structure

```
my_ai_intern/
├── backend/
│   ├── app.py              # Flask API
│   ├── voice.py            # System prompts + call logic
│   ├── scraper.py          # CQC/Google Maps scraping
│   ├── models.py           # SQLite schema
│   ├── config.py           # Config management
│   ├── requirements.txt    # Python dependencies
│   └── .env                # API keys (create this)
├── frontend/
│   ├── src/                # React components
│   └── package.json        # Node dependencies
└── README.md           # This file
```

---

## Next Steps

1. **Get API Keys:**
   - [Twilio](https://www.twilio.com/)
   - [ElevenLabs](https://elevenlabs.io/)
   - [OpenAI](https://platform.openai.com/)
   - [Bright Data](https://brightdata.com/) (optional)

2. **Test in Dummy Mode:**
   - Run without API keys to see the dashboard
   - Uses dummy data for leads
   - No actual calls made

3. **Run 10 Test Calls:**
   - Add API keys
   - Scrape 10 leads
   - Make real calls to test numbers
   - Review transcripts

4. **Scale to 100+ Calls/Week:**
   - Refine scripts based on feedback
   - Monitor conversion rates
   - Integrate with your CRM

---

## Troubleshooting

**"No leads scraped"**
- Check Bright Data API token
- If missing, dummy data is used automatically

**"Calls not connecting"**
- Verify Twilio credentials
- Check phone number format (+44...)

**"Voice sounds robotic"**
- Update ElevenLabs agent ID
- Try different voices in ElevenLabs dashboard

**"Transcripts missing"**
- Check OpenAI API key
- Verify quota not exceeded

---

## Support

For questions or custom implementations:
- GitHub Issues: [github.com/gatosa12/my_ai_intern/issues](https://github.com/gatosa12/my_ai_intern/issues)
- Original by: [Siraj Raval](https://github.com/llSourcell)

---

## License

MIT License - Free to use and modify.
