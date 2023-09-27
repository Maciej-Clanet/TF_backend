import json

def getUsersDB():
    with open("db/usersDB.json", "r+") as file:
        return json.load(file)
    
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