from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'Index'),
    path('add/member', views.add_member, name = 'Add Member'),
    path('show/members', views.show_members, name = 'Show Members'),
    path('show/member/<str:id>', views.show_member, name = 'Show Member with id'),
    path('add/activity_period/<str:id>', views.add_activity_period, name = 'Add Activity Period'),
    path('update/member/<str:id>', views.update_member, name = 'Update Member with id'),
    path('delete/member/<str:id>', views.delete_member, name = 'Delete Member with id'),
]
