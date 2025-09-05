from supabase import create_client, Client

SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"  # Replace with your Supabase project URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"      # Replace with your Supabase API key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Example: Fetch all rows from a table named 'users'
response = supabase.table("users").select("*").execute()
print(response.data)

# Example: Insert a new row into 'users'
# result = supabase.table("users").insert({"email": "test@example.com", "name": "Test User"}).execute()
# print(result.data)
