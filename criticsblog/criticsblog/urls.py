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
from authentication.views import subscribe_page, follow_user_page, unfollow_user_page
from litreview.views import newticket_page, newreview_page
from litreview.views import create_ticket_and_review_page
from litreview.views import edit_ticket, delete_ticket, edit_review
from litreview.views import feed, delete_review
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_page, name='signup'),
    path("login/", login_page, name="login"),
    path('', home, name='home'),
    path('logout/', logout_user, name='logout'),
    # page principale abonnements
    path('subscribe/', subscribe_page, name='subscribe'),

    # suivre / se désabonner
    path('follow_user/<int:user_id>/', follow_user_page, name='followuser'),
    path('unfollow_user/<int:user_id>/', unfollow_user_page, name='unfollowuser'),
    path('feed/', feed, name='feed'),
    path('ticket/newticket/<int:ticket_id>', newticket_page, name='newticket'),
    path('ticket/newticket/', newticket_page, name='newticket'),
    path('review/newreview/<int:ticket_id>', newreview_page, name='newreview'),
    path('review/ticketreview/', create_ticket_and_review_page, name='ticketreview'),
    path('ticket/edit/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    path('ticket/delete/<int:ticket_id>/', delete_ticket, name='delete_ticket'),

    path('review/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', delete_review, name='delete_review'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
