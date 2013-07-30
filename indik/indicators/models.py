from django.db import models

# Create your models here.

from mongoengine import *

#TODO: load from settings
connect('indik')


class IndicatorDescriptor(Document):
	name = StringField(max_length=300, required=True)
	code = StringField(max_length=10, required=True, unique=True)



class IndicatorData(DynamicDocument):
    pass







