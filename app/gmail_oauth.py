import os
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
from config import Config

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_config(
    {
        "web": {
            "client_id": Config.CLIENT_ID,
            "client_secret": Config.CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    scopes=SCOPES
)

flow.redirect_uri = Config.REDIRECT_URI