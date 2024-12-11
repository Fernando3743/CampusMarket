from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del cliente de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

