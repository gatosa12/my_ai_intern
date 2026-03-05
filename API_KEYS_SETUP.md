# API Keys Setup Guide

This file contains all the API keys and credentials you've collected for your AI Sales Intern project.

## 🔑 Environment Variables

Create a `.env` file in the root directory of your project and add these credentials:

```bash
# OpenAI API Key
OPENAI_API_KEY=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

# ElevenLabs API Key
ELEVENLABS_API_KEY=sk_4f21be9bb58c37b5285d1d4d0ccc9f92c9d02d5bec4fadb1

# Twilio Credentials
TWILIO_ACCOUNT_SID=AC6b3e8cd7c5dd0dc51b19afe73b90b654
TWILIO_AUTH_TOKEN=10f8e39ec00acfe99f0b1c9aa3b2e1dd
TWILIO_PHONE_NUMBER=+18886584970

# Bright Data API Key
BRIGHT_DATA_API_KEY=9dab0c11-95b2-40c3-82b5-9a28d2749103
BRIGHT_DATA_ZONE=unblocker
```

## 📋 API Key Details

### 1. OpenAI
- **Service**: GPT-4 API for conversation intelligence
- **Key Name**: AI Sales Intern Final
- **Dashboard**: https://platform.openai.com/api-keys
- **Usage**: Powers the AI conversation logic and lead qualification

### 2. ElevenLabs
- **Service**: Text-to-Speech voice synthesis
- **Key Name**: dad people
- **Dashboard**: https://elevenlabs.io/app/developers/api-keys
- **Usage**: Generates natural-sounding voice for phone calls

### 3. Twilio
- **Service**: Phone number provisioning and call handling
- **Phone Number**: +1 (888) 658-4970
- **Dashboard**: https://console.twilio.com/dashboard
- **Usage**: Makes and receives phone calls

### 4. Bright Data
- **Service**: Web scraping and proxy network
- **Zone**: unblocker
- **Dashboard**: https://brightdata.com/cp/setting/users
- **Usage**: Scrapes CQC care home data and Google Maps listings

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gatosa12/my_ai_intern.git
   cd my_ai_intern
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**:
   - Copy the environment variables section above
   - Create a new file named `.env` in the root directory
   - Paste the credentials

5. **Run the application**:
   ```bash
   # For Sussex Staffing Solutions mode
   python app.py --mode sussex_staffing
   
   # For Roofing AI Assistant mode
   python app.py --mode roofing
   ```

## 🧪 Testing with Dummy Data

You can test the system without API keys using dummy data:

```bash
python app.py --mode sussex_staffing --use-dummy-data
```

This will:
- Use sample care home data instead of live scraping
- Simulate voice synthesis locally
- Skip actual phone calls

## 💰 Cost Estimates

### Per Successful Call (approximates):
- **OpenAI (GPT-4)**: £0.15-0.30 per call
- **ElevenLabs**: £0.10-0.20 per call
- **Twilio**: £0.02-0.05 per minute
- **Bright Data**: £0.50-1.00 per 1000 requests

**Total per qualified lead**: £0.80-1.50

### Monthly Subscription Costs:
- OpenAI: Pay-as-you-go (no subscription)
- ElevenLabs: £22/month (Starter) or £99/month (Creator)
- Twilio: Pay-as-you-go + £1/month per phone number
- Bright Data: £500/month (minimum for Unblocker zone)

## 🔒 Security Notes

⚠️ **IMPORTANT**: 
- Never commit the `.env` file to GitHub
- Add `.env` to your `.gitignore` file
- Rotate API keys if they're ever exposed
- Keep your Twilio Auth Token private

## 📞 Support Contacts

- **OpenAI Support**: https://help.openai.com
- **ElevenLabs Support**: support@elevenlabs.io
- **Twilio Support**: https://support.twilio.com
- **Bright Data Support**: support@brightdata.com

## ✅ Next Steps

1. Set up your `.env` file with all credentials
2. Test with dummy data first
3. Run a small pilot with 10-20 leads
4. Monitor costs and response rates
5. Scale up based on results

---

**Last Updated**: January 2025
**Project**: AI Sales Intern - Sussex Staffing Solutions & Roofing AI
**Repository**: https://github.com/gatosa12/my_ai_intern
