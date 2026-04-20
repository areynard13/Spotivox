import os

def check_dotenv_vars():
    """Check if the required vars are stored in the dotenv file"""
    required_vars = ["SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET", "SPOTIPY_REDIRECT_URI", "GROQ_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise EnvironmentError(f"The following variables are missing from your .env file: {', '.join(missing)}")