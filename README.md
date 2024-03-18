# Welcome to streamlit


Install dependencies
```
pip install -r requirements.txt
```

Create .env file in the root directory. 

Get API key from OpenAI and add to the .env file
```
OPENAI_API_KEY=sk-CZHGP17hlblablablablablav
```

Run app
```
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```