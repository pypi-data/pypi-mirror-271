from .settings import settings
from .verification import generate_code
from .session import session_startup
from .router import auth_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles



def startup():
    """ initialize auth and test settings """
    # print(settings)

    code = generate_code()

    assert(settings.auth_transport in ['session', 'jwt'])

    if settings.auth_transport == "session":
        # session_startup(app)
        pass

