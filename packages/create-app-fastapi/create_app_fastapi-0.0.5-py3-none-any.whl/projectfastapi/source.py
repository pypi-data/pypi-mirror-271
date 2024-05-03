# main file data
def main(name):
    result= '{"message": "Service started successfully"}'
    return f"""from fastapi import FastAPI
from APIs import api

app = FastAPI(
    title="{name} API",
    version="1.0"
)

@app.get('/')
def root():
    return {result}

# include api routes with main app
app.include_router(api.app)

"""
# gitignore file data
def gitignore(venv):
    return f"""__pycache__
{venv}
.env
"""

# auth file
def auth():
    return """from fastapi.security import OAuth2PasswordBearer

#jwt token, user password encrypt decrypt code here

def getToken():
    pass

def authenticate(token):
    pass
"""

# env file
def env():
    return """# environment varibales here
DATABASE=<dbname>
DBUSER=<dbusername>
PASSWORD=<db password>
HOST=<db host>
PORT=<db port>
"""

# config file
def config():
    return """from pydantic_settings import BaseSettings, SettingsConfigDict
    
# env variable access code here
class Secret(BaseSettings):
    database: str
    dbuser: str
    password: str
    host: str
    port: str
    
    model_config= SettingsConfigDict(env_file=".env")
    
secret= Secret()

"""

#db file
def db():
    return"""from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import secret

# database connection code here
"""
#model file
def model():
    return"""from sqlalchemy import Column, Integer, String, Float
from settings.db import Base

# model code here
"""
#schema file
def schema():
    return """from pydantic import BaseModel

# schema code here
class Sample(BaseModel):
    pass
"""
#api file
def api():
    return """from fastapi import APIRouter

# api code here
app= APIRouter(
    prefix="/api/v1",
    tags=["api"]
)
@app.get('/')
def initial():
    return {"message": "Serive from API routes"}
"""

def getFileData(name, venv):
    return {
            'auth.py': auth(),
            'config.py': config(),
            'db.py': db(),
            'model.py': model(),
            'schema.py': schema(),
            'api.py': api(),
            'main.py': main(name), 
            '.gitignore':gitignore(venv),
            '.env':env()
            }

