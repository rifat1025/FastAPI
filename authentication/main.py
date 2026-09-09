from fastapi import FastAPI,Depends,HTTPException,status
from database import Base, get_db, engine
from .model import User
from sqlalchemy.orm import Session
from .validation import UserCreate,UserResponse,UserLogin
from authentication.jwt_handler import (
        create_access_token

            )

from authentication.hashing import (
        get_hashed_password,verify_password )  

Base.metadata.create_all(bind=engine)

app= FastAPI ()

@app.post('/register')
def user_register (user:UserCreate, db:Session=Depends(get_db)):

    new_user = User(
        username =user.username,
        email = user.email,
        hashed_password =get_hashed_password(user.password) 

    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return new_user

@app.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(
            User.email ==
            user.email
        )
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    access_token = (
        create_access_token(
            {
                "sub":
                db_user.email,
                "user_id":
                db_user.id
            }
        )
    )

    return {
        "access_token":
        access_token,
        "token_type":
    }
    