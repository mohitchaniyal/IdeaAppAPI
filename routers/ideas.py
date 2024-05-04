
import os
import sys
# script_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.path.dirname(script_dir))
import schemas,models,oauth2
from typing import List,Optional
from fastapi import Response,status,HTTPException,Depends,APIRouter
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_,func

router = APIRouter(prefix="/ideaapp/api/v1/ideas",tags=["ideas"])

@router.get("/",response_model=List[schemas.IdeaRespOut])
def get_ideas(db: Session = Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]=""):
    ideas = db.query(models.Idea).filter(models.Idea.public==True,models.Idea.idea_name.contains(search)).limit(limit).offset(skip).all()
    if ideas==[]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Data Available")
    result = db.query(models.Idea,func.count(models.Like.idea_id).label("likes")).join(models.Like,models.Idea.id==models.Like.idea_id,isouter=True).group_by(models.Idea.id).all()
    print(result)
    return result

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.IdeaResp)
def create_idea(idea:schemas.CreateIdea,db: Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)):
    new_idea = models.Idea(owner_id=user_data.id,**idea.model_dump())
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    return new_idea

@router.get("/{id}",response_model=schemas.IdeaResp)
def get_idea(id:int,db: Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)):
    idea = db.query(models.Idea).filter(models.Idea.id == id, or_(models.Idea.owner_id == user_data.id, models.Idea.public == True)).first()

    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Idea {id} Not Found")
    return idea 


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_idea(id:int,db: Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)):
    idea = db.query(models.Idea).filter(models.Idea.id==id,models.Idea.owner_id==user_data.id)
    
    if idea.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Idea {id} Not Found")

    idea.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_idea(id:int,idea:schemas.CreateIdea,db: Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)):
    idea_q = db.query(models.Idea).filter(models.Idea.id==id,models.Idea.owner_id==user_data.id)
    
    if idea_q.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post {id} Not Found")
    idea_q.update(idea.model_dump())
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)