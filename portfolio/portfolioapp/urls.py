from django.urls import path
from .views import signupfunc, Home, Ideas_list, opinion, main_list, goodfunc, branchfunc, detailfunc, myfunc, Edit, Idea_edit, Delete

app_name = 'portfolioapp'


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('signup/', signupfunc, name='signup'),
    path('ideas_list/', Ideas_list.as_view(), name='ideas_list'),
    path('opinion/<int:pk>', opinion, name='opinion'),
    path('main_list/<int:pk>', main_list, name='main_list'),
    path('good/<int:pk>', goodfunc, name='good'),
    path('branch/<int:pk>', branchfunc, name='branch'),
    path('detail/<int:pk>', detailfunc, name='detail'),
    path('my_page/', myfunc, name='my_page'),
    path('edit/<int:pk>', Edit.as_view(), name='edit'),
    path('idea_edit/<int:pk>', Idea_edit.as_view(), name='idea_edit'),
    path('delete/<int:pk>', Delete.as_view(), name='delte'),
]
