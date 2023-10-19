from fastapi import FastAPI,Depends,Body
from schemas import *
from jwt_handler import signJWT
from jwt_bearer import JWTBearer


app = FastAPI()

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to your blog!"}


posts = []

users = []

@app.get("/posts")
def get_posts():
    return { "data": posts }


@app.get("/posts/{id}")
def get_single_post(id: int):
    if id > len(posts):
        return {
            "error": "No such post with the provided ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }
            
# @app.post("/posts/add")
# def add_post(post: PostSchema):
#     post.id = len(posts) + 1
#     posts.append(post.dict())
#     return {
#         "data": "post added."
#     }
@app.post("/posts/add")
def add_post(post: PostSchema):
    new_post = post
    print(new_post,111111111111)
    posts.append(new_post)
    return new_post

    
@app.post("/user/signup", tags=["user"])
def create_user(user: UserSignupSchema):
    users.append(user)
    return signJWT(user.email)    
def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(post: PostSchema):
    new_post = post
    new_post.id = len(posts) + 1
    posts.append(new_post)
    return posts