from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.typing import Optional
import random

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
            {"title": "title of post 1", "content": "content of post 1", "id": 0},
            {"title": "fav foods", "content": "pizza", "id": 1}
            ]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


@app.get("/")
async def root():
    return {'message': "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post = new_post.dict()
    post["id"] = random.randrange(0, 99999999)
    my_posts.append(post)
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for i in range(len(my_posts)):
        if my_posts[i]['id'] == int(id):
            my_posts.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} was not found')


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, new_post: Post):
    new_post = new_post.dict()
    for i in range(len(my_posts)):
        if my_posts[i]['id'] == int(id):
            my_posts[i]['title'] = new_post['title']
            my_posts[i]['content'] = new_post['content']
            return {"message": f"Post with id {id} was successfully updated"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")