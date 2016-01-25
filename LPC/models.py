#coding:utf-8
import json
from django.db import models

# Create your models here.
from mongoengine import Document, StringField, DateTimeField, DictField, ListField, FloatField, IntField, ReferenceField


# class TestModel(Document):
#     test_key=StringField(required=True)
#     test_value=StringField(max_length=50)



class instances(models.Model):
    deleted=models.CharField(max_length=1)
    uuid=models.CharField(max_length=50)
    user_id=models.CharField(max_length=50)
    project_id=models.CharField(max_length=50)
    display_name=models.CharField(max_length=50)
    class Meta:
        db_table = "instances"

class project(models.Model):
    id = models.CharField(primary_key = True, db_column="ID",max_length=50)
    name=models.CharField(max_length=50)
    enabled=models.CharField(max_length=50)
    domain_id=models.CharField(max_length=50)
    class Meta:
        db_table = "project"

class volumes(models.Model):
    id = models.CharField(primary_key = True, db_column="ID",max_length=50)
    instance_uuid=models.CharField(max_length=50)
    project_id=models.CharField(max_length=50)
    deleted=models.CharField(max_length=1)
    class Meta:
        db_table = "volumes"
