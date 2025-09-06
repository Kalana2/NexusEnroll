from fastapi import FastAPI, HTTPException, status
from typing import List
from src.services.user_service import UserService
from src.models.user import User, UserCreate, UserUpdate, UserLogin

app = FastAPI(title="NexusEnroll User Service", version="1.0.0")
user_service = UserService()


@app.get("/users", response_model=List[User])
def list_users():
    return user_service.list_users()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    return user_service.create_user(user.dict())


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user_update: UserUpdate):
    updated = user_service.update_user(user_id, user_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: str):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="User not found or could not be deleted"
        )
    return {"success": True}


@app.post("/users/login", response_model=User)
def login(login: UserLogin):
    user = user_service.authenticate_user(login.username, login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
