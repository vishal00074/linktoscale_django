from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path
from polls import views 

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # admin URL_______________________________________________________________________________________
    # path('', admin.site.urls),
    # path('logout/', RedirectView.as_view(url = '') , name="logout"),
    
    path('', views.admin_login, name="admin"),
    path('logout/',views.admin_logout, name="admin_logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('index/', views.ad_index, name="admin_index"),
    path('index/add/', views.ad_index_add, name="admin_index_add"),
    path('index/edit/<int:id>/', views.ad_index_edit, name="admin_index_edit"),
    path('index/delete/<int:id>/', views.ad_index_delete, name="admin_index_delete"),
    path('category/<int:id>/', views.ad_category, name="admin_category"),
    path('category/add/<int:id>/', views.ad_category_add, name="admin_category_add"),
    path('category/edit/<int:id>/', views.ad_category_edit, name="admin_category_edit"),
    path('category/delete/<int:id>', views.ad_category_delete, name="admin_category_delete"),
    
    path('user/', views.admin_user, name="admin_user"),
    path('user/add/', views.admin_user_add, name="admin_user_add"),
    path('user/<int:id>/', views.viewproperties, name="viewproperties"),
    
    path('activate/<int:id>/',views.activate, name="activate" ),
    path('deactivate/<int:id>/',views.deactivate, name="deactivate" ),

    path('properties/', views.properties, name="properties"),
    path('adminproperty/', views.adminproperty, name="adminproperty"),
    path('registeredUser/', views.registeredUser, name='registeredUser'),
    path('edit_user/<int:id>/', views.edit_user, name="edit_user"),
    path('update_user/<int:id>/', views.update_user, name="update_user"),
    path('delete_user/<int:id>/',views.delete_user, name='delete_user'),
    path('view_property/<int:id>/', views.view_property, name='view_property'),
    path('add-user/', views.AddUser, name='add_user'),
    path('ajax-adduser/', views.ajaxadduser, name='ajax-adduser'),
    path('database/', views.Database, name='database'),
    path('database_edit/<int:id>/', views.db_edit, name='db_edit'),
    path('database_update/<int:id>/', views.db_update, name='db_update'),
    path('rating/', views.rating, name='rating'),
    path('rating_edit/<int:id>/', views.rating_edit, name = "rating_edit"),
    path('add_rating', views.add_rating, name="add_rating"),
    path('new_rating', views.new_rating, name="new_rating"),
    path('add_new_rating', views.add_new_rating, name="add_new_rating"),
    path('property_view', views.property_view, name="property_view"),
    path('view_all_rating/<int:id>/', views.view_all_rating, name="view_all_rating"),
    path('indexes', views.Index, name="indexes"),
    path('percentile', views.Percentile, name="percentile"),
   
   
   
    path('approve/<int:id>/', views.approve, name='approve'),
    path('unapprove/<int:id>/', views.unapprove, name='unapprove'),
    path('update_special/', views.update_special, name='update_special'),
    path('delete_property/<int:id>/', views.delete_property, name='delete_property'),

    #________________________________SubAdminRoute_____________________________

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)