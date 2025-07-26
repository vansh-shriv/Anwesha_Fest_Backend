import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("path/firebase/anweshawebapp-firebase-adminsdk-fbsvc-97038c7575.json")
firebase_admin.initialize_app(cred)

def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        return None
