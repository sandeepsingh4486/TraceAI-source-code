# Deployment Options

## Fastest: local laptop

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints, normally `http://localhost:8501`.

## Streamlit Community Cloud

1. Put the project in a GitHub repository.
2. Create a Streamlit Community Cloud app from `app.py`.
3. Add `GEMINI_API_KEY` in the app's secret/environment configuration.
4. Deploy.
5. Test Demo mode and Live AI mode before submission.

## Presentation fallback

Always keep **Demo** mode available. It shows the exact expected UX without depending on:
- Wi-Fi
- API quota
- API latency
- temporary provider errors

For judging, show Demo first, then Live AI on a short unseen requirement if connectivity is stable.
