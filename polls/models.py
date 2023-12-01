from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

# Create your models here.

class Customer(models.Model):
  name = models.CharField(max_length=200)
  phone_number =  models.CharField(max_length=200)

  def __str__(self):
        return self.name


class index(models.Model):
    name= models.CharField(max_length=100)
    # image= models.CharField(max_length=100)
    active = models.CharField(max_length=100, default='0')
    image= models.ImageField(null=True, blank=True, upload_to = "admin/index/images/")
    
    def __str__(self):
        return self.name
     

class category(models.Model):
    name= models.CharField(max_length=100)
    # image= models.CharField(max_length=100)
    image= models.ImageField(null=True, blank=True, upload_to = "admin/category/images/")
    index_id= models.CharField(max_length=100)
    active = models.CharField(max_length=100, default='0')
    
    def __str__(self):
        return self.name

class MyModel(models.Model):
    Name = models.CharField(max_length=100)
    Rollno = models.IntegerField()
    # Add more fields as needed 

    
class Contact(models.Model):
    full_name=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
    message=models.TextField()

    def __str__(self):
        return self.full_name
        

class Prperty(models.Model):
    index=models.CharField(max_length=100)
    category=models.CharField(max_length=200)
    weburl=models.TextField()
    address=models.TextField()
    purchase_type=models.CharField(max_length=200)
    property_type=models.CharField(max_length=200)
    floor_area=models.CharField(max_length=200)
    Bedroom=models.CharField(max_length=200)
    bathroom=models.CharField(max_length=200)
    features=models.CharField(max_length=200)
    amenties=models.CharField(max_length=1000)
    duration=models.CharField(max_length=200)
    image =models.ImageField(upload_to='images/',default=' ')
    is_admin=models.CharField(max_length=200)
    title = models.CharField(max_length=100, default=' ')
    user_id = models.CharField(max_length=100, default=' ')
    floor_area_value = models.CharField(max_length=100, default=' ')
    amount = models.CharField(max_length=100, default=' ')
    site_area = models.CharField(max_length=100, default=' ')
    site_area_value = models.CharField(max_length=100, default=' vlue')
    Country = models.CharField(max_length=200,default=' ')
    Continent = models.CharField(max_length=200,default='')
    created_at = models.DateTimeField(default=timezone.now)
    hide = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=200, default="")
    # created_at = models.CharField(max_length=100, default='default value')
    
    def __str__(self):
        return self.index        

    
class Propertyuser(models.Model):
    property_id=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    company_name=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.property_id

class CustomUser(AbstractUser):
    is_delete =models.CharField(max_length=100, default='0') 
    opt= models.CharField(max_length=100, default='null')      
    

