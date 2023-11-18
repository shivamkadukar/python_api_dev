from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


posts = [
    {"title": "shivam", "content": "kadukar", "id": 1},
    {"title": "kartik", "content": "kadukar", "id": 2},
]


def get_specific_post(id):
    for post in posts:
        if post["id"] == id:
            return post


def delete_specific_post(id):
    for i, post in enumerate(posts):
        if post["id"] == id:
            return posts.pop(i)
    return None


def update_specific_post(id, updated_post):
    for i, post in enumerate(posts):
        if post["id"] == id:
            posts[i] = updated_post.dict()
            return i
    return None


@app.get("/")
def root():
    return {"message": "Hello welcom to hell"}


@app.get("/posts")
def get_posts():
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    created_post = new_post.dict()
    created_post["id"] = randrange(0, 10000000)
    posts.append(created_post)
    return {"data": created_post}


@app.get("/posts/latest")
def get_latest_post():
    return {"data": posts[-1]}


@app.get("/posts/{id}")
def get_post(id: int):  # response: Response):
    post = get_specific_post(id)
    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"alert": f"post with {id} not found"}
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted_post = delete_specific_post(id)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    # return {"data": deleted_post}
    # api standard practice - when you delete something dont send any data back
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    updated_post_index = update_specific_post(id, post)
    if not updated_post_index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    return {"data": post.dict()}


# @app.post("/create_post")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f'title - {payload["title"]}, content - {payload["content"]}'}
