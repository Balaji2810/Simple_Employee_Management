from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'Index'),
    path('add/member', views.add_member, name = 'Add Member'),
    path('show/members', views.show_members, name = 'Show Members'),
    path('show/members/<str:id>', views.show_member, name = 'Show Member with id'),
    path('add/activity_period/<str:id>', views.add_activity_period, name = 'Add Activity Period'),
]
