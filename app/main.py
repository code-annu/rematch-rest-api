from fastapi import FastAPI

from .core.database import lifespan
from .router.user_router import user_router
from .router.qna_router import qna_router

app = FastAPI(lifespan=lifespan)

app.include_router(router=user_router,prefix="/user")
app.include_router(router=qna_router,prefix="/qna")



