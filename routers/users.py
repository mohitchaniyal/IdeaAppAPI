
import schemas,models,utils
from typing import List
from fastapi import Response,status,HTTPException,Depends,APIRouter
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/ideaapp/api/v1/users",tags=['users'])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UsersResp)
def create_user(user:schemas.Users,db: Session = Depends(get_db)):
    #hash the password
    user_valid = db.query(models.User).filter(models.User.email==user.email)
    # print(user_valid)
    # if user_valid :
    #     return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Email alredy registered.")
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UsersResp)
def get_user(id:int,db: Session = Depends(get_db)):
    user_=db.query(models.User).filter(models.User.id==id).first()
    if not user_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User Not Found {id}")
    return user_