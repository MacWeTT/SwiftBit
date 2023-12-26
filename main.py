from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus

# Router imports
from routes.url import urlRouter
from routes.user import userRouter

# Application Initialization
app = FastAPI()
app.middleware(CORSMiddleware)
app.include_router(urlRouter, tags=["url"])
app.include_router(userRouter, tags=["user"])

# Template and Static File Initialization
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "response": {
                "status": HTTPStatus.OK,
                "message": "All API services are up and running.",
            },
        },
    )
