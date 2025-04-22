import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv

""""
Connection to supabase
"""
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
