from fastapi import FastAPI,Depends
from database import Base, get_db, engine
from .model import User
from sqlalchemy.orm import Session
from .validation import UserCreate,UserResponse

Base.metadata.create_all(bind=engine)

app= FastAPI ()

@app.post('/register')
def user_register (user:UserCreate, db:Session=Depends(get_db)):

    new_user = User(
        username =user.username,
        email = user.email,
        hashed_password = user.password

    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return new_user


    