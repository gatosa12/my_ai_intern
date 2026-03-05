@echo off
REM ========================================
REM AI Sales Intern - One-Click Windows Setup
REM Sussex Staffing Solutions + Roofing AI
REM ========================================

color 0A
echo.
echo ========================================
echo   AI SALES INTERN - AUTOMATED SETUP
echo   Sussex Staffing ^& Roofing AI
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [1/7] Python detected...
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Git is not installed!
    echo Downloading repository as ZIP instead...
    echo.
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/gatosa12/my_ai_intern/archive/refs/heads/main.zip' -OutFile 'my_ai_intern.zip'"
    powershell -Command "Expand-Archive -Path 'my_ai_intern.zip' -DestinationPath '.' -Force"
    cd my_ai_intern-main
    goto CONTINUE_SETUP
)

echo [2/7] Git detected...
echo.

REM Clone repository if not already cloned
if not exist "my_ai_intern" (
    echo [3/7] Cloning AI Sales Intern repository...
    git clone https://github.com/gatosa12/my_ai_intern.git
    cd my_ai_intern
) else (
    echo [3/7] Repository already exists, pulling latest changes...
    cd my_ai_intern
    git pull
)

:CONTINUE_SETUP

echo.
echo [4/7] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)

echo.
echo [5/7] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [6/7] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some packages may have failed to install
    echo Continuing anyway...
)

echo.
echo [7/7] Creating .env template file...
if not exist ".env" (
    (
        echo # AI Sales Intern - API Keys Configuration
        echo # Copy this template and fill in your actual API keys
        echo.
        echo # OpenAI API Key ^(GPT-4^)
        echo OPENAI_API_KEY=your_openai_key_here
        echo.
        echo # ElevenLabs API Key ^(Voice Synthesis^)
        echo ELEVENLABS_API_KEY=your_elevenlabs_key_here
        echo.
        echo # Twilio Credentials ^(Phone Calls^)
        echo TWILIO_ACCOUNT_SID=your_twilio_sid_here
        echo TWILIO_AUTH_TOKEN=your_twilio_token_here
        echo TWILIO_PHONE_NUMBER=your_twilio_phone_here
        echo.
        echo # Bright Data API Key ^(Web Scraping^)
        echo BRIGHT_DATA_API_KEY=your_brightdata_key_here
        echo BRIGHT_DATA_ZONE=unblocker
    ) > .env
    echo .env template created!
echo.
    echo IMPORTANT: Edit .env file with your actual API keys before running!
) else (
    echo .env file already exists - skipping template creation
)

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Edit .env file with your API keys from API_KEYS_SETUP.md
echo 2. Test with dummy data:
echo    python app.py --mode sussex_staffing --use-dummy-data
echo.
echo 3. Or run live:
echo    python app.py --mode sussex_staffing
echo    python app.py --mode roofing
echo.
echo For API keys, see: API_KEYS_SETUP.md
echo.
echo ========================================
echo.
pause
