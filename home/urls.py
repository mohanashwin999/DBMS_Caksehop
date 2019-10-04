from django.contrib import admin
from django.urls import path,include
from . import views

app_name='home'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('cakes/',views.cakes,name='cakes'),
    path('logout/',views.logout,name='logout'),
    path('weight/',views.weight,name='weight'),
    path('orders/',views.orders,name='orders'),
    path('',views.landingpage,name='landingpage'),
    path('home/',views.landingpage2,name='landingpage2'),
    path('orderconf/',views.orderconf,name='orderconf'),
    path('feedback/',views.feedback1,name='feedback'),
    path('profile/',views.profile,name='profile'),
    path('update/',views.update,name='update'),
    path('delete/',views.delete,name='delete'),
]
