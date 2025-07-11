from fastapi import FastAPI
from .core.database import lifespan

app = FastAPI(lifespan=lifespan)
