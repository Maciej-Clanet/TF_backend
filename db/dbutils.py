import json

#just some functions for getting the right jeson files or modifying them

#gets the entire users file
def getUsersDB():
    with open("db/usersDB.json", "r+") as file:
        return json.load(file)
    
#needs to receive a new users file (with all users, not just the new user), overwrites the old file
def saveUsersDB(newUsers):
    with open("db/usersDB.json", "w+") as file:
        file.write(json.dumps(newUsers, indent=4))

def getExercisesDB():
    with open("db/exercisesDB.json", "r+") as file:
        return json.load(file)
    
def getWorkoutsDB():
    with open("db/workoutsDB.json", "r+") as file:
        return json.load(file)

def saveWorkoutsDB(newWorkouts):
    print(newWorkouts)
    with open("db/workoutsDB.json", "w+") as file:
        file.write(json.dumps(newWorkouts, indent=4))

def getArticles():
    with open("db/articlesDB.json", "r+") as file:
        return json.load(file)