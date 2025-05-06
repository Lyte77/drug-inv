from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard_view,name='dashboard'),
    path('drugs/', drugs_view,name='drugs'),
    
    path('add-drug/', add_drug,name='add-drug'),
    path('drug/<int:pk>/edit', edit_drug,name='edit-drug'),
    path('drug/<int:pk>/delete/', delete_drug,name='delete-drug'),
    
    # path('signup/', signup, name='signup'),


]
