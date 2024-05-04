
import schemas,models,oauth2
from typing import List,Optional
from fastapi import Response,status,HTTPException,Depends,APIRouter
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_

router = APIRouter(prefix="/ideaapp/api/v1/likes",tags=["likes"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_like(like:schemas.Like,db: Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)):
    idea = db.query(models.Idea).filter(models.Idea.id == like.idea_id, models.Idea.public == True).first()
    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Idea {like.idea_id} Not Found")
    like_query=db.query(models.Like).filter(models.Like.idea_id==like.idea_id,models.Like.user_id==user_data.id)
    alredy_liked = like_query.first()
    if like.dir==1:
        if alredy_liked:
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Already Liked The Post")
        new_like=models.Like(user_id=user_data.id,idea_id=like.idea_id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
    elif like.dir==0 :
        if not alredy_liked:
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Alredy UnLiked The Post")
        like_query.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)