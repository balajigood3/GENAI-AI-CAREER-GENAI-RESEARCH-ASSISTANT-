# Deployment checklist

1. Revoke any API key exposed in chat, logs, screenshots, or source control.
2. Create a replacement API key.
3. Confirm `.env` and `.streamlit/secrets.toml` are excluded from Git.
4. Push the project to GitHub.
5. Create a Streamlit Community Cloud app pointing to `app.py`.
6. Add the OpenAI key and model settings under Manage app > Settings > Secrets.
7. Reboot the app and test all modes and document upload.

Never commit a real API key. The app reads secrets at runtime.