class database(models.Model):
    name = models.CharField(max_length=100)
    # date_added = models.DateField()
    date_uploaded = models.DateTimeField(null=True, blank=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    number = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    city_town = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    status_value = models.CharField(max_length=100)
    prop_type = models.CharField(max_length=100)
    features = models.CharField(max_length=100)
    exterior = models.CharField(max_length=100)
    interior = models.CharField(max_length=100)
    energy_efficiency = models.CharField(max_length=100)
    environmental_impact = models.CharField(max_length=100)
    riverside = models.CharField(max_length=100)
    seaside = models.CharField(max_length=100)
    bar = models.CharField(max_length=100)
    convenience_store = models.CharField(max_length=100)
    fire_station = models.CharField(max_length=100)
    gym = models.CharField(max_length=100)
    hospital = models.CharField(max_length=100)
    nursery = models.CharField(max_length=100)
    park = models.CharField(max_length=100)
    petrol_station = models.CharField(max_length=100)
    police_station = models.CharField(max_length=100)
    restaurant = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    super_market = models.CharField(max_length=100)
    floor_area = models.CharField(max_length=100)
    site_area = models.CharField(max_length=100)
    kitchen = models.CharField(max_length=100)
    living_room = models.CharField(max_length=100)
    bedroom1 = models.CharField(max_length=100)
    bedroom2 = models.CharField(max_length=100)
    bedroom3 = models.CharField(max_length=100)
    airport = models.CharField(max_length=100)
    bus_stop = models.CharField(max_length=100)
    train_station = models.CharField(max_length=100)
    underground_station = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    sort = models.CharField(max_length=200, default="")
    property_id = models.CharField(max_length=200, default="")
    city = models.CharField(max_length=200, default="")
    duration = models.CharField(max_length=200, default=0)
    expired_date = models.DateTimeField(null=True, blank=True)
    # action = models.CharField(max_length=200, default="")


# class rating(models.Model):
#     inrating_admin = models.CharField(max_length=100)
#     inrating_subadmin = models.CharField(max_length=100)
#     inrating_subadmin = models.CharField(max_length=100)
#     inrating = models.CharField(max_length=100)
#     inrating = models.CharField(max_length=100)
#     inrating = models.CharField(max_length=100)
#     inrating = models.CharField(max_length=100)

    def __str__(self):
        return self.name
   

class Rating(models.Model):
    admin_id= models.CharField(max_length=100)
    interior=models.CharField(max_length=100, default='')
    exterior=models.CharField(max_length=100, default='')
    property_id= models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    name = models.CharField(max_length=100, default="")
    date_added = models.DateField(null=True, blank=True)
    link = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.admin_id




class Entry(models.Model):
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline  


class PropertyPercentile(models.Model):
    property_id = models.CharField(max_length=100)
    exterior = models.CharField(max_length=100, null=True)
    interior = models.CharField(max_length=100, null=True)
    energy_efficiency = models.CharField(max_length=100, null=True)
    environmental_impact = models.CharField(max_length=100, null=True)
    riverside = models.CharField(max_length=100, null=True)
    seaside = models.CharField(max_length=100, null=True)
    bar = models.CharField(max_length=100, null=True)
    convenience_store = models.CharField(max_length=100, null=True)
    fire_station = models.CharField(max_length=100, null=True)
    gym = models.CharField(max_length=100, null=True)
    hospital = models.CharField(max_length=100, null=True)
    nursery = models.CharField(max_length=100, null=True)
    park = models.CharField(max_length=100, null=True)
    petrol_station = models.CharField(max_length=100, null=True)
    police_station = models.CharField(max_length=100, null=True)
    restaurant = models.CharField(max_length=100, null=True)
    school = models.CharField(max_length=100, null=True)
    super_market = models.CharField(max_length=100, null=True)
    floor_area = models.CharField(max_length=100, null=True)
    site_area = models.CharField(max_length=100, null=True)
    kitchen = models.CharField(max_length=100, null=True)
    living_room = models.CharField(max_length=100, null=True)
    bedroom1 = models.CharField(max_length=100, null=True)
    bedroom2 = models.CharField(max_length=100, null=True)
    bedroom3 = models.CharField(max_length=100, null=True)
    airport = models.CharField(max_length=100, null=True)
    bus_stop = models.CharField(max_length=100, null=True)
    train_station = models.CharField(max_length=100, null=True)
    underground_station = models.CharField(max_length=100, null=True)
    index=models.CharField(max_length=100, null=True)
    category=models.CharField(max_length=200, null=True)
    weburl=models.TextField(null=True)
    address=models.TextField(null=True)
    purchase_type=models.CharField(max_length=200, null=True)
    property_type=models.CharField(max_length=200, null=True)
    Bedroom=models.CharField(max_length=200, null=True)
    bathroom=models.CharField(max_length=200, null=True)
    features=models.CharField(max_length=200, null=True)
    amenties=models.CharField(max_length=1000, null=True)
    duration=models.CharField(max_length=200, null=True)
    is_admin=models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=100, null=True)
    user_id = models.CharField(max_length=100, null=True)
    amount = models.CharField(max_length=100, null=True)
    Country = models.CharField(max_length=200, null=True)
    Continent = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    hide = models.CharField(max_length=100, null=True)
    date_uploaded = models.DateTimeField(null=True, blank=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    city = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.property_id        

