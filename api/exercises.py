from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.dbutils import getExercisesDB, getWorkoutsDB, saveWorkoutsDB, getUsersDB
from typing import List, Dict

router = APIRouter()

##Pydantic models for request and response objects##

#singular exercise
class Exercise(BaseModel):
    name: str
    description: str
    type: str
    tags: List[str]

#define list of exercises as a a dictionary containing the exercise object as a value
class ExercisesList(BaseModel):
    exercises: Dict[str, Exercise]

#workout plans are build of those, each exercise in a workout has it's name, and a list of numbers for repetitions in each set
class WorkoutExerciseEntry(BaseModel):
    exercise : str
    reps : List[int]

#the actual workout
class Workout(BaseModel):
    author: str
    authorname :str
    name: str
    description: str
    tags : List[str]
    exercises : List[WorkoutExerciseEntry]

#all workouts
class WorkoutList(BaseModel):
    workouts : Dict[str, Workout]

#list of workout names the user has added
class UserWorkoutsList(BaseModel):
    workouts : List[str]

##ROUTES##

#get a list of all exercises, needed for building a new workout and to display exercise details in existing workouts
@router.get("/exercises", response_model=ExercisesList)
async def getExerciseList():
    exercises = getExercisesDB()
    return {"exercises": exercises}

#get all workouts, needed for the workout selection page
@router.get("/workouts", response_model=WorkoutList)
async def getWorkoutList():
    workouts = getWorkoutsDB()
    return {"workouts": workouts}

#get defails from a specific workout
@router.get("/workout/{workout_name}", response_model=Workout)
async def getWorkout(workout_name):
    workouts = getWorkoutsDB()

    if workout_name not in workouts:
        raise HTTPException(400, detail="no such workout in database")
    
    return workouts[workout_name]


#create a new workout, it's expecting all the workout information defined in "Workout"
@router.post("/addworkout")
async def addWorkout(workout: Workout):
    
    workouts = getWorkoutsDB()
    #some validation, if with the name exist we don't want to allow the user to overwrite one of the premium workouts, or a workout created by a different user
    if(workout.name in workouts):
        if(workouts[workout.name]["author"] == "titanic fitness"):
            raise HTTPException(400, detail="Can't overwrite premium workout, chose different name")
        elif(workout.author != workouts[workout.name]["author"]):
            raise HTTPException(400, detail="Can't overwrite workout made by another user, chose different name")      
    
    workouts[workout.name] = workout.dict()
    saveWorkoutsDB(workouts)

    return

class Token(BaseModel):
    token: str

#get the list of workouts the specific user has added to their account
@router.post("/getuserworkouts", response_model=UserWorkoutsList)
async def getUserWorkouts(token: Token):
    users = getUsersDB()
    print(token.token)
    #find if the user exists
    for person in users:
        if users[person]["access_token"] == token.token:
            return {"workouts": users[person]["exercise_plans"]}
    
    raise HTTPException(400, detail="user not found")
