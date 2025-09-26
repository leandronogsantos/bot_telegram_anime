import os 
from dotenv import load_dotenv
from huggingface_hub import login

def get_auth():   
    load_dotenv() 
    return {'hf_token': login(token=os.getenv("HF_LOGIN_TOKEN")), "tl_token":os.getenv("TELEGRAM_TOKEN") }


