# API Keys Setup Guide

This file contains all the API keys and credentials you've collected for your AI Sales Intern project.

## 🔑 Environment Variables

Create a `.env` file in the root directory of your project and add these credentials:

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs API Key
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Twilio Credentials
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# Bright Data API Key
BRIGHT_DATA_API_KEY=your_bright_data_api_key_here
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
- **Phone Number**: (see your Twilio console)
- **Dashboard**: https://console.twilio.com/dashboard
- **Usage**: Makes and receives phone calls

### 4. Bright Data
- **Service**: Web scraping and proxy network
- **Zone**: unblocker
- **Dashboard**: https://brightdata.com/cp/setting/users
- **Usage**: Scrapes CQC care home data and Google Maps listings

## ⚠️ Security Notice

NEVER commit real API keys to this repository. Store your actual keys in a `.env` file locally and add `.env` to your `.gitignore`.
