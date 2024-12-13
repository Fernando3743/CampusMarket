from supabase import create_client, Client

# Configura las credenciales del proyecto
url: str = "https://vnnwzzlzcyqqgzrygwmd.supabase.co"  # URL de tu proyecto
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZubnd6emx6Y3lxcWd6cnlnd21kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzM5NTQxMzEsImV4cCI6MjA0OTUzMDEzMX0.CdCZOFj4kFppQs9pqgz12s_xgxFK-dCaa676Rz7rsX8"  # Clave API
supabase: Client = create_client(url, key)

# Verificar la conexión
response = supabase.table("nombre_de_tabla").select("*").execute()
print(response.data)