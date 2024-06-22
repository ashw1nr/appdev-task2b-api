from typing import Union
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import HTMLResponse, FileResponse

import random
import os


app = FastAPI()


# 1. The number of times that Jerry can bit an obstacle before Tom catches it. (Instead of the default, 2, given now)
@app.get("/obstacleLimit")
async def get_obstacle_limit():
    obstacle_limit = random.randint(2, 5)
    return {"obstacleLimit": obstacle_limit}

# 2. Image links of Tom, Jerry and Obstacles. together
@app.post("/images")
async def get_image(character: str):
    character.strip().lower()
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
@app.get("/reward")
async def get_reward():
    rewards = ["2x speed", "3x speed", "Auto jump upcoming obstacles for n seconds"]
    reward = random.choice(rewards)
    return {"reward": reward} 

@app.get("/penalty")
async def get_penalty():
    penalties = ["Bring Tom closer by one threshold"]
    penalty = random.choice(penalties)
    return {"penalty": penalty}

# GET /obstacleCourse
# returns a character array of length (insert length here) with characters "L", "M", "R" in a random order depicting the obstacle course.
# used POST for /images because otherwise all routes are just GET
# example request for POST /image
@app.get("/obstacleCourse")
async def get_obstacle_course():
    obstacle_course = ["L", "M", "R", "B"] * 12
    random.shuffle(obstacle_course)
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

# generate a random word of length "n" (taken from querry parameter) characters and return it
@app.get("/randomWord")
async def get_random_word(n: int):
    if n not in words:
        raise HTTPException(status_code=400, detail="length of word should be between 5 and 15.")
    word = random.choice(words[n])
    return {"word": word}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("api/docs.html") as html_file:
        return HTMLResponse(content=html_file.read())