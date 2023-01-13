from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime

class Membre(models.Model):
    id= fields.IntField(pk =True, index=True)
    name=fields.CharField(max_length=200)
    email=fields.CharField(max_length=200, null=False, unique=True)
    num_tel=fields.CharField(max_length=20, null=False, unique=True)
    adresse_phis=fields.CharField(max_length=200, null=False, unique=True)
    join_time=fields.DatetimeField(default=datetime.utcnow)

class Comment(models.Model):
    id= fields.IntField(pk =True, index=True)
    comment=fields.CharField(max_length=200)
    publication=fields.ForeignKeyField("models.Publication", related_name="Comment")
    time=fields.DatetimeField(default=datetime.utcnow)


class Artiste(models.Model):
    id= fields.IntField(pk =True, index=True)
    name=fields.CharField(max_length=200, null=False, unique=True)
    description=fields.TextField()

class Publication(models.Model):
    id= fields.IntField(pk =True, index=True)
    pub_descrition=fields.CharField(max_length=300, null=False, unique=True)
    likes=fields.IntField()
    post_time=fields.DatetimeField(default=datetime.utcnow)



membre_pydantic=pydantic_model_creator(Membre, name="Membre")
membreIn_pydantic=pydantic_model_creator(Membre, name="MembreIn", exclude="join_time", exclude_readonly=True)


comment_pydantic = pydantic_model_creator(Membre, name="Membre")
commentIn_pydantic = pydantic_model_creator(Membre, name="MembreIn", exclude="time", exclude_readonly=True)

artiste_pydantic=pydantic_model_creator(Artiste, name="Artiste")
artisteIn_pydantic=pydantic_model_creator(Artiste, name="ArtisteIn", exclude="id")

publication_pydantic=pydantic_model_creator(Publication, name="Publication", exclude="id")
publicationIn_pydantic=pydantic_model_creator(Publication, name="PublicationIn", exclude_readonly=True)
