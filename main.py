from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware      
#needed to allow communication between our front end server and backend server
#This is needed because we are hosting the frontend and backend separately, 
#if they were to run on a single server (like some other workflows that combine backend and frontend in one) it would not be needed

from fastapi.staticfiles import StaticFiles
#staticfiles is needed for serving content of articles from a markdown file, and to serve images from backend
#STUDENTS WILL NOT GET THIS FAR, YOU CAN SKIP

#import the api endpoint files, tis is only needed because I categorised my endpoitns in multiple files, if they do all the endpoints in main it can be skiped
from api import user
from api import exercises
from api import articles

app = FastAPI()

app.mount("/static", StaticFiles(directory="articles"), name="articles") #again, needed for serving articles from backend, can skip as students wont get that far

#orgins is a list of locations we expect traffic from, by default running a new react project starts at port 3000
orgins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000"
]

#adds the cors middleware to the app, with default settings that allow all methods, and use the orgins we defined above
app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#tags is what sections the endpoints it will appear under in the docs (the ones you get be going to http://127.0.0.1:8000/docs when server is running)
#this is only needed because I have endpoints in multiple files, if endpoints are in main it can be skipped
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(exercises.router, prefix="/workouts", tags=["Workouts"])
app.include_router(articles.router, prefix="/articles", tags=["Articles"])


#They don't actually need this part it's just the default example endpoint I never ended up removing
@app.get("/")
async def root():
    return {"message" : "Hello World"}
