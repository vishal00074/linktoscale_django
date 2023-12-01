"""link2scale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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


from django.urls import include, path
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth
from .views import home, index, activate


urlpatterns = [
    # admin URL=========================================================================================================
    path('admin/', include('polls.urls')),
    

    # frontend URL=====================================================================================================
    path('contact/',views.contact,name='contact-form'),
    path('category/<int:sts_id>/', views.category_view, name='category'),
    path('',views.home, name=''),
    path('how_it_works/', views.how_it_works, name='how_it_works'),
    path('help/',views.help, name='help'),
    path('settings/',views.settings, name='settings'),
    path('upload/',views.upload, name='upload'),
    path('property/',views.property, name='property'),
    path('vehicles/',views.vehicles, name='vehicles'),
    path('residential/',views.residential, name='residential'),
    path('sub-category/',views.subcategory, name='sub-category'),
    path('Addproperty/', views.Addproperty, name='Addproperty'),
    path('login/', views.userlogin, name='userlogin'),
    path('signup/', views.signup, name='signup'),
    path("register_request/", views.register_request, name="register_request"),
    path('login_request/', views.login_request, name="login_request"),
    path('activate/', views.activate, name='activate'),  
    path('email_registration', views.email_registration, name='email_registration'),
    path('upload_property', views.UploadProperty, name='upload_property'),
    path('get_city/', views.get_city, name='get_city'),
    path('thankyou/', views.thankyou, name='submit'),
    path('get_data/', views.GetData, name='get_data'),
    path('multiple/', views.multiple, name='multiple'),
    path('get_cities_by_country/', views.get_cities_by_country, name='get_cities_by_country'),
    path('cities/', views.cities, name='cities'),
  
  
   

    
    
    # path('filter-data/', views.filterprperty, name="filter-data"),
    
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)