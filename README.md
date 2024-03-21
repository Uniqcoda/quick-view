# Welcome to  Quick View! 📄🕵🏻

## Setup

### Install dependencies

Create a virtual environment.
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

There can be issues with using the pytesseract package. Installing its co-dependencies may fix it:
```
tesseract
tesseract-ocr
```

Otherwise, ensure tesseract is installed on the local machine:
Mac
```
brew install tesseract
```
Ubuntu
```
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
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