from django.contrib.auth.models import User
from django.db.models import *
from django.db import models
from django.contrib import admin
from users.models import User
class Users(Model):
    firstname=CharField(max_length=100)
    lastname=CharField(max_length=100)
    image=models.ImageField()
    
        
    
    
class Candidate(Model):
    name = CharField(max_length=100)
    description = TextField()
    image = models.ImageField(upload_to='candidate_pics')
    
class VotingSession(Model):
    name = CharField(max_length=100)
    active = models.BooleanField(default=True)
    year = IntegerField()
    country = CharField(max_length=100)
    image = models.ImageField(upload_to='voting_pics')
    candidates = models.ManyToManyField('Candidate', related_name='candidates')


class VoteUser(Model):
    voting_session = models.ForeignKey('VotingSession', on_delete=models.CASCADE)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
    
