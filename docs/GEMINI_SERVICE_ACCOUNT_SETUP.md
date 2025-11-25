# Gemini API Service Account Setup

This guide explains how to configure Service Account authentication for the Gemini API chatbot in the Streamlit dashboard.

## What was changed?

The code now supports **two authentication methods**:

1. **Service Account (Recommended)** - Uses OAuth2 Bearer tokens
2. **API Key (Fallback)** - Simple API key authentication

## Setup Instructions

### Option 1: Service Account Authentication (Your Method)

1. **Save your Service Account JSON file**:
   - Place the `service-account.json` file in `frontend/streamlit_dashboard/`
   - The file is already created with your credentials
   - ⚠️ **IMPORTANT**: This file is in `.gitignore` and will NOT be pushed to GitHub

2. **Set environment variable** (optional):
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="frontend/streamlit_dashboard/service-account.json"
   ```
   
   Or add to your `.env` file:
   ```
   GOOGLE_APPLICATION_CREDENTIALS="frontend/streamlit_dashboard/service-account.json"
   ```

3. **Run the app**:
   ```bash
   cd frontend/streamlit_dashboard
   streamlit run app.py
   ```

### Option 2: API Key Authentication (Fallback)

If you prefer using a simple API key instead:

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Add to your `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   ```

## How the Authentication Works

The code automatically tries Service Account first, then falls back to API key:

```python
# 1. Try Service Account (if service-account.json exists)
credentials = service_account.Credentials.from_service_account_file(
    service_account_path,
    scopes=['https://www.googleapis.com/auth/generative-language.retriever']
)
credentials.refresh(Request())
access_token = credentials.token

# 2. Fall back to API Key (if Service Account fails)
api_key = os.getenv("GEMINI_API_KEY")
```

## Required Packages

These packages were added to `requirements.txt`:

- `google-auth>=2.23.0` - For Service Account authentication
- `google-generativeai>=0.8.0` - For Gemini API client library

Install them with:
```bash
pip install google-auth google-generativeai
```

## Security Notes

- ✅ The `service-account.json` file is excluded from git via `.gitignore`
- ✅ Never commit or share your private key
- ✅ The file is only stored locally on your machine
- ⚠️ When deploying (Streamlit Cloud, server, etc.), upload the file separately or use environment variables

## Troubleshooting

### "Service Account auth failed"
- Check that `service-account.json` exists in `frontend/streamlit_dashboard/`
- Verify the file contains valid JSON
- Ensure the Service Account has access to Gemini API

### "404 Not Found" errors
- Some models require specific permissions (e.g., gemini-1.5-pro might need approval)
- The code automatically falls back to available models (gemini-1.5-flash)
- Check your Service Account's enabled APIs in Google Cloud Console

### "Neither GOOGLE_APPLICATION_CREDENTIALS nor GEMINI_API_KEY found"
- Set one of these in your `.env` file or environment variables
- For Service Account: point to your JSON file path
- For API Key: get one from Google AI Studio

## Testing

Test the authentication with:
```bash
cd frontend/streamlit_dashboard
streamlit run app.py
```

Then use the chatbot in the app. Check the terminal output for:
- "Using Service Account authentication" (if successful)
- "Service Account auth failed, trying API key" (if falling back)

## Reference

- [Google Cloud Service Accounts](https://cloud.google.com/iam/docs/service-accounts)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google Auth Library](https://google-auth.readthedocs.io/)
