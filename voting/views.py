import base64
from django.http import HttpResponse
from django.views.generic import View
#from .process import html_to_pdf 
#from voting.templates import admin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from voting.models import VotingSession, VoteUser, Candidate
from .forms import ContactForm,Status
import face_recognition 
from users.forms import UserRegisterForm
from django.contrib.auth.models import User
from .models import Users
from django.contrib.auth.hashers import check_password,make_password


def status1(request):
    os1=User.objects.all()
    us=VoteUser.objects.all()
    x=""
    l1=[]
    for i in us:
            print(i.user)
            l1.append(i.user)
    
        
            
    return render(request,'status1.html',{'l1':l1})

def dashboard(request):
    return render(request, 'dashboard.html', {'dashboard': VotingSession.objects.filter(active=True)})


@login_required        
def results_dashboard(request):
    return render(request, 'results.html', {
        'active_sessions': VotingSession.objects.filter(active=True),
        'inactive_sessions': VotingSession.objects.filter(active=False)
    })


@login_required
def votedash(request, pk):
    return render(request, 'votedash.html', {'voting': get_object_or_404(VotingSession, pk=pk)})


def results_detail(request, pk):
    voting_session = get_object_or_404(VotingSession, pk=pk)
    labels, data = generate_statistics_and_context(voting_session)
    labels_chart, data_chart = str(labels).replace("'", '"'), str(data).replace("'", '"')

    return render(request, 'results_detail.html', {
        'voting_session': voting_session,
        'labels': labels,
        'data': data,
        'labels_chart': labels_chart,
        'data_chart': data_chart
    })

@login_required
def about_page(request):
    return render(request, 'about.html', {})
g1=""
@login_required

def admin_page(request):
   
    users = User.objects.all()
    check=len(users)
    #s=vote(request,candidate_id=)
    us=VoteUser.objects.all()
    #print(us)
    a=[]
    l1=[]
    
    for i in us:
        l1.append(i.user)
    for i in users:
        a.append(i)
    n=len(l1)
    #print(l1)
    gettext=""
    g1=""
    if request.method=="POST":
        gettext=request.POST.get('te1',None)
        print(type(gettext),gettext)
        gettext=int(gettext)
        print(type(gettext))
        g1=a[gettext-1]
        print(g1)
        return render(request,'admin2.html',{'users':users,'us':us,"g1":g1,'l1':l1})
        
    return render(request,'admin.html',{'users':users,'us':us,'l1':l1,'g1':g1,'check':check,'n':n})
def admin2(request):
    
    l1=[]
    users=User.objects.all()
    us=VoteUser.objects.all()
    for i in us:
        l1.append(i.user)
    a=[i for i in users]
    return render(request,'admin2.html',{'users':users,'l1':l1,'us':us})
        
        
        
    
        
    return render(request, 'admin.html', {'users':users,'check':check,'l1':l1,'a':a})

@login_required
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = "{0} has sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['message'])
            to=['ananthabalucm023@gmail.com','20l35a0507@gmail.com','20l35a0507@vignaniit.edu.in']

            msg=EmailMultiAlternatives('Support Request', message,sender_email, to)
            msg.send()
            print([settings.EMAIL_HOST_USER])
            messages.success(request,f'The message has been sent! We will contact you shortly.')

            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
@login_required
def status(request):
    if request.method=="POST":
        us=VoteUser.objects.all()
        s_form=Status(request.POST)
        form=ContactForm()
        if s_form.is_valid() :
            x=s_form.cleaned_data['password']
            x1=check_password(x, request.user.password)
            x=make_password(x)
            
            if x1==True:
                l1=[]
                for i in us:
                    print(i.user)
                    l1.append(i.user)
                return render(request,'status1.html',{'l1':l1})
                
                #return render(request,'status1.html',{})
            
                
    else:
        s_form=Status()
    return render(request,'status.html',{'s_form':s_form})

        
    
        
    
        
l=[]
def vote(request, candidate_id, voting_session_id):
    user = request.user.username 
    st=False
    can_vote = face_recog(settings.MEDIA_ROOT + '/webcamimages/' + user + '.jpg',
                          request.user.profile.image.url[1:len(request.user.profile.image.url)]) 
    print(can_vote,"canvote")
    if settings.GLOBAL_SETTINGS.get('default_image') in request.user.profile.image.path:
        return redirect('profile')
    elif not can_vote:
        messages.warning(request, f"The vote is not valid")
   
    else:
        candidate = Candidate.objects.get(pk=candidate_id)
        voting_session = VotingSession.objects.get(pk=voting_session_id)
        rows = VoteUser.objects.filter(voting_session=voting_session, user=request.user)

        if rows.count() == 0:
            
            user_vote = VoteUser(candidate=candidate, voting_session=voting_session, user=request.user)
            user_vote.save()
            
            messages.success(request, f'Your vote has been registered successfully!')
            
            
            
        else:
            messages.warning(request, f'Your already voted in this election!')

    return redirect(reverse('votedash', kwargs={'pk': voting_session_id}))
    

u=""
def generate_statistics_and_context(voting_session):
    labels, data ,u= [], [],""
    votes = VoteUser.objects.all().filter(voting_session=voting_session)
    
    for candidate in voting_session.candidates.all():
        labels.append(candidate.name)
        data.append(len(list(filter(lambda c: c.candidate_id == candidate.pk, votes))))
        for i in votes:
            print(i.user)
        
    return labels, data


def face_recog(webcam_photo, user_photo):
 

    picture_of_me = face_recognition.load_image_file(user_photo)
    my_face_encoding, unknown_face_encoding = [], []
    
    if face_recognition.face_encodings(picture_of_me):
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
        
    else:
        return False
    # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

    unknown_picture = face_recognition.load_image_file(webcam_photo)
    print(unknown_picture,'picture')
    if face_recognition.face_encodings(unknown_picture):
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
        
    else:
        return False

    # Now we can see the two face encodings are of the same person with `compare_faces`!

    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
    print(results)
    return results[0]


@csrf_exempt
def save_image(request):
    imgstr = request.POST['mydata']
    voting_session_id = request.POST['voting_session']
    user = request.user.username
    
    if request.POST:
        f = open(settings.MEDIA_ROOT + '/webcamimages/' + user + '.jpg', 'wb')
        f.write(base64.b64decode(imgstr))
        f.close()

    messages.success(request, f'A picture of your face has been saved in the database!')

    return redirect(reverse('votedash', kwargs={'pk': voting_session_id}))

#Creating a class based view
from django.http import HttpResponse
from django.views.generic import View

#importing get_template from loader
from django.template.loader import get_template

#import render_to_pdf from util.py 
from .process import render_to_pdf 

#Creating our view, it is a class based view
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        
        #getting the template
        pdf = render_to_pdf('invoice.html')
         
         #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')