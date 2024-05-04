from pydantic import BaseModel,Field,EmailStr
from typing import Optional

class Users(BaseModel):
    email: EmailStr
    password: str

class UsersResp(BaseModel):
    id :int 
    email: EmailStr
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Idea(BaseModel):
    # id:int
    idea_name:str
    idea_disc:str
    idea_author:str
    public:Optional[bool] = False
    

class CreateIdea(Idea):
    # id:int
    idea_name:str
    idea_disc:str
    idea_author:str
    public:Optional[bool] = False
    # owner_id:int

class IdeaResp(Idea):
    id:int
    owner_id:int 
    owner:UsersResp
    class Config:
        from_attributes = True

class IdeaRespOut(Idea):
    Idea:Idea
    likes:int

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int]=None

class Like(BaseModel):
    idea_id:int
    # user_id:int
    dir:int = Field(...,isin=(1,2))
# class UpdateIdea(BaseModel):
#     # id:int
#     idea_name:Optional[str] = None
#     idea_disc:Optional[str] = None
#     idea_author:Optional[str] = None
#     public:Optional[bool] = False