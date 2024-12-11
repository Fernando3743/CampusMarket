from django.http import JsonResponse
from .supabase_client import supabase

# Create a new user
def create_user_view(request):
    data = {"full_name": "Alice", "mail": "alice@example.com","password":"1234"}
    response = supabase.table("user").insert(data).execute()
    return JsonResponse(response.data, safe=False)

# Get all users
def get_users_view(request):
    response = supabase.table("user").select("*").execute()
    return JsonResponse(response.data, safe=False)

# Update a user
def update_user_view(request, user_id):
    new_data = {"full_name": "Lauren"}
    response = supabase.table("user").update(new_data).eq("id", user_id).execute()
    return JsonResponse(response.data, safe=False)

# Delete a user
def delete_user_view(request, user_id):
    response = supabase.table("user").delete().eq("id", user_id).execute()
    return JsonResponse(response.data, safe=False)