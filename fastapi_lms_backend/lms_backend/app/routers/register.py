import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.book import User as UserSchema, UserDisplay, Token
from app.database.session import get_db
from app.models.book import User, UserRole
from fastapi.security import OAuth2PasswordRequestForm
from app.utils import (create_access_token, pwd_context, verify_password,
                       oauth2_scheme, project_root, verify_token)
import json
from datetime import datetime

router = APIRouter()

saved_dir = os.path.join(project_root, "revoked_tokens")
revoked_tokens_file = os.path.join(saved_dir, 'revoked_tokens.json')


@router.post('/signup', response_model=UserDisplay)
def register_user(user: UserSchema, db: Session = Depends(get_db)):
    if user.role not in [role.value for role in UserRole]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid user role')

    hashed_pwd = pwd_context.hash(user.password)
    new_user = User(username=user.username.lower(),
                    role=user.role.lower(), password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User {form_data.username} does not exist')
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def save_revoked_token(token: str):
    date_key = datetime.now().strftime('%Y-%m-%d')
    new_entry = {date_key: token}

    with open(revoked_tokens_file, 'a') as file:
        file.write(json.dumps(new_entry) + "\n")


@router.post('/logout')
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    save_revoked_token(token)
    return {"message": "Logout successful"}


# @router.post('/refresh-token', response_model=Token)
# def refresh_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     # Verify the refresh token
#     username = verify_token(token)  # This will raise an exception if the token is invalid or expired
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="User not found")

#     # Generate a new access token
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}