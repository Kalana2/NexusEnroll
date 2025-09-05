from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Enrollment Service is running!"}

# Add more endpoints and logic as needed
