from typing import Union
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

import random
import os

# Define a Pydantic model for the request body
class WordRequest(BaseModel):
    length: int

class ObstacleCourseRequest(BaseModel):
    extent: int

class ThemeRequest(BaseModel):
    date: str
    time: str

app = FastAPI()


# 1. The number of times that Jerry can bit an obstacle before Tom catches it. (Instead of the default, 2, given now)
@app.get("/obstacleLimit")
async def get_obstacle_limit():
    obstacle_limit = random.randint(2, 5)
    return {"obstacleLimit": obstacle_limit}

# 2. Images Tom, Jerry and Obstacles. together
@app.get("/image")
async def get_image(character: str):
    character = character.strip().lower()
    file_path = os.path.join("images", character+".png")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    #return {"error": "Image not found"}
    raise HTTPException(status_code=404, detail="character should be 'tom' or 'jerry' or 'obstacle'.")

# 3. Hacker mode's reward/punishment on hitting a type of obstacle feature-> Implement it by getting the random reward from the API
# a. 2x/3x speed
# b.Bring Tom closer by one threshold
# c.Auto jump upcoming obstacles for n seconds

@app.get("/hitHindrance")
async def get_reward_or_punish():
    effects = {1:"Increase speed of run by given amount", 2:"Auto jump upcoming obstacles for given seconds", 3:"Bring Tom closer by given threshold and if he crosses Jerry, let him catch Jerry"}
    choice = random.randint(1,3)
    if choice==1:
        amount = random.randint(2,3)
    elif choice==2:
        amount = random.randint(2,6)
    else:
        amount = random.randint(1,2)
    return {"type":choice,
            "amount":amount,
            "description":effects[choice]}

# GET /obstacleCourse
# returns a character array of length (insert length here) with characters "L", "M", "R" in a random order depicting the obstacle course.
# used POST for /images because otherwise all routes are just GET
# example request for POST /image
@app.post("/obstacleCourse")
async def get_obstacle_course(request: ObstacleCourseRequest):
    obstacle_course = ["L", "L", "M", "M", "R", "R", "B"] * (request.extent//4 + 1)
    random.shuffle(obstacle_course)
    obstacle_course = obstacle_course[:request.extent]
    return {"obstacleCourse": obstacle_course}


words = {
    5: ["delta", "force"],
    6: ["canvas", "kotlin"],
    7: ["android", "adapter"],
    8: ["retrofit", "activity"],
    9: ["animation", "interface"],
    10: ["viewmodel", "repository"],
    11: ["architecture", "notification"],
    12: ["implementation", "multithreading"],
    13: ["instrumentation", "connectivity"],
    14: ["fragmentmanager", "intentfilters"],
    15: ["configuration", "navigationgraph"]
}

# generate a random word of length "n" (taken from query parameter) characters and return it
@app.post("/randomWord")
async def get_random_word(request: WordRequest):
    n = request.length
    if n not in words:
        raise HTTPException(status_code=400, detail="length of word should be between 5 and 15.")
    word = random.choice(words[n])
    return {"word": word}

@app.post("/theme")
async def get_theme(request: ThemeRequest):
    date = request.date
    time = request.time
    theme = "day"
    if len(date)!=10 or date[4]!="-" or date[7]!="-" or len(time)!=8 or time[2]!=":" or time[5]!=":":
        raise HTTPException(status_code=400, detail="Enter date(YYYY-MM-DD) and time(HH:MM:SS) in correct format.")
    try:
        print(date," ",time)
        month = int(date[5:7])
        hour = int(time[:2])
        mins = int(time[3:5])
        if month<=4:
            if hour>17 or hour<9:
                theme="night"
        elif month<=8:
            if hour>18 or hour<8:
                theme = "night"
        else:
            if hour>16 or hour<10:
                theme = "night"
    except:
        raise HTTPException(status_code=400, detail="Enter date in correct format YYYY-MM-DD.")
    return {"theme": theme}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("api/docs.html") as html_file:
        return HTMLResponse(content=html_file.read())