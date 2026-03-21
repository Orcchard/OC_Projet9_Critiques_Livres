"""
URL configuration for criticsblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication.views import signup_page, login_page, home, logout_user
from litreview.views import newticket_page, newreview_page
from litreview.views import ticket_list_page, review_list_page
from litreview.views import create_ticket_and_review_page
from litreview.views import follow_user_page, suscribe_page, unfollow_user_page
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_page, name='signup'),
    path("login/", login_page, name="login"),
    path('', home, name='home'),
    path('logout/', logout_user, name='logout'),
    # page principale abonnements
    path('suscribe/', suscribe_page, name='suscribe'),

    # suivre / se désabonner
    path('follow/<int:user_id>/', follow_user_page, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user_page, name='unfollow_user'),
    path('ticket/newticket/<int:ticket_id>', newticket_page, name='newticket'),
    path('ticket/newticket/', newticket_page, name='newticket'),
    path('review/newreview/<int:ticket_id>', newreview_page, name='newreview'),
    path('review/ticketreview/', create_ticket_and_review_page, name='ticketreview'),
    path('ticket/ticketlist/', ticket_list_page, name='ticketlist'),
    path('review/reviewlist/', review_list_page, name='reviewlist'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
