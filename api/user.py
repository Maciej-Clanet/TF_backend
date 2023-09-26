from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.dbutils import getUsersDB, saveUsersDB

from typing import Union, List
import uuid

import jwt

SECRET_KEY = "testkey"

router = APIRouter()

##Pydantic models for request and response objects##

class UserCredentials(BaseModel):
    email: str
    password: str
    display_name : str = None

class UserData(BaseModel):
    id: str
    email: str
    display_name : str
    # exercise_plans: Union[List[str], None] = None
    # diet_plans: Union[List[str], None] = None

class LoginResponse(BaseModel):
    access_token: str
    user: UserData


@router.post("/register", response_model=LoginResponse)
async def register_user(credentials: UserCredentials):

    users = getUsersDB()
    if credentials.email in users:
       raise HTTPException(400, detail="account already exists")

    new_user = {
        "id": str(uuid.uuid1()), 
        "email" : credentials.email, 
        "display_name" : credentials.display_name, 
        "password" : credentials.password, 
        "exercise_plans" : [], 
        "diet_plans" : [] 
        }
    
    token_data = {
        "sub": new_user["id"]
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    new_user["access_token"] = token

    users[credentials.email] = new_user

    saveUsersDB(users)


    return {"access_token":token, "user": users[credentials.email]}



@router.post("/login", response_model=LoginResponse)
async def login_user(user: UserCredentials):
    users = getUsersDB()

    #validate credentials and send error details
    if not user.email in users:
        raise HTTPException(400, detail="account not found")
    if not user.password == users[user.email]["password"]:
        raise HTTPException(400, detail="invalid password bruh")
    

    token_data = {
        "sub": users[user.email]["id"]
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

    users[user.email]["access_token"] = token
    saveUsersDB(users)

    return {"access_token":token, "user": users[user.email]}


class WorkoutSelection(BaseModel):
    workout_name: str
    token : str

@router.post("/addworkout", response_model=UserData)
async def add_workout(data : WorkoutSelection):
    users = getUsersDB()

    #find if the user exists
    for person in users:
        if users[person]["access_token"] == data.token:
            #validate to make sure can't add the same workout twice
            if data.workout_name in users[person]["exercise_plans"]:
                raise HTTPException(400, detail="workout already added")
            
            users[person]["exercise_plans"].append(data.workout_name)
            saveUsersDB(users)

            #return new user state for updating front end
            return users[person]
        
    raise HTTPException(400, detail="user not found")

@router.post("/removeworkout", response_model=UserData)
async def remove_workout(data: WorkoutSelection):
    users = getUsersDB()

    #find if the user exists
    for person in users:
        if users[person]["access_token"] == data.token:
            #validate that the workout exists before removing it
            if data.workout_name in users[person]["exercise_plans"]:
                users[person]["exercise_plans"].remove(data.workout_name)
                saveUsersDB(users)

                #return new user state for updating front end
                return users[person]
            else:
                raise HTTPException(400, detail="workout does not exist")
            
    
    raise HTTPException(400, detail="user not found")

