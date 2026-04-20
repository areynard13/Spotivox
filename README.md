# Spotivox
Spotivox is a voice-controlled interface designed for task execution through an autonomous agent architecture. The system utilizes local wake word detection to trigger interactions, ensuring data privacy and low-latency response times.

# Get Started
Clone the repository
```bash
git clone https://github.com/areynard13/Spotivox.git
cd Spotivox
```

## Environment Setup
create a virtual environment and install dependencies

## With Venv
```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### With Conda
```bash
conda create -n spotivox python=3.11
conda activate spotivox

pip install -r requirements.txt
```

## Configuration

Spotivox uses environment variables to connect with:

* Spotify API (music control)
* Groq via LiteLLM (LLM agent)

### Spotify API

#### 1. Create an application
Go to Spotify for Developers

* Dashboard → **Create App**
* Name: `Spotivox`
* Add a Redirect URI:
```
http://localhost:8888/callback
```

#### 2. Get your credentials
From your Spotify app dashboard:
* Client ID
* Client Secret

#### 3. Create a `.env` file
At the root of the project:
```bash
cp .env.example .env
```

### Groq (LiteLLM)

#### 1. Get an API key
Go to Groq

* Create an account
* Generate an API key

#### 2. Add it to `.env`