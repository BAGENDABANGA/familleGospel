from fastapi import FastAPI, HTTPException, File, UploadFile
from models import*
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel



app=FastAPI()

class Message(BaseModel):
    message: str


@app.get("/")
async def index():
    return {"INDEX":"Famille Gospel API"}

#upload files

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

#les methodes REST pour la gestion des membres

@app.post("/membre", response_model=membre_pydantic)
async def create(membre: membreIn_pydantic):
    obj=await Membre.create(**membre.dict(exclude_unset=True))
    return await membre_pydantic.from_tortoise_orm(obj)

@app.get("/membre/{id}", response_model=membre_pydantic, responses={404:{"model": HTTPNotFoundError}})
async def get_one(id:int):
    return await membre_pydantic.from_queryset_single(Membre.get(id=id))


@app.put("/membre/{id}", response_model=membre_pydantic, responses={404:{"model":HTTPNotFoundError}})
async def update_membre(id:int, membre:membreIn_pydantic):
    await Membre.filter(id=id).update(**membre.dict())
    return await membre_pydantic.from_queryset_single(Membre.get(id=id))

@app.delete("/membre/{id}", response_model=Message, responses={404:{"model":HTTPNotFoundError}})
async def delete_membre(id:int):
    delete_obj= await Membre.filter(id=id).delete()
    if not delete_obj:
        raise HTTPException(status_code=404, detail="This membre dosen't exist")
    return Message(message="Successfuly deleted")


#les methodes REST pour la gestion des publications

@app.post("/pub", response_model=publication_pydantic)
async def create_PUBLICATION(pub: publicationIn_pydantic, data: UploadFile):
    obj=await Publication.create(**pub.dict(exclude_unset=True, exclude="likes"))
    return await publication_pydantic.from_tortoise_orm(obj)

@app.get("/pub/{id}", response_model=publication_pydantic, responses={404:{"model": HTTPNotFoundError}})
async def get_PUBLICATION(id:int):
    return await publication_pydantic.from_queryset_single(Publication.get(id=id))


@app.put("/pub/{id}", response_model=publication_pydantic, responses={404:{"model":HTTPNotFoundError}})
async def update_PUBLICATION(id:int, pub:publicationIn_pydantic):
    await Publication.filter(id=id).update(**pub.dict())
    return await publication_pydantic.from_queryset_single(Publication.get(id=id))

@app.delete("/pub/{id}", response_model=Message, responses={404:{"model":HTTPNotFoundError}})
async def delete_PUBLICATION(id:int):
    delete_obj= await Publication.filter(id=id)
    if not delete_obj:
        raise HTTPException(status_code=404, detail="This pub dosen't exist")
    return Message(message="Successfuly deleted")

#les methodes REST pour la gestion des commentaires

@app.post("/comment", response_model=comment_pydantic)
async def post_comment(comment: commentIn_pydantic):
    obj=await Comment.create(**comment.dict(exclude_unset=True))
    return await comment_pydantic.from_tortoise_orm(obj)

@app.get("/pub/{id}", response_model=comment_pydantic, responses={404:{"model": HTTPNotFoundError}})
async def get_comment(id:int):
    return await comment_pydantic.from_queryset_single(Publication.get(id=id))

@app.put("/comment/{id}", response_model=comment_pydantic, responses={404:{"model":HTTPNotFoundError}})
async def update_comment(id:int, comment:commentIn_pydantic):
    await Comment.filter(id=id).update(**comment.dict())
    return await comment_pydantic.from_queryset_single(Comment.get(id=id))

@app.delete("/comment/{id}", response_model=Message, responses={404:{"model":HTTPNotFoundError}})
async def delete_comment(id:int):
    delete_obj= await Comment.filter(id=id)
    if not delete_obj:
        raise HTTPException(status_code=404, detail="This comment dosen't exist")
    return Message(message="Successfuly deleted")


#les methodes REST por la gestion des artistes


@app.post("/artiste", response_model=artiste_pydantic)
async def create_artiste(artiste: artisteIn_pydantic, file: UploadFile):
    obj=await Artiste.create(**artiste.dict(exclude_unset=True))
    return await artiste_pydantic.from_tortoise_orm(obj)

@app.get("/artiste/{id}", response_model=artiste_pydantic, responses={404:{"model": HTTPNotFoundError}})
async def get_artiste(id:int):
    return await artiste_pydantic.from_queryset_single(Artiste.get(id=id))


@app.put("/artiste/{id}", response_model=artiste_pydantic, responses={404:{"model":HTTPNotFoundError}})
async def update_artiste(id:int, artiste:artisteIn_pydantic):
    await Artiste.filter(id=id).update(**artiste.dict())
    return await artiste_pydantic.from_queryset_single(Artiste.get(id=id))

@app.delete("/artiste/{id}", response_model=Message, responses={404:{"model":HTTPNotFoundError}})
async def delete_artiste(id:int):
    delete_obj= await Artiste.filter(id=id)
    if not delete_obj:
        raise HTTPException(status_code=404, detail="This artist dosen't exist")
    return Message(message="Successfuly deleted")




register_tortoise(
    app,
    db_url="sqlite://gospellff.db",
    modules={'models':['models']},
    generate_schemas=True,
    add_exception_handlers=True
)