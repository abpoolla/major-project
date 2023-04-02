from django.urls import path
from django.contrib import admin

from voting import views
from .views import GeneratePdf


urlpatterns = [
    path("vote/<int:pk>/", views.votedash, name='votedash'),
    path("vote/<int:candidate_id>/<int:voting_session_id>/", views.vote, name='vote'),
    path('vote/', views.dashboard, name='dashboard'),
    path('results/', views.results_dashboard, name='results_dashboard'),
    path('results/<int:pk>/', views.results_detail, name='results_detail'),
    path('status/', views.status ,name='status'),
    path('pdf/', views.GeneratePdf.as_view()),
    path('admin/' ,views.admin_page,name='admin'),
    path('admin/', admin.site.urls),
    path('status1/',views.status1,name='status1'),
    path('admin2/',views.admin2,name='admin2')
    #path('change-background-color/', views.change_background_color, name='change-background-color'),

]