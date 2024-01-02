from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus

# Router imports
from routes.url import urlRouter
from routes.user import userRouter

tags_metadata = [
    {
        "name": "Users",
        "description": "User level operations.",
    },
    {
        "name": "Urls",
        "description": "Create and manage short URLs.",
    },
]

# Application Initialization
app = FastAPI(openapi_tags=tags_metadata)
app.middleware(CORSMiddleware)

# Router Initialization
app.include_router(urlRouter, tags=["Urls"])
app.include_router(userRouter, tags=["Users"])

# Template and Static File Initialization
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Root Route
@app.get("/")
async def root(request: Request):
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
