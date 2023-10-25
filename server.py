import logging
import warnings
import os
import typing
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import newrelic.agent
from getCustomAttributes import getCustomAttributes, getCustomAttributesEnd
from pkg_resources import PkgResourcesDeprecationWarning

warnings.simplefilter("ignore", category=PkgResourcesDeprecationWarning)

app = FastAPI(title="Battlesnake")
newrelic.agent.initialize('newrelic.ini')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_server(handlers: typing.Dict):

    @app.get("/")
    async def on_info():
        return handlers["info"]()

    @app.post("/start")
    async def on_start(request: Request):
        game_state = await request.json()
        handlers["start"](game_state)
        return "ok"

    @app.post("/move")
    async def on_move(request: Request):
        game_state = await request.json()
        attributes = getCustomAttributes(game_state)
        for key, value in attributes.items():
            newrelic.agent.add_custom_parameter(key, value)
        return handlers["move"](game_state)

    @app.post("/end")
    async def on_end(request: Request):
        game_state = await request.json()
        attributes = getCustomAttributes(game_state)
        for key, value in attributes.items():
            newrelic.agent.add_custom_parameter(key, value)
        handlers["end"](game_state)
        return "ok"

    @app.get("/ping")
    async def on_ping():
        return "ok"

    @app.head("/ping")
    async def on_head():
        return JSONResponse(content=None, status_code=200)

    @app.middleware("http")
    async def identify_server(request: Request, call_next):
        response = await call_next(request)
        response.headers["server"] = "battlesnake/github/starter-snake-python"
        return response

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))

    logging.getLogger("uvicorn.access").setLevel(logging.ERROR)

    print(f"\nRunning Battlesnake at http://{host}:{port}")
    import uvicorn
    uvicorn.run(app, host=host, port=port)