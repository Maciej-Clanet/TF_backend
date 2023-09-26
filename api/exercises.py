from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.dbutils import getExercisesDB, getWorkoutsDB, saveWorkoutsDB, getUsersDB
from typing import List, Dict

router = APIRouter()

##Pydantic models for request and response objects##

class Exercise(BaseModel):
    name: str
    description: str
    type: str
    tags: List[str]

class ExercisesList(BaseModel):
    exercises: Dict[str, Exercise]


class WorkoutExerciseEntry(BaseModel):
    exercise : str
    reps : List[int]

class Workout(BaseModel):
    author: str
    authorname :str
    name: str
    description: str
    tags : List[str]
    exercises : List[WorkoutExerciseEntry]


class WorkoutList(BaseModel):
    workouts : Dict[str, Workout]

class UserWorkoutsList(BaseModel):
    workouts : List[str]

##ROUTES##


@router.get("/exercises", response_model=ExercisesList)
async def getExerciseList():
    exercises = getExercisesDB()
    return {"exercises": exercises}

@router.get("/workouts", response_model=WorkoutList)
async def getWorkoutList():
    workouts = getWorkoutsDB()
    return {"workouts": workouts}

@router.get("/workout/{workout_name}", response_model=Workout)
async def getWorkout(workout_name):
    workouts = getWorkoutsDB()

    if workout_name not in workouts:
        raise HTTPException(400, detail="no such workout in database")
    
    return workouts[workout_name]

class Test(BaseModel):
    test : str

@router.post("/addworkout",  response_model=WorkoutList)
async def addWorkout(workout: Workout):
    
    workouts = getWorkoutsDB()
    workouts[workout.name] = workout.dict()
    saveWorkoutsDB(workouts)

    return {"workouts":workouts}

    saveWorkoutsDB(workouts)
    
    return WorkoutList(workouts = workouts)
    saveWorkoutsDB(workouts)
    # return workouts
    # return {"test" : "dsadsa"}
    return True

class Token(BaseModel):
    token: str

@router.post("/getuserworkouts", response_model=UserWorkoutsList)
async def getUserWorkouts(token: Token):
    users = getUsersDB()
    print(token.token)
    #find if the user exists
    for person in users:
        if users[person]["access_token"] == token.token:
            return {"workouts": users[person]["exercise_plans"]}
    
    raise HTTPException(400, detail="user not found")
