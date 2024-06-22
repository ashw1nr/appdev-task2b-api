from typing import Union
from fastapi import FastAPI
from fastapi import HTTPException
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
    if character == "tom":
        return {"image": os.getenv("TOM_IMG_LINK", "tom-default-link")}
    elif character == "jerry":
        return {"image": os.getenv("JERRY_IMG_LINK", "jerry-default-link")}
    elif character == "obstacle":
        return {"image": os.getenv("OBSTACLE_IMG_LINK", "obstacle-default-link")}
    else:
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




@app.get("/")
async def read_root():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tom and Jerry Game API Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #333;
        }
        .container {
            width: 80%;
            margin: auto;
            overflow: hidden;
        }
        header {
            background: #35424a;
            color: #ffffff;
            padding-top: 30px;
            min-height: 70px;
            border-bottom: #e8491d 3px solid;
        }
        header a {
            color: #ffffff;
            text-decoration: none;
            text-transform: uppercase;
            font-size: 16px;
        }
        header ul {
            padding: 0;
            list-style: none;
        }
        header li {
            display: inline;
            padding: 0 20px 0 20px;
        }
        .main {
            padding: 20px;
            background: #ffffff;
            margin-top: 20px;
            border: #e8491d 1px solid;
        }
        .endpoint {
            margin-bottom: 20px;
        }
        .endpoint h2 {
            color: #e8491d;
        }
        .endpoint pre {
            background: #f4f4f9;
            padding: 10px;
            border: #e1e1e1 1px solid;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div id="branding">
                <h1>Tom and Jerry Game API</h1>
            </div>
            <nav>
                <ul>
                    <li><a href="#obstacleLimit">obstacleLimit</a></li>
                    <li><a href="#images">images</a></li>
                    <li><a href="#reward">reward</a></li>
                    <li><a href="#penalty">penalty</a></li>
                    <li><a href="#obstacleCourse">obstacleCourse</a></li>
                    <li><a href="#randomWord">randomWord</a></li>
                </ul>
            </nav>
        </div>
    </header>
    <div class="container main">
        <div class="endpoint" id="obstacleLimit">
            <h2>GET /obstacleLimit</h2>
            <p>Returns a number that represents the number of times Jerry can hit an obstacle before Tom catches up.</p>
            <pre>
Example Response:
{
    "obstacleLimit": 3
}
            </pre>
        </div>
        <div class="endpoint" id="images">
            <h2>POST /images</h2>
            <p>Returns an image link of the requested character.</p>
            <p><strong>Request Parameter:</strong></p>
            <ul>
                <li><strong>character</strong> (string) - can take values "tom", "jerry", "obstacle".</li>
            </ul>
            <pre>
Example Request:
POST /images
{
    "character": "tom"
}

Example Response:
{
    "image": "tom-default-link"
}
            </pre>
        </div>
        <div class="endpoint" id="reward">
            <h2>GET /reward</h2>
            <p>Returns a random reward when hitting a type of obstacle in hacker mode.</p>
            <pre>
Possible Rewards:
- 2x speed
- 3x speed
- Auto jump upcoming obstacles for n seconds

Example Response:
{
    "reward": "2x speed"
}
            </pre>
        </div>
        <div class="endpoint" id="penalty">
            <h2>GET /penalty</h2>
            <p>Returns a random penalty when hitting a type of obstacle in hacker mode.</p>
            <pre>
Possible Penalties:
- Bring Tom closer by one threshold

Example Response:
{
    "penalty": "Bring Tom closer by one threshold"
}
            </pre>
        </div>
        <div class="endpoint" id="obstacleCourse">
            <h2>GET /obstacleCourse</h2>
            <p>Returns a character array of a specified length depicting the obstacle course. The characters "L", "M", "R", "B" represent different types of obstacles.</p>
            <pre>
Example Response:
{
    "obstacleCourse": ["L", "M", "R", "B", "L", "M", "R", "B"]
}
            </pre>
        </div>
        <div class="endpoint" id="randomWord">
            <h2>GET /randomWord</h2>
            <p>Generates a random word of a specified length (between 5 and 15 characters) and returns it.</p>
            <p><strong>Query Parameter:</strong></p>
            <ul>
                <li><strong>n</strong> (int) - the length of the word.</li>
            </ul>
            <pre>
Example Request:
GET /randomWord?n=6

Example Response:
{
    "word": "kotlin"
}
            </pre>
        </div>
    </div>
</body>
</html>

    """

