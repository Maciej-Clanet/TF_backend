from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

#import the api endpoint files
from api import user
from api import exercises
from api import articles

app = FastAPI()

app.mount("/static", StaticFiles(directory="articles"), name="articles")

orgins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#tags is what sections the endpoints it will appear under in the docs
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(exercises.router, prefix="/workouts", tags=["Workouts"])
app.include_router(articles.router, prefix="/articles", tags=["Articles"])


@app.get("/")
async def root():
    return {"message" : "Hello World"}

#random comment test