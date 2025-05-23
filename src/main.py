from fastapi import FastAPI
import uvicorn
from src.config.configs import CacheSettings
import os
from src.routes import intro, book, auth, protected, user_book_review, user, book_summary
from src.middleware.middleware import add_process_time
# from src.middleware.redis_middleware import RedisCacheMiddleware
# from src.exceptions.exception import SourceException
# from fastapi_pagination import add_pagination
from contextlib import asynccontextmanager
from src.db import init_db


# os.environ["DEVELOPMENT_DATABASE_HOST"] = "test_os_host"
# os.environ["DEVELOPMENT_DATABASE_USERNAME"] = "test_os_user"
os.environ.pop('DEVELOPMENT_DATABASE_HOST', None) 
os.environ.pop('DEVELOPMENT_DATABASE_USERNAME', None) 


cache_settings = CacheSettings()

#life span event
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("in life span")
    init_db()
    yield

def create_app(lifespan:lifespan) -> FastAPI:
    fastapi_app = FastAPI(title="Intelligent Book Management System",
                          description="An intelligent book management system that uses AI to provide recommendations and manage book collections.",
                          version="0.0.1",
                          lifespan=lifespan
                          )
    # Middleware Settings
    fastapi_app.middleware("http")(add_process_time)

    # fastapi_app.add_middleware(RedisCacheMiddleware, cache_settings=cache_settings)

    # fastapi_app.add_exception_handler(SourceException, source_exception_handler)
    for router in get_fastapi_routers():
        fastapi_app.include_router(router)

    return fastapi_app

def get_fastapi_routers():
    return [
        auth.router,
        protected.router,
        intro.router,
        book.router,
        user.router,
        user_book_review.router,
        book_summary.router
    ]


app = create_app(lifespan=lifespan)
# add_pagination(app)
if __name__ == "__main__":
    uvicorn.run("main:app")



