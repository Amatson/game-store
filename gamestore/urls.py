"""game_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', views.register_view),
    url(r'^register/activate/(\w+)/$', views.activate_view),
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^account/$', views.account),
    url(r'^account/sales/([0-9]+)/$', views.sales),
    url(r'^game/([0-9]+)/$', views.gameplay, name='gameplay'),
    url(r'^$', views.gamelist, name='index'),
    url(r'^gamelist/$', views.gamelist, name='gamelist'),
    url(r'^addgame/$', views.add_game, name='addgame'),
    url(r'^buygame/([0-9]+)/$', views.buy_game, name='buygame'),
    url(r'^payment/success/$', views.payment_successful, name='payment_successful'),
    url(r'^payment/cancel/$', views.payment_cancel, name='payment_cancel'),
    url(r'^payment/error/$', views.payment_error, name='payment_error'),
    url(r'^highscores/([0-9]+)/$', views.high_scores),
    url(r'^account/edit/name/$', views.edit_name),
    url(r'^account/edit/password/$', views.edit_password),
    url(r'^account/edit/game/([0-9]+)$', views.edit_game),
    url(r'^rest/$', views.rest_info),
    url(r'^rest/highscores/$', views.rest_high_scores),
    url(r'^rest/sales/$', views.rest_sales),
    url(r'^rest/games/$', views.rest_games),
]
