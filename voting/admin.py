from django.contrib import admin
from .views import vote
from .models import Users,Candidate, VotingSession, VoteUser

# Register your models here.
admin.site.register(Users)
admin.site.register(Candidate)
admin.site.register(VotingSession)
admin.site.register(VoteUser)
#admin.site.register()
#x=vote(candidate_id,voting_session_id)
   