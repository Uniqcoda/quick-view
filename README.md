# Welcome to  Quick View! 📄🕵🏻

## Setup

### Install dependencies

Create a virtual environment. The common way to name virtual environments is `env`. But you can give it a different name to easily identify it. So, we would use `.my_venv` instead.
```
python3 -m venv .my_venv
```

Add this virtual environment to your .gitignore file, so you don't push it to GitHub.

Activate the virtual env
```
source .my_venv/bin/activate # Linux/Mac
.\.my_venv\Scripts\activate # Windows 
```

Upgrade pip
```
python3 -m pip install --upgrade pip
```

Install dependencies
```
pip install -r requirements.txt
```

### Add API keys to .env file
Create .env file in the root directory. 

Get API key from OpenAI and add to the .env file
```
OPENAI_API_KEY=sk-CZHGP17hlblablablablablav
```

Run app
```
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```