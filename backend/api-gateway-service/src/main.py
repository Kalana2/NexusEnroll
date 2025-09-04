from fastapi import FastAPI
from .routes import gateway_routes

app = FastAPI(title="NexusEnroll API Gateway")

# Include gateway routes
app.include_router(gateway_routes.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the NexusEnroll API Gateway"}
