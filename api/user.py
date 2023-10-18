from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.dbutils import getUsersDB, saveUsersDB #importing the functions from db/utils.py file for accessing and saving the users

from typing import Union, List
import uuid #for the id's

import jwt  #need to install jwt with pip install pyJWT

#key unique to our website that is used in hashing to make sure people who don't know the key can't generate valid access tokens
#in real world scenario this would be in a .env file for extra security
SECRET_KEY = "testkey"

router = APIRouter() #needed because have these endpoints in user.py instead of main

##Pydantic models for request and response objects##
class UserCredentials(BaseModel):
    email: str
    password: str
    display_name : str = None #optional display_name, this way we can use same UserCredentials object for both login and registration

#define the object of data about the user we will be sending back
class UserData(BaseModel):
    id: str
    email: str
    display_name : str

#the actual response user receives when logging in (and when registering)
class LoginResponse(BaseModel):
    access_token: str
    user: UserData


@router.post("/register", response_model=LoginResponse)
async def register_user(credentials: UserCredentials):

    #get all users and teporarily store them in "users"
    users = getUsersDB()
    #guard clause making sure the user doesn't already exist
    if credentials.email in users:
       #if user already exists, raise an exception, the error message will be send to the frontend where they can handle it, function stops here
       raise HTTPException(400, detail="account already exists")

    #create new user using data received
    new_user = {
        "id": str(uuid.uuid1()), 
        "email" : credentials.email, 
        "display_name" : credentials.display_name, 
        "password" : credentials.password, 
        "exercise_plans" : [], 
        "diet_plans" : [] 
        }
    
    #what info about the user we want to cryptographically encode
    token_data = {
        "sub": new_user["id"]
    }
    #encode that info using the secret key and a specific cryptography algorithm
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    #add this token to the new user so we can use it later
    new_user["access_token"] = token

    #note: Pretty sure I'm not using the jwt token properly later on, 
    #I think the way its mean to be used is, when receiving the token during a request for data, we decode it first, then use whatever data we had encoded to do the action
    #instead later on in the project I use the token itself directly for finding users
    #for the purpose of this project this is fine though.

    #save all the new user info in the users object, we know it will create a new key because we already made sure the user with that email doesn't exist in the guard clause above
    users[credentials.email] = new_user 

    #save the new users
    saveUsersDB(users)

    #return the token and the user objects, could had just returned new_user here, doesn't matter as new_user and users[credentials.email] have the same data at this point
    return {"access_token":token, "user": users[credentials.email]}



@router.post("/login", response_model=LoginResponse)
async def login_user(user: UserCredentials):

    #get all the users
    users = getUsersDB()

    #validate credentials and send error details if credentials incorrect
    #1. Check if user exist (we are using email as the username)
    if not user.email in users:
        raise HTTPException(400, detail="account not found")
    #2. User exists, so now check if the password stored in that user is same as the one received. Passwords are stored as plaintext for simplicity
    if not user.password == users[user.email]["password"]:
        raise HTTPException(400, detail="invalid password bruh")
    
    #everything is correct, so we can make a token to send back
    token_data = {
        "sub": users[user.email]["id"]
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

    users[user.email]["access_token"] = token  #overwrite the existing token, this entire process is more of a setup for token management later on, they wont do it in this project though
    saveUsersDB(users)

    return {"access_token":token, "user": users[user.email]}

#this is how data for adding a new workout to an user account lokos like
class WorkoutSelection(BaseModel):
    workout_name: str   #we just use the name of the workout as that will be added to a list
    token : str         #we use the token to identify the user we are adding the workout to


#endpoint does not need to return anything as it only updates the db
@router.post("/addworkout")
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

            return  #need the return keyword to prevent bad request errors, but does not need to return any data

    #if the for loop didn't find a user for that token        
    raise HTTPException(400, detail="user not found")


@router.post("/removeworkout")
async def remove_workout(data: WorkoutSelection):
    users = getUsersDB()

    #find if the user exists
    for person in users:
        if users[person]["access_token"] == data.token:
            #validate that the workout exists before removing it
            if data.workout_name in users[person]["exercise_plans"]:
                users[person]["exercise_plans"].remove(data.workout_name)
                saveUsersDB(users)

                return
            else:
                raise HTTPException(400, detail="workout does not exist")
            
    
    raise HTTPException(400, detail="user not found")

