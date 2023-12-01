import ast
from django.shortcuts import render
from polls.models import index ,category,Contact, Prperty, Propertyuser,CustomUser, Rating, database, PropertyPercentile
from django.db.models import Avg, F
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from datetime import datetime, date
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes#, force_text 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.core.mail import EmailMessage 
from django.db.models import F, Window
from datetime import date, timedelta
from datetime import datetime
from django.db.models import Q
from collections import Counter
import random,re
import re
from django.db.models import Q
from datetime import date
from django.core import serializers
from django.db.models.functions import PercentRank
from django.db.models import Count
import requests
import json

# User Registration____________________________________________________________________
def email_registration(request):  
    if request.method == 'POST': 
        rand_num = random.randrange(1000, 9000) 
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = make_password(request.POST['password1'])
        opt=rand_num
        user =  CustomUser.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password1, opt=opt)       
        user.is_active = False
        user.save()

        current_site = get_current_site(request)  
        mail_subject = 'Welcome to the linktoscale Web Application' 
        message = render_to_string('acc_active_email.html', {  
            'user': user,  
            'domain': current_site.domain,  
            'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
            'opt': rand_num
            # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(), 
            # 'token':account_activation_token.make_token(user), 
        })  
        to_email = email 
        email = EmailMessage(  
                    mail_subject, message, to=[to_email]  
        )  
        email.send()  
        return render(request,  'otp.html',{'user':user})  
    else:         
        return render(request, 'signup.html') 


def activate(request): 
    if request.method == 'POST':
        username = request.POST.get('username')  # Get the email from the POST data
        opt = request.POST.get('opt')

        user = CustomUser.objects.filter(username=username, opt=opt).first()
        if user:
            user.is_active = True
            user.save()
            return render(request,  'login.html') 
        else:
            context = {'error': 'Wrong OTP'}
            return redirect(request,  'otp.html',{'context': context}) 
    else:
        return redirect('/activate')



def register_request(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = make_password(request.POST['password1'])
        CustomUser.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
        messages.success(request, 'Data has been submitted')

    return render(request, 'signup.html')

def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active and user.is_delete == 0:
            login(request, user)
            return redirect('/')
        else:
            context = {'error': 'Please enter valid credentials'}
            return render(request, 'login.html', {'context': context})

    return render(request, 'login.html')




#frontend functions____________________________________________________________________
# def filter_data(request):
#     if request.method == 'POST':
#         date = request.POST.get('date')
#         continent = request.POST.get('continent')
#         country = request.POST.get('country')
#         city = request.POST.get('city')
#         status = request.POST.get('status')
#         property_type = request.POST.get('property_type')
#         features = request.POST.get('feature')
#         amenities = request.POST.get('amenities')
#         website = request.POST.get('site')

#         # Create an empty dictionary to store the filter parameters
#         filters = {}

#         # Add the filter parameters only if they are not empty
#         # if date:
#         #     filters['date'] = date
#         # if continent:
#         #     filters['continent'] = continent
#         if date:
#             filters.update({'date': date})
#         if continent:
#             filters.update({'continent': continent})
#         if country:
#             filters.update({'address__icontains': country})
#         if city:
#             filters.update({'city': city})
#         if status:
#             filters.update({'purchase_type': status})
#         if property_type:
#             filters.update({'property_type': property_type})
#         if features:
#             filters.update({'features__icontains': features})
#         if amenities:
#             filters.update({'amenties__icontains': amenities})
#         if website:
#             filters.update({'weburl': weburl})

#         # Use the filter parameters to query the database
#         filtered_data = Prperty.objects.filter(**filters)##.extra(where=["purchase_type = %s"], params=[status])

#         # Pass the filtered data to the template for rendering
#         return render(request, 'filtered.html', {'filtered_data': filtered_data})

#     return render(request, 'filtered.html')



#-----------------------Backend validation for fields------------------------------------------->>>
# def Addproperty(request):
#     if request.method == 'POST':
#         index = request.POST.get('index', '')
#         category = request.POST.get('category', '')
#         weburl = request.POST.get('weburl', '')
#         address = request.POST.get('address', '')
#         image = request.FILES.get('image')
#         purchase_type = request.POST.get('purchase_type', '')
#         floor_area = request.POST.get('floor_area', '')
#         property_type = request.POST.getlist('property_type')
#         bedroom = request.POST.get('bedroom', '')
#         bathroom = request.POST.get('bathroom', '')
#         amenities = request.POST.getlist('amenities')
#         features = request.POST.getlist('features')
#         duration = request.POST.get('duration', '')
#         amount = request.POST.get('amount', '')
#         floor_area_value = request.POST.get('floor_area_value', '')
#         site_area = request.POST.get('site_area', '')
#         site_area_value = request.POST.get('site_area_value', '')
#         country = request.POST.get('country', '')
#         continent = request.POST.get('continent', '')
#         hide = request.POST.get('hide', '')
#         is_admin = '0'

#         name = request.POST.get('name', '')
#         company_name = request.POST.get('company_name', '')
#         phone = request.POST.get('phone', '')
#         email = request.POST.get('email', '')

#         # Validation
#         errors = {}

#         if not index:
#             errors['index'] = 'Please provide an index.'

#         if not category:
#             errors['category'] = 'Please select a category.'

#         if not weburl:
#             errors['weburl'] = 'Please provide a web URL.'

#         if not address:
#             errors['address'] = 'Please provide an address.'

#         if not image:
#             errors['image'] = 'Please select an image.'

#         if not purchase_type:
#             errors['purchase_type'] = 'Please select a purchase type.'

#         if not floor_area:
#             errors['floor_area'] = 'Please provide a floor area.'

#         if not property_type:
#             errors['property_type'] = 'Please select at least one property type.'

#         if not bedroom:
#             errors['bedroom'] = 'Please provide the number of bedrooms.'

#         if not bathroom:
#             errors['bathroom'] = 'Please provide the number of bathrooms.'

#         if not amenities:
#             errors['amenities'] = 'Please select at least one amenity.'

#         if not features:
#             errors['features'] = 'Please select at least one feature.'

#         if not duration:
#             errors['duration'] = 'Please provide a duration.'

#         if not amount:
#             errors['amount'] = 'Please provide an amount.'

#         if not floor_area_value:
#             errors['floor_area_value'] = 'Please provide a floor area value.'

#         if not site_area:
#             errors['site_area'] = 'Please provide a site area.'

#         if not site_area_value:
#             errors['site_area_value'] = 'Please provide a site area value.'

#         if not country:
#             errors['country'] = 'Please provide a country.'

#         if not continent:
#             errors['continent'] = 'Please provide a continent.'

#         if not name:
#             errors['name'] = 'Please provide a name.'

#         if not company_name:
#             errors['company_name'] = 'Please provide a company name.'

#         if not phone:
#             errors['phone'] = 'Please provide a phone number.'

#         if not email:
#             errors['email'] = 'Please provide an email address.'

#         if errors:
#             # If there are validation errors, render the form with the errors
#             return render(request, 'upload.html', {'errors': errors})

#         # Create Propertyuser object
#         property_user = Propertyuser.objects.create(
#             name=name,
#             company_name=company_name,
#             phone=phone,
#             email=email,
#         )

#         # Create Prperty object
#         words = address.split()
#         first_few_words = ' '.join(words[:3])
#         Addproperty = Prperty.objects.create(
#             user_id=property_user.id,
#             index=index,
#             category=category,
#             weburl=weburl,
#             address=address,
#             title=first_few_words,
#             image=image,
#             purchase_type=purchase_type,
#             floor_area=floor_area,
#             property_type=property_type,
#             bedroom=bedroom,
#             bathroom=bathroom,
#             features=features,
#             amenities=amenities,
#             duration=duration,
#             amount=amount,
#             floor_area_value=floor_area_value,
#             site_area=site_area,
#             site_area_value=site_area_value,
#             Country=country,
#             Continent=continent,
#             hide=hide,
#             is_admin=is_admin,
#         )

#         messages.success(request, 'Data has been submitted')
#         return redirect('/residential')

#     return render(request, 'upload.html')

#------------------some fields validation is not working------------------------>>
#-----------------------Backend Validation------------------------------------------->>

# def Addproperty(request):
#     # print(request.POST.get('index', ''))
#     # return HttpResponse(request.POST.get('index', ''))

#     if request.method == 'POST':
#         index = request.POST.get('index', '')
#         category = request.POST.get('category', '')  # Assign a value to category
#         weburl = request.POST.get('weburl', '')
#         address = request.POST.get('address', '')
#         # title = request.POST.get('title', '')
#         image = request.FILES['image']
#         purchase_type = request.POST.get('purchase_type', '')
#         floor_area = request.POST.get('floor_area', '')
#         property_type = request.POST.getlist('property_type', '')
#         Bedroom = request.POST.get('Bedroom', '')
#         bathroom = request.POST.get('bathroom', '')
#         amenties = request.POST.getlist('amenties')
#         features = request.POST.getlist('features')
#         duration = request.POST.get('duration', '')
#         amount = request.POST.get('amount', '')
#         floor_area_value = request.POST.get('floor_area_value', '')
#         site_area = request.POST.get('site_area', '')
#         site_area_value = request.POST.get('site_area_value', '')
#         country = request.POST.get('country','')
#         continent = request.POST.get('continent','')
#         hide = request.POST.get('hide', '')
#         is_admin = '0'

#         # Store user data in second model
#         name = request.POST.get('name', '')
#         company_name = request.POST.get('company_name', '')
#         phone = request.POST.get('phone', '')
#         email = request.POST.get('email', '')

#         words = address.split()
#         first_few_words = ' '.join(words[:3])




#         property_user = Propertyuser.objects.create(
#             name=name,
#             company_name=company_name,
#             phone=phone,
#             email=email,
#         )

#         Addproperty = Prperty.objects.create(
#             user_id= property_user.id,
#             index=index,
#             category=category,
#             weburl=weburl,
#             address=address,
#             title=first_few_words,
#             image=image,
#             purchase_type=purchase_type,
#             floor_area=floor_area,
#             property_type=property_type,
#             Bedroom=Bedroom,
#             bathroom=bathroom,
#             features=features,
#             amenties=amenties,
#             duration=duration,
#             amount=amount,
#             floor_area_value=floor_area_value,
#             site_area=site_area,
#             site_area_value=site_area_value,
#             Country=country,
#             Continent=continent,
#             hide=hide,
#             is_admin=is_admin,
            
#         )
        

#         # property_user.Prperty = Addproperty  # Associate with Prperty object
#         # property_user.save()  # Save the created object

#         messages.success(request, 'Data has been submitted')

#         return redirect('/residential')

#     return render(request, 'upload.html')

#------------------------------>>>>>------------------------------
def Addproperty(request):
    if request.method == 'POST':
            index = request.POST.get('index', '')
            category = request.POST.get('category', '')
            weburl = request.POST.get('weburl', '')
            address = request.POST.get('address', '')
            city =request.POST.get('city', '')
            image = request.FILES.get('image', '')
            purchase_type = request.POST.get('purchase_type', '')
            floor_area = request.POST.get('floor_area', '')
            property_type = request.POST.getlist('property_type')
            Bedroom = request.POST.get('Bedroom', '')
            bathroom = request.POST.get('bathroom', '')
            amenties = request.POST.getlist('amenties')
            features = request.POST.getlist('features')
            duration = request.POST.get('duration', '')
            amount = request.POST.get('amount', '')
            floor_area_value = request.POST.get('floor_area_value', '')
            site_area = request.POST.get('site_area', '')
            site_area_value = request.POST.get('site_area_value', '')
            country = request.POST.get('country', '')
            continent = request.POST.get('continent', '')
            hide = request.POST.get('hide', '')
            is_admin = '0'

            name = request.POST.get('name', '')
            company_name = request.POST.get('company_name', '')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            words = address.split()
            first_few_words = ' '.join(words[:3])

            property_user = Propertyuser.objects.create(
                name=name,
                company_name=company_name,
                phone=phone,
                email=email,
            )

            Addproperty = Prperty.objects.create(
                user_id=property_user.id,
                index=index,
                category=category,
                weburl=weburl,
                address=address,
                title=first_few_words,
                image=image,
                purchase_type=purchase_type,
                floor_area=floor_area,
                property_type=property_type,
                Bedroom=Bedroom,
                bathroom=bathroom,
                features=features,
                amenties=amenties,
                duration=duration,
                amount=amount,
                floor_area_value=floor_area_value,
                site_area=site_area,
                site_area_value=site_area_value,
                Country=country,
                Continent=continent,
                hide=hide,
                is_admin=is_admin,
                city=city,
            )

            # Check if there are additional listings
            listing_counter = int(request.POST.get('listingCounter', 0))
            for i in range(2, listing_counter + 1):
                index = request.POST.get(f'index{i}', '')
                category = request.POST.get(f'category{i}', '')
                weburl = request.POST.get(f'weburl{i}', '')
                address = request.POST.get(f'address{i}', '')
                image = request.FILES.get(f'image{i}', '')
                purchase_type = request.POST.get(f'purchase_type{i}', '')
                floor_area = request.POST.get(f'floor_area{i}', '')
                property_type = request.POST.getlist(f'property_type{i}', [])
                Bedroom = request.POST.get(f'Bedroom{i}', '')
                bathroom = request.POST.get(f'bathroom{i}', '')
                amenties = request.POST.getlist(f'amenties{i}', [])
                features = request.POST.getlist(f'features{i}', [])
                duration = request.POST.get(f'duration{i}', '')
                amount = request.POST.get(f'amount{i}', '')
                floor_area_value = request.POST.get(f'floor_area_value{i}', '')
                site_area = request.POST.get(f'site_area{i}', '')
                site_area_value = request.POST.get(f'site_area_value{i}', '')
                country = request.POST.get(f'country{i}', '')
                continent = request.POST.get(f'continent{i}', '')
                hide = request.POST.get(f'hide{i}', '')
                is_admin = '0'

                Addproperty=Prperty.objects.create(
                    user_id=property_user.id,
                    index=index,
                    category=category,
                    weburl=weburl,
                    address=address,
                    title=first_few_words,
                    image=image,
                    purchase_type=purchase_type,
                    floor_area=floor_area,
                    property_type=property_type,
                    Bedroom=Bedroom,
                    bathroom=bathroom,
                    features=features,
                    amenties=amenties,
                    duration=duration,
                    amount=amount,
                    floor_area_value=floor_area_value,
                    site_area=site_area,
                    site_area_value=site_area_value,
                    Country=country,
                    Continent=continent,
                    hide=hide,
                    is_admin=is_admin,
                    city=city,
                )

            messages.success(request, 'Data has been submitted')
            
            return redirect('/thankyou')
    else:
        # form = LoginForm()
     return render(request, 'testing_upload.html')


#------------------------------<<<<<-------------------------------
def thankyou(request):
    return render(request, 'submit.html')

def wrongotp(request):
    return render(request,'otp.html')

def contact(request):
    if request.method=='POST':
        full_name=request.POST['full_name']
        email=request.POST['email']
        message=request.POST['message']
        contact=Contact.objects.create(full_name=full_name,email=email,message=message)
        messages.success(request,'Data has been submitted')
    return render(request,'contact.html')
    

def home(request):
	st=index.objects.all() # Collect all records from table 
	return render(request,'home.html',{'st':st})



def category_view(request, sts_id):
    cat = category.objects.filter(index_id=sts_id)
    return render(request, 'property.html', {'cat': cat})

	
def how_it_works(request):
    return render(request,'how_it_works.html')

def help(request):
    return render(request,'help.html')

def settings(request):
    return render(request,'settings.html')

def upload(request):
    return render(request,'testing_upload.html')

def property(request):
    return render(request,'property.html',{'st':st})

def vehicles(request):
    return render(request,'vehicles.html')

# def residential(request):
#     properties = Prperty.objects.filter(index=1, category=1, is_admin=1)
    
#     for property in properties:
#         if property.hide == "on":
#             ini_string = property.title
#             property.title = ''.join([i for i in ini_string if not i.isdigit()])

#     return render(request, 'residential.html', {'properties': properties})

def subcategory(request):
    return render(request,'sub-category.html')
    
def userlogin(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html') 

def residential(request):
    if is_ajax(request):
        # Filters Request
        status = request.GET.get("status", '')
        purchase_type=status
        property_type = request.GET.getlist("property_type[]", '')
        showBuy = request.GET.get("rent", '')
        buy =  request.GET.get("buy", '')
        auction = request.GET.get("auction", '')
        stay = request.GET.get("stay", '')

        country = request.GET.get("country", '')
        features =  request.GET.getlist("features[]", '')
       

        amenities = request.GET.get("amenities", '')
        amenity_list = amenities.split(',')
        duration = request.GET.get("duration", '')
        bedrooms = request.GET.getlist("bedrooms[]", '')
        bedrooms = [str(int(re.search(r'\d+', bedroom).group())) for bedroom in bedrooms]
        
        created_at= request.GET.get('created_at', '')
        continent= request.GET.getlist("continent[]", '')
        city = request.GET.get("city", '')
        price = request.GET.get("price", '')
        bathrooms = request.GET.getlist("bathroom[]", '')
        bathroom = [str(int(re.search(r'\d+', bathroomobj).group())) for bathroomobj in bathrooms]

        # print(bathroom)
        # return HttpResponse(bathroom)

        # Aesthetic 
        interior = request.GET.get("interior", '')
        exterior = request.GET.get("exterior", '')

        # Ecofriendly
        environment = request.GET.get("environment", '')
        energy = request.GET.get("energy", '')
        
        # Nearby
        river = request.GET.get("river", '')
        seaside = request.GET.get("seaside", '')
        bar = request.GET.get("bar", '')
        convinience = request.GET.get("convinience", '')
        fire = request.GET.get("fire", '')
        gym = request.GET.get("gym", '')
        hospital = request.GET.get("hospital", '')
        nursery = request.GET.get("nursery", '')
        park = request.GET.get("park", '')
        petrol = request.GET.get("petrol", '')
        police = request.GET.get("police", '')
        restaurant = request.GET.get("restaurant", '')
        school = request.GET.get("school", '')
        market = request.GET.get("market", '')

        # Transport
        airport = request.GET.get("airport", '')
        bus_stop = request.GET.get("bus_stop", '')
        train_station = request.GET.get("train_station", '')
        underground_station = request.GET.get("underground_station", '')

        #Sizes
        floor_area = request.GET.get("floor_area", '')
        site_area = request.GET.get("site_area", '')
        kitchen = request.GET.get("kitchen", '')
        living_room = request.GET.get("living_room", '')
        bedroom1 = request.GET.get("bedroom1", '')
        bedroom2 = request.GET.get("bedroom2", '')
        bedroom3 = request.GET.get("bedroom3", '')

        # change status into integer
        if status =='Rent':
           status='0'
        elif  status =='Buy':
            status='1' 
        elif  status =='Auction':
            status='2' 
        elif  status =='Stay':
            status='3' 
        elif  status =='Featured':
            status='4'            
       

        # Verified Check
        index=1
        category=1
        is_admin=1
        
        filters = {}


        continent_str = ', '.join(continent)
        continent_list = continent_str.split(', ')

        country_str= ', '.join(country)
        country_list = country_str.split(', ')

        city_str = ', '.join(city)
        city_list = city_str.split(', ')

        property_type_str = ', '.join(property_type)
        property_type_list = property_type_str.split(', ')

        features_str = ', '.join(features)
        features_str_list = features_str.split(', ')
        

        bedrooms_str = ', '.join(bedrooms)
        bedrooms_str_list = bedrooms_str.split(', ')

        bathroom_str = ', '.join(bathroom)
        bathroom_str_list = bathroom_str.split(', ')
        
        properties = PropertyPercentile.objects.all()

       
    # Filters____________________
        if created_at:
            created_at = int(created_at)
            today_date = datetime.now()
            previous_day_date = today_date - timedelta(days=created_at)
            
            properties = properties.filter(date_uploaded__gte=previous_day_date)
       
        if amenities:
            for amenity in amenity_list:
                 properties = properties.filter(amenties__icontains=amenity.strip())

        if continent:
            properties = properties.filter(Continent__in=continent_list)

        if country:
            properties = properties.filter(Country__icontains=country)

        # properties_list = list(properties.values())
        # print(properties_list)
        # return HttpResponse(properties_list) 

        if showBuy and  status=="0":
           lower, upper = [int(value.strip()) for value in showBuy.split(',')]
           upper= int(upper)
           lower= int(lower)
           properties = properties.filter(amount__range=(lower,upper)) 

        if buy and status=="1":
           lower, upper = [int(value.strip()) for value in buy.split(',')]
           upper= int(upper)
           lower= int(lower)
           properties = properties.filter(amount__range=(lower,upper))        

        if auction and status=="2":
           lower, upper = [int(value.strip()) for value in auction.split(',')]
           upper= int(upper)
           lower= int(lower)
           properties = properties.filter(amount__range=(lower,upper)) 
                
        if status:
            properties = properties.filter(purchase_type=status) 

        if stay and status=="3": 
           lower, upper = [int(value.strip()) for value in stay.split(',')]
           upper= int(upper)
           lower= int(lower)
           properties = properties.filter(amount__range=(lower,upper))
                

        if property_type:
            for property_typeOBj in property_type_list:    
                 properties = properties.filter(property_type__icontains=property_typeOBj)

        if features: 
            for features_strObj in features_str_list:    
                 properties = properties.filter(features__icontains=features_strObj)

        if bedrooms: 
            properties = properties.filter(Bedroom__in=bedrooms_str_list)

        if bathroom: 
            properties = properties.filter(bathroom__in=bathroom_str_list)    

        if city:
            properties = properties.filter(city=city)
    #Indexes Filters_____________
       
        # Aeshthetic Indexes  
        if interior == "2":
            properties = properties.filter(interior__gte=25)

        if interior == "3":
            properties=  properties.filter(interior__gte=75)
         

        if exterior == "2":
             properties=  properties.filter(exterior__gte=25)
   
        if exterior == "3":
             properties=  properties.filter(exterior__gte=75)


        # Ecofriendly Indexes  
        if environment == "2":
            properties = properties.filter(environmental_impact__gte=25)

        if environment == "3":
            properties=  properties.filter(environmental_impact__gte=75)
         

        if energy == "2":
             properties=  properties.filter(energy_efficiency__gte=25)
   
        if energy == "3":
             properties=  properties.filter(energy_efficiency__gte=75)  




        # Nearby
        if river == "2":
            properties = properties.filter(riverside__gte=25)

        if river == "3":
            properties=  properties.filter(riverside__gte=75)
         


        if seaside == "2":
             properties=  properties.filter(seaside__gte=25)
   
        if seaside == "3":
             properties=  properties.filter(seaside__gte=75)  



        if bar == "2":
            properties = properties.filter(bar__gte=25)

        if bar == "3":
            properties=  properties.filter(bar__gte=75)
         


        if convinience == "2":
             properties=  properties.filter(convenience_store__gte=25)
   
        if convinience == "3":
             properties=  properties.filter(convenience_store__gte=75)     



        if fire == "2":
            properties = properties.filter(fire_station__gte=25)

        if fire == "3":
            properties=  properties.filter(fire_station__gte=75)
         


        if gym == "2":
             properties=  properties.filter(gym__gte=25)
   
        if gym == "3":
             properties=  properties.filter(gym__gte=75)  



        if hospital == "2":
            properties = properties.filter(hospital__gte=25)

        if hospital == "3":
            properties=  properties.filter(hospital__gte=75)
         

        if nursery == "2":
             properties=  properties.filter(nursery__gte=25)
   
        if nursery == "3":
             properties=  properties.filter(nursery__gte=75)



        if park == "2":
            properties = properties.filter(park__gte=25)

        if park == "3":
            properties=  properties.filter(park__gte=75)
         

        if petrol == "2":
             properties=  properties.filter(petrol_station__gte=25)
   
        if petrol == "3":
             properties=  properties.filter(petrol_station__gte=75) 




        if police == "2":
            properties = properties.filter(police_station__gte=25)

        if police == "3":
            properties=  properties.filter(police_station__gte=75)
         

        if restaurant == "2":
             properties=  properties.filter(restaurant__gte=25)
   
        if restaurant == "3":
             properties=  properties.filter(restaurant__gte=75)   




        if school == "2":
            properties = properties.filter(school__gte=25)

        if school == "3":
            properties=  properties.filter(school__gte=75)
         

        if market == "2":
             properties=  properties.filter(super_market__gte=25)
   
        if market == "3":
             properties=  properties.filter(super_market__gte=75)   





        # Sizes Indexes
        if floor_area == "2":
            properties = properties.filter(floor_area__gte=25)

        if floor_area == "3":
            properties=  properties.filter(floor_area__gte=75)
         

        if site_area == "2":
             properties=  properties.filter(site_area__gte=25)
   
        if site_area == "3":
             properties=  properties.filter(site_area__gte=75)



        if kitchen == "2":
            properties = properties.filter(kitchen__gte=25)

        if kitchen == "3":
            properties=  properties.filter(kitchen__gte=75)
         

        if living_room == "2":
             properties=  properties.filter(living_room__gte=25)
   
        if living_room == "3":
             properties=  properties.filter(living_room__gte=75)


        if bedroom1 == "2":
            properties = properties.filter(bedroom1__gte=25)

        if bedroom1 == "3":
            properties=  properties.filter(bedroom1__gte=75)
         

        if bedroom2 == "2":
             properties=  properties.filter(bedroom2__gte=25)
   
        if bedroom2 == "3":
             properties=  properties.filter(bedroom2__gte=75)                                             
         

        if bedroom3 == "2":
             properties=  properties.filter(bedroom3__gte=25)
   
        if bedroom3 == "3":
             properties=  properties.filter(bedroom3__gte=75) 


        # Transport 
        if airport == "2":
            properties = properties.filter(airport__gte=25)

        if airport == "3":
            properties=  properties.filter(airport__gte=75)
         

        if bus_stop == "2":
             properties=  properties.filter(bus_stop__gte=25)
   
        if bus_stop == "3":
             properties=  properties.filter(bus_stop__gte=75)                                             
         

        if train_station == "2":
             properties=  properties.filter(train_station__gte=25)
   
        if train_station == "3":
             properties=  properties.filter(train_station__gte=75)


        if underground_station == "2":
             properties=  properties.filter(underground_station__gte=25)
   
        if underground_station == "3":
             properties=  properties.filter(underground_station__gte=75)        
        

        getcity =''
     
        property_list = []
        count = 0  
        for property in properties:
            singleitem= Prperty.objects.filter(id= property.property_id).first()
            db_property= database.objects.filter(property_id= property.property_id).first()
             
             
            property.image= singleitem.image  
            property.weburl= singleitem.weburl  

            hide = singleitem.hide
            if hide == "on":
                ini_string = db_property.name
                title = ''.join([i for i in ini_string if not i.isdigit()])
            else:
                title = db_property.name

            property_list.append({
                'id': property.property_id,
                'title': title,
                'image': property.image.url,
                'weburl': property.weburl,
            })
                
            count += 1  

        return JsonResponse({'properties': property_list, 'count': count,  'getcity': getcity})   
    else: 
         properties = Prperty.objects.filter(index=1, category=1, is_admin=1)

         asia = Prperty.objects.filter(is_admin=1, Continent__exact='Asia').count()
         europe = Prperty.objects.filter(is_admin=1, Continent='Europe').count()
         africa = Prperty.objects.filter(is_admin=1, Continent__exact='Africa').count()
         antractica = Prperty.objects.filter(is_admin=1, Continent__exact='Antractica').count()
         north_america = Prperty.objects.filter(is_admin=1, Continent__exact='North America').count()
         south_america = Prperty.objects.filter(is_admin=1, Continent__exact='South America').count()
         australia = Prperty.objects.filter(is_admin=1, Continent__exact='Australia').count()


         #Property Type Count 
         Duplex= Prperty.objects.filter(is_admin=1, property_type__icontains='Duplex').count()
         Garden= Prperty.objects.filter(is_admin=1, property_type__icontains='Garden').count()
         Highrise= Prperty.objects.filter(is_admin=1, property_type__icontains='Highrise').count()
         House= Prperty.objects.filter(is_admin=1, property_type__icontains='House').count()
         Apartment= Prperty.objects.filter(is_admin=1, property_type__icontains='Flat/Apartment').count()
         Lowrise= Prperty.objects.filter(is_admin=1, property_type__icontains='Lowrise').count()
         Joint= Prperty.objects.filter(is_admin=1, property_type__icontains='Joint').count()
         Luxury= Prperty.objects.filter(is_admin=1, property_type__icontains='Luxury Highrise').count()
         Flat = Prperty.objects.filter(is_admin=1, property_type__icontains='Flat').count()
         Bungalow = Prperty.objects.filter(is_admin=1, property_type__icontains='Bungalow').count()

         #country
         Afghanistan = Prperty.objects.filter(is_admin=1, Country__icontains='Afghanistan').count()
         Aland_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Aland Islands').count()
         Albania = Prperty.objects.filter(is_admin=1, Country__icontains='Albania').count()
         Algeria = Prperty.objects.filter(is_admin=1, Country__icontains='Algeria').count()
         American_Samoa = Prperty.objects.filter(is_admin=1, Country__icontains='American Samoa').count()
         Andorra = Prperty.objects.filter(is_admin=1, Country__icontains='Andorra').count()
         Angola = Prperty.objects.filter(is_admin=1, Country__icontains='Angola').count()
         Anguilla = Prperty.objects.filter(is_admin=1, Country__icontains='Anguilla').count()
         Antarctica = Prperty.objects.filter(is_admin=1, Country__icontains='Antarctica').count()
         Antigua_and_Barbuda = Prperty.objects.filter(is_admin=1, Country__icontains='Antigua and Barbuda').count()
         Argentina = Prperty.objects.filter(is_admin=1, Country__icontains='Argentina').count()
         Armenia = Prperty.objects.filter(is_admin=1, Country__icontains='Armenia').count()
         Aruba = Prperty.objects.filter(is_admin=1, Country__icontains='Aruba').count()
         Australia = Prperty.objects.filter(is_admin=1, Country__icontains='Australia').count()
         Austria = Prperty.objects.filter(is_admin=1, Country__icontains='Austria').count()
         Azerbaijan = Prperty.objects.filter(is_admin=1, Country__icontains='Azerbaijan').count()
         Bahamas = Prperty.objects.filter(is_admin=1, Country__icontains='Bahamas').count()
         Bahrain = Prperty.objects.filter(is_admin=1, Country__icontains='Bahrain').count()
         Bangladesh = Prperty.objects.filter(is_admin=1, Country__icontains='Bangladesh').count()
         Barbados = Prperty.objects.filter(is_admin=1, Country__icontains='Barbados').count()
         Belarus = Prperty.objects.filter(is_admin=1, Country__icontains='Belarus').count()
         Belgium = Prperty.objects.filter(is_admin=1, Country__icontains='Belgium').count()
         Belize = Prperty.objects.filter(is_admin=1, Country__icontains='Belize').count()
         Benin = Prperty.objects.filter(is_admin=1, Country__icontains='Benin').count()
         Bermuda = Prperty.objects.filter(is_admin=1, Country__icontains='Bermuda').count()
         Bhutan = Prperty.objects.filter(is_admin=1, Country__icontains='Bhutan').count()
         Bolivia = Prperty.objects.filter(is_admin=1, Country__icontains='Bolivia').count()
         Bonaire_Sint_Eustatius_Saba = Prperty.objects.filter(is_admin=1, Country__icontains='Bonaire, Sint Eustatius and Saba').count()
         Bosnia_and_Herzegovina = Prperty.objects.filter(is_admin=1, Country__icontains='Bosnia and Herzegovina').count()
         Botswana = Prperty.objects.filter(is_admin=1, Country__icontains='Botswana').count()
         Bouvet_Island = Prperty.objects.filter(is_admin=1, Country__icontains='Bouvet Island').count()
         Brazil = Prperty.objects.filter(is_admin=1, Country__icontains='Brazil').count()
         British_Indian_Ocean_Territory = Prperty.objects.filter(is_admin=1, Country__icontains='British Indian Ocean Territory').count()
         Brunei_Darussalam = Prperty.objects.filter(is_admin=1, Country__icontains='Brunei Darussalam').count()
         Bulgaria = Prperty.objects.filter(is_admin=1, Country__icontains='Bulgaria').count()
         Burkina_Faso = Prperty.objects.filter(is_admin=1, Country__icontains='Burkina Faso').count()
         Burundi = Prperty.objects.filter(is_admin=1, Country__icontains='Burundi').count()
         Cambodia = Prperty.objects.filter(is_admin=1, Country__icontains='Cambodia').count()
         Cameroon = Prperty.objects.filter(is_admin=1, Country__icontains='Cameroon').count()
         Canada = Prperty.objects.filter(is_admin=1, Country__icontains='Canada').count()
         Cape_Verde = Prperty.objects.filter(is_admin=1, Country__icontains='Cape Verde').count()
         Cayman_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Cayman Islands').count()
         Central_African_Republic = Prperty.objects.filter(is_admin=1, Country__icontains='Central African Republic').count()
         Chad = Prperty.objects.filter(is_admin=1, Country__icontains='Chad').count()
         Chile = Prperty.objects.filter(is_admin=1, Country__icontains='Chile').count()
         China = Prperty.objects.filter(is_admin=1, Country__icontains='China').count()
         Cocos_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Cocos (Keeling) Islands').count()
         Colombia = Prperty.objects.filter(is_admin=1, Country__icontains='Colombia').count()
         Comoros = Prperty.objects.filter(is_admin=1, Country__icontains='Comoros').count()
         Congo = Prperty.objects.filter(is_admin=1, Country__icontains='Congo').count()
         Republic_of_the_Congo = Prperty.objects.filter(is_admin=1, Country__icontains='Congo, Democratic Republic of the Congo').count()
         Cook_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Cook Islands').count()
         Costa_Rica = Prperty.objects.filter(is_admin=1, Country__icontains='Costa Rica').count()
         Cote_DIvoire = Prperty.objects.filter(is_admin=1, Country__icontains="Cote D'Ivoire").count()
         Croatia = Prperty.objects.filter(is_admin=1, Country__icontains='Croatia').count()
         Cuba = Prperty.objects.filter(is_admin=1, Country__icontains='Cuba').count()
         Curacao = Prperty.objects.filter(is_admin=1, Country__icontains='Curacao').count()
         Cyprus = Prperty.objects.filter(is_admin=1, Country__icontains='Cyprus').count()
         Czech_Republic = Prperty.objects.filter(is_admin=1, Country__icontains='Czech Republic').count()
         Denmark = Prperty.objects.filter(is_admin=1, Country__icontains='Denmark').count()
         Djibouti = Prperty.objects.filter(is_admin=1, Country__icontains='Djibouti').count()
         Dominica = Prperty.objects.filter(is_admin=1, Country__icontains='Dominica').count()
         Dominican_Republic = Prperty.objects.filter(is_admin=1, Country__icontains='Dominican Republic').count()
         Ecuador = Prperty.objects.filter(is_admin=1, Country__icontains='Ecuador').count()
         Egypt = Prperty.objects.filter(is_admin=1, Country__icontains='Egypt').count()
         El_Salvador = Prperty.objects.filter(is_admin=1, Country__icontains='El Salvador').count()
         Equatorial_Guinea = Prperty.objects.filter(is_admin=1, Country__icontains='Equatorial Guinea').count()
         Eritrea = Prperty.objects.filter(is_admin=1, Country__icontains='Eritrea').count()
         Estonia = Prperty.objects.filter(is_admin=1, Country__icontains='Estonia').count()
         Ethiopia = Prperty.objects.filter(is_admin=1, Country__icontains='Ethiopia').count()
         Falkland_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Falkland Islands (Malvinas)').count()
         Faroe_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Faroe Islands').count()
         Fiji = Prperty.objects.filter(is_admin=1, Country__icontains='Fiji').count()
         Finland = Prperty.objects.filter(is_admin=1, Country__icontains='Finland').count()
         France = Prperty.objects.filter(is_admin=1, Country__icontains='France').count()
         French_Guiana = Prperty.objects.filter(is_admin=1, Country__icontains='French Guiana').count()
         French_Polynesia = Prperty.objects.filter(is_admin=1, Country__icontains='French Polynesia').count()
         French_Southern_Territories = Prperty.objects.filter(is_admin=1, Country__icontains='French Southern Territories').count()
         Gabon = Prperty.objects.filter(is_admin=1, Country__icontains='Gabon').count()
         Gambia = Prperty.objects.filter(is_admin=1, Country__icontains='Gambia').count()
         Georgia = Prperty.objects.filter(is_admin=1, Country__icontains='Georgia').count()
         Germany = Prperty.objects.filter(is_admin=1, Country__icontains='Germany').count()
         Ghana = Prperty.objects.filter(is_admin=1, Country__icontains='Ghana').count()
         Gibraltar = Prperty.objects.filter(is_admin=1, Country__icontains='Gibraltar').count()
         Greece = Prperty.objects.filter(is_admin=1, Country__icontains='Greece').count()
         Greenland = Prperty.objects.filter(is_admin=1, Country__icontains='Greenland').count()
         Grenada = Prperty.objects.filter(is_admin=1, Country__icontains='Grenada').count()
         Guadeloupe = Prperty.objects.filter(is_admin=1, Country__icontains='Guadeloupe').count()
         Guam = Prperty.objects.filter(is_admin=1, Country__icontains='Guam').count()
         Guatemala = Prperty.objects.filter(is_admin=1, Country__icontains='Guatemala').count()
         Guernsey = Prperty.objects.filter(is_admin=1, Country__icontains='Guernsey').count()
         Guinea = Prperty.objects.filter(is_admin=1, Country__icontains='Guinea').count()
         Guinea_Bissau = Prperty.objects.filter(is_admin=1, Country__icontains='Guinea-Bissau').count()
         Guyana = Prperty.objects.filter(is_admin=1, Country__icontains='Guyana').count()
         Haiti = Prperty.objects.filter(is_admin=1, Country__icontains='Haiti').count()
         Heard_Island_and_Mcdonald_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Heard Island and Mcdonald Islands').count()
         Holy_See = Prperty.objects.filter(is_admin=1, Country__icontains='Holy See (Vatican City State)').count()
         Honduras = Prperty.objects.filter(is_admin=1, Country__icontains='Honduras').count()
         Hong_Kong = Prperty.objects.filter(is_admin=1, Country__icontains='Hong Kong').count()
         Hungary = Prperty.objects.filter(is_admin=1, Country__icontains='Congo').count()
         Iceland = Prperty.objects.filter(is_admin=1, Country__icontains='Iceland').count()
         India = Prperty.objects.filter(is_admin=1, Country__icontains='India').count()
         Indonesia = Prperty.objects.filter(is_admin=1, Country__icontains='Indonesia').count()
         Iran = Prperty.objects.filter(is_admin=1, Country__icontains='Iran').count()
         Iraq = Prperty.objects.filter(is_admin=1, Country__icontains='Iraq').count()
         Ireland = Prperty.objects.filter(is_admin=1, Country__icontains='Ireland').count()
         Isle_of_Man = Prperty.objects.filter(is_admin=1, Country__icontains='Isle of Man').count()
         Israel = Prperty.objects.filter(is_admin=1, Country__icontains='Israel').count()
         Italy = Prperty.objects.filter(is_admin=1, Country__icontains='Italy').count()
         Jamaica = Prperty.objects.filter(is_admin=1, Country__icontains='Jamaica').count()
         Japan = Prperty.objects.filter(is_admin=1, Country__icontains='Japan').count()
         Jersey = Prperty.objects.filter(is_admin=1, Country__icontains='Jersey').count()
         Jordan = Prperty.objects.filter(is_admin=1, Country__icontains='Jordan').count()
         Kazakhstan = Prperty.objects.filter(is_admin=1, Country__icontains='Kazakhstan').count()
         Kenya = Prperty.objects.filter(is_admin=1, Country__icontains='Kenya').count()
         Kiribati = Prperty.objects.filter(is_admin=1, Country__icontains='Kiribati').count()
         Korea = Prperty.objects.filter(is_admin=1, Country__icontains='Korea').count()
         Kosovo = Prperty.objects.filter(is_admin=1, Country__icontains='Kosovo').count()
         Kuwait = Prperty.objects.filter(is_admin=1, Country__icontains='Kuwait').count()
         Kyrgyzstan = Prperty.objects.filter(is_admin=1, Country__icontains='Kyrgyzstan').count()
         Lao_People_Democratic_Republic = Prperty.objects.filter(is_admin=1, Country__icontains="Lao People's Democratic Republic").count()
         Latvia = Prperty.objects.filter(is_admin=1, Country__icontains='Latvia').count()
         Lebanon = Prperty.objects.filter(is_admin=1, Country__icontains='Lebanon').count()
         Lesotho = Prperty.objects.filter(is_admin=1, Country__icontains='Lesotho').count()
         Liberia = Prperty.objects.filter(is_admin=1, Country__icontains='Liberia').count()
         Libyan_Arab_Jamahiriya = Prperty.objects.filter(is_admin=1, Country__icontains='Libyan Arab Jamahiriya').count()
         Liechtenstein = Prperty.objects.filter(is_admin=1, Country__icontains='Liechtenstein').count()
         Lithuania = Prperty.objects.filter(is_admin=1, Country__icontains='Lithuania').count()
         Luxembourg = Prperty.objects.filter(is_admin=1, Country__icontains='Luxembourg').count()
         Macao = Prperty.objects.filter(is_admin=1, Country__icontains='Macao').count()
         Macedonia = Prperty.objects.filter(is_admin=1, Country__icontains='Macedonia, the Former Yugoslav Republic of').count()
         Madagascar = Prperty.objects.filter(is_admin=1, Country__icontains='Madagascar').count()
         Malawi = Prperty.objects.filter(is_admin=1, Country__icontains='Malawi').count()
         Malaysia = Prperty.objects.filter(is_admin=1, Country__icontains='Malaysia').count()
         Maldives = Prperty.objects.filter(is_admin=1, Country__icontains='Maldives').count()
         Mali = Prperty.objects.filter(is_admin=1, Country__icontains='Mali').count()
         Malta = Prperty.objects.filter(is_admin=1, Country__icontains='Malta').count()
         Marshall_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Marshall Islands').count()
         Martinique = Prperty.objects.filter(is_admin=1, Country__icontains='Martinique').count()
         Mauritania = Prperty.objects.filter(is_admin=1, Country__icontains='Mauritania').count()
         Mauritius = Prperty.objects.filter(is_admin=1, Country__icontains='Mauritius').count()
         Mayotte = Prperty.objects.filter(is_admin=1, Country__icontains='Mayotte').count()
         Mexico = Prperty.objects.filter(is_admin=1, Country__icontains='Mexico').count()
         Micronesia_Federated_States_of = Prperty.objects.filter(is_admin=1, Country__icontains='Micronesia, Federated States of').count()
         Moldova_Republic_of = Prperty.objects.filter(is_admin=1, Country__icontains='Moldova, Republic of').count()
         Monaco = Prperty.objects.filter(is_admin=1, Country__icontains='Monaco').count()
         Mongolia = Prperty.objects.filter(is_admin=1, Country__icontains='Mongolia').count()
         Montenegro = Prperty.objects.filter(is_admin=1, Country__icontains='Montenegro').count()
         Montserrat = Prperty.objects.filter(is_admin=1, Country__icontains='Montserrat').count()
         Morocco = Prperty.objects.filter(is_admin=1, Country__icontains='Morocco').count()
         Mozambique = Prperty.objects.filter(is_admin=1, Country__icontains='Mozambique').count()
         Myanmar = Prperty.objects.filter(is_admin=1, Country__icontains='Myanmar').count()
         Namibia = Prperty.objects.filter(is_admin=1, Country__icontains='Namibia').count()
         Nauru = Prperty.objects.filter(is_admin=1, Country__icontains='Nauru').count()
         Nepal = Prperty.objects.filter(is_admin=1, Country__icontains='Nepal').count()
         Netherlands = Prperty.objects.filter(is_admin=1, Country__icontains='Netherlands').count()
         Netherlands_Antilles = Prperty.objects.filter(is_admin=1, Country__icontains='Netherlands Antilles').count()
         New_Caledonia = Prperty.objects.filter(is_admin=1, Country__icontains='New Caledonia').count()
         New_Zealand = Prperty.objects.filter(is_admin=1, Country__icontains='New Zealand').count()
         Nicaragua = Prperty.objects.filter(is_admin=1, Country__icontains='Nicaragua').count()
         Niger = Prperty.objects.filter(is_admin=1, Country__icontains='Niger').count()
         Nigeria = Prperty.objects.filter(is_admin=1, Country__icontains='Nigeria').count()
         Niue = Prperty.objects.filter(is_admin=1, Country__icontains='Niue').count()
         Norfolk_Island = Prperty.objects.filter(is_admin=1, Country__icontains='Norfolk Island').count()
         Northern_Mariana_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Northern Mariana Islands').count()
         Norway = Prperty.objects.filter(is_admin=1, Country__icontains='Norway').count()
         Oman = Prperty.objects.filter(is_admin=1, Country__icontains='Oman').count()
         Pakistan = Prperty.objects.filter(is_admin=1, Country__icontains='Pakistan').count()
         Palau = Prperty.objects.filter(is_admin=1, Country__icontains='Palau').count()
         Palestinian = Prperty.objects.filter(is_admin=1, Country__icontains='Palestinian Territory, Occupied').count()
         Panama = Prperty.objects.filter(is_admin=1, Country__icontains='Panama').count()
         Papua_New_Guinea = Prperty.objects.filter(is_admin=1, Country__icontains='Papua New Guinea').count()
         Paraguay = Prperty.objects.filter(is_admin=1, Country__icontains='Paraguay').count()
         Peru = Prperty.objects.filter(is_admin=1, Country__icontains='Peru').count()
         Philippines = Prperty.objects.filter(is_admin=1, Country__icontains='Philippines').count()
         Pitcairn = Prperty.objects.filter(is_admin=1, Country__icontains='Pitcairn').count()
         Poland = Prperty.objects.filter(is_admin=1, Country__icontains='Poland').count()
         Portugal = Prperty.objects.filter(is_admin=1, Country__icontains='Portugal').count()
         Puerto_Rico = Prperty.objects.filter(is_admin=1, Country__icontains='Puerto Rico').count()
         Qatar = Prperty.objects.filter(is_admin=1, Country__icontains='Qatar').count()
         Reunion = Prperty.objects.filter(is_admin=1, Country__icontains='Reunion').count()
         Romania = Prperty.objects.filter(is_admin=1, Country__icontains='Romania').count()
         Russian_Federation = Prperty.objects.filter(is_admin=1, Country__icontains='Russian Federation').count()
         Rwanda = Prperty.objects.filter(is_admin=1, Country__icontains='Rwanda').count()
         Saint_Barthelemy = Prperty.objects.filter(is_admin=1, Country__icontains='Saint Barthelemy').count()
         Saint_Helena = Prperty.objects.filter(is_admin=1, Country__icontains='Saint Helena').count()
         Saint_Kitts_and_Nevis = Prperty.objects.filter(is_admin=1, Country__icontains='Saint Kitts and Nevis').count()
         Saint_Lucia = Prperty.objects.filter(is_admin=1, Country__icontains='Saint Lucia').count()
         Saint_Martin = Prperty.objects.filter(is_admin=1, Country__icontains='Saint Martin').count()
         Saint_Pierre_and_Miquelon = Prperty.objects.filter(is_admin=1, Country__icontains='Saint Pierre and Miquelon').count()
         Saint_Vincent_and_the_Grenadines = Prperty.objects.filter(is_admin=1, Country__icontains='Saint Vincent and the Grenadines').count()
         Samoa = Prperty.objects.filter(is_admin=1, Country__icontains='Samoa').count()
         San_Marino = Prperty.objects.filter(is_admin=1, Country__icontains='San Marino').count()
         Sao_Tome_and_Principe = Prperty.objects.filter(is_admin=1, Country__icontains='Sao Tome and Principe').count()
         Saudi_Arabia = Prperty.objects.filter(is_admin=1, Country__icontains='Saudi Arabia').count()
         Senegal = Prperty.objects.filter(is_admin=1, Country__icontains='Senegal').count()
         Serbia = Prperty.objects.filter(is_admin=1, Country__icontains='Serbia').count()
         Serbia_and_Montenegro = Prperty.objects.filter(is_admin=1, Country__icontains='Serbia and Montenegro').count()
         Seychelles = Prperty.objects.filter(is_admin=1, Country__icontains='Seychelles').count()
         Sierra_Leone = Prperty.objects.filter(is_admin=1, Country__icontains='Sierra Leone').count()
         Singapore = Prperty.objects.filter(is_admin=1, Country__icontains='Singapore').count()
         Sint_Maarten = Prperty.objects.filter(is_admin=1, Country__icontains='Sint Maarten').count()
         Slovakia = Prperty.objects.filter(is_admin=1, Country__icontains='Slovakia').count()
         Slovenia = Prperty.objects.filter(is_admin=1, Country__icontains='Slovenia').count()
         Solomon_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Solomon Islands').count()
         Somalia = Prperty.objects.filter(is_admin=1, Country__icontains='Somalia').count()
         South_Africa = Prperty.objects.filter(is_admin=1, Country__icontains='South Africa').count()
         South_Georgia_and_the_South_Sandwich_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='South Georgia and the South Sandwich Islands').count()
         South_Sudan = Prperty.objects.filter(is_admin=1, Country__icontains='South Sudan').count()
         Spain = Prperty.objects.filter(is_admin=1, Country__icontains='Spain').count()
         Sri_Lanka = Prperty.objects.filter(is_admin=1, Country__icontains='Sri Lanka').count()
         Sudan = Prperty.objects.filter(is_admin=1, Country__icontains='Sudan').count()
         Suriname = Prperty.objects.filter(is_admin=1, Country__icontains='Suriname').count()
         Svalbard_and_Jan_Mayen = Prperty.objects.filter(is_admin=1, Country__icontains='Svalbard and Jan Mayen').count()
         Swaziland = Prperty.objects.filter(is_admin=1, Country__icontains='Swaziland').count()
         Sweden = Prperty.objects.filter(is_admin=1, Country__icontains='Sweden').count()
         Switzerland = Prperty.objects.filter(is_admin=1, Country__icontains='Switzerland').count()
         Syrian_Arab_Republic = Prperty.objects.filter(is_admin=1, Country__icontains='Syrian Arab Republic').count()
         Taiwan = Prperty.objects.filter(is_admin=1, Country__icontains='Taiwan').count()
         Tajikistan = Prperty.objects.filter(is_admin=1, Country__icontains='Tajikistan').count()
         Tanzania = Prperty.objects.filter(is_admin=1, Country__icontains='Tanzania').count()
         Thailand = Prperty.objects.filter(is_admin=1, Country__icontains='Thailand').count()
         Timor_Leste = Prperty.objects.filter(is_admin=1, Country__icontains='Timor-Leste').count()
         Togo = Prperty.objects.filter(is_admin=1, Country__icontains='Togo').count()
         Tokelau = Prperty.objects.filter(is_admin=1, Country__icontains='Tokelau').count()
         Tonga = Prperty.objects.filter(is_admin=1, Country__icontains='Tonga').count()
         Trinidad_and_Tobago = Prperty.objects.filter(is_admin=1, Country__icontains='Trinidad and Tobago').count()
         Tunisia = Prperty.objects.filter(is_admin=1, Country__icontains='Tunisia').count()
         Turkey = Prperty.objects.filter(is_admin=1, Country__icontains='Turkey').count()
         Turkmenistan = Prperty.objects.filter(is_admin=1, Country__icontains='Turkmenistan').count()
         Turks_and_Caicos_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='Turks and Caicos Islands').count()
         Tuvalu = Prperty.objects.filter(is_admin=1, Country__icontains='Tuvalu').count()
         Uganda = Prperty.objects.filter(is_admin=1, Country__icontains='Uganda').count()
         Ukraine = Prperty.objects.filter(is_admin=1, Country__icontains='Ukraine').count()
         United_Arab_Emirates = Prperty.objects.filter(is_admin=1, Country__icontains='United Arab Emirates').count()
         United_Kingdom = Prperty.objects.filter(is_admin=1, Country__icontains='United Kingdom(UK)').count()
         United_States = Prperty.objects.filter(is_admin=1, Country__icontains='United State America').count()
         United_States_Minor_Outlying_Islands = Prperty.objects.filter(is_admin=1, Country__icontains='United States Minor Outlying Islands').count()
         Uruguay = Prperty.objects.filter(is_admin=1, Country__icontains='Uruguay').count()
         Uzbekistan = Prperty.objects.filter(is_admin=1, Country__icontains='Uzbekistan').count()
         Vanuatu = Prperty.objects.filter(is_admin=1, Country__icontains='Vanuatu').count()
         Venezuela = Prperty.objects.filter(is_admin=1, Country__icontains='Venezuela').count()
         Viet_Nam = Prperty.objects.filter(is_admin=1, Country__icontains='Viet Nam').count()
         Virgin_Islands_British = Prperty.objects.filter(is_admin=1, Country__icontains='Virgin Islands, British').count()
         Virgin_Islands_Us = Prperty.objects.filter(is_admin=1, Country__icontains='Virgin Islands, U.s.').count()
         Wallis_and_Futuna = Prperty.objects.filter(is_admin=1, Country__icontains='Wallis and Futuna').count()
         Western_Sahara = Prperty.objects.filter(is_admin=1, Country__icontains='Western Sahara').count()
         Yemen = Prperty.objects.filter(is_admin=1, Country__icontains='Yemen').count()
         Zambia = Prperty.objects.filter(is_admin=1, Country__icontains='Zambia').count()
         Zimbabwe = Prperty.objects.filter(is_admin=1, Country__icontains='Zimbabwe').count()
        
         


         #Purchase Type Count
         Rent =Prperty.objects.filter(is_admin=1, purchase_type='0').count()
         Buy =Prperty.objects.filter(is_admin=1, purchase_type='1').count()
         Auction =Prperty.objects.filter(is_admin=1, purchase_type='2').count()
         Stay =Prperty.objects.filter(is_admin=1, purchase_type='3').count()
         Featured =Prperty.objects.filter(is_admin=1, purchase_type='4').count()

         #Features Count
         Room = Prperty.objects.filter(is_admin=1, features__icontains='Living Room').count()
         Studio = Prperty.objects.filter(is_admin=1, features__icontains='Studio').count()
         Kitchen = Prperty.objects.filter(is_admin=1, features__icontains='Kitchen').count()
         Garage = Prperty.objects.filter(is_admin=1, features__icontains='Garage').count()
         Garden_f = Prperty.objects.filter(is_admin=1, features__icontains='Garden').count()
         balcony = Prperty.objects.filter(is_admin=1, features__icontains='balcony').count()
         ensuite = Prperty.objects.filter(is_admin=1, features__icontains='ensuite').count()


         #Amenities Count
         aParking = Prperty.objects.filter(is_admin=1, amenties__icontains='Parking facilities').count()
         aPlayground = Prperty.objects.filter(is_admin=1, amenties__icontains='Playground').count()
         aSwimming  = Prperty.objects.filter(is_admin=1, amenties__icontains='Swimming pool').count()
         aLaundry  = Prperty.objects.filter(is_admin=1, amenties__icontains='Laundry facilities').count()
         aOutdoor  = Prperty.objects.filter(is_admin=1, amenties__icontains='Outdoor spaces').count()
         aGym  = Prperty.objects.filter(is_admin=1, amenties__icontains='Gym').count()
         aconditioning  = Prperty.objects.filter(is_admin=1, amenties__icontains='Air conditioning').count()
         camera  = Prperty.objects.filter(is_admin=1, amenties__icontains='Security cameras').count()
         patio = Prperty.objects.filter(is_admin=1, amenties__icontains='Private patio').count()
         Ofurniture = Prperty.objects.filter(is_admin=1, amenties__icontains='Outdoor furniture').count()
         Odining = Prperty.objects.filter(is_admin=1, amenties__icontains='Outdoor dining area').count()
         Salarm = Prperty.objects.filter(is_admin=1, amenties__icontains='Smoke alarm').count()
         Calarm = Prperty.objects.filter(is_admin=1, amenties__icontains='Carbon monoxide alarm').count()
         Fextinguisher = Prperty.objects.filter(is_admin=1, amenties__icontains='Fire extinguisher').count()
         Fkit = Prperty.objects.filter(is_admin=1, amenties__icontains='First aid kit').count()
         Mview = Prperty.objects.filter(is_admin=1, amenties__icontains='Mountain view').count()
         Vview = Prperty.objects.filter(is_admin=1, amenties__icontains='Valley view').count()
         FkHeatingit = Prperty.objects.filter(is_admin=1, amenties__icontains='Heating').count()
         
         #Bedroom Count 
         bedroom1 = Prperty.objects.filter(is_admin=1, Bedroom=1).count()
         bedroom2 = Prperty.objects.filter(is_admin=1, Bedroom=2).count()
         bedroom3 = Prperty.objects.filter(is_admin=1, Bedroom=3).count()
         bedroom4 = Prperty.objects.filter(is_admin=1, Bedroom=4).count()
         bedroom5 = Prperty.objects.filter(is_admin=1, Bedroom=5).count()
         bedroom6 = Prperty.objects.filter(is_admin=1, Bedroom=6).count()
         bedroom7 = Prperty.objects.filter(is_admin=1, Bedroom=7).count()
         bedroom8 = Prperty.objects.filter(is_admin=1, Bedroom=12).count()

         #Bathroom Count 
         bathroom1 = Prperty.objects.filter(is_admin=1, bathroom=1).count()
         bathroom2 = Prperty.objects.filter(is_admin=1, bathroom=2).count()
         bathroom3 = Prperty.objects.filter(is_admin=1, bathroom=3).count()
         bathroom4 = Prperty.objects.filter(is_admin=1, bathroom=4).count()
         bathroom5 = Prperty.objects.filter(is_admin=1, bathroom=5).count()
         bathroom6 = Prperty.objects.filter(is_admin=1, bathroom=6).count()
         bathroom7 = Prperty.objects.filter(is_admin=1, bathroom=7).count()
         bathroom8 = Prperty.objects.filter(is_admin=1, bathroom=1).count()

         # Status Count 
         # Rent
         rent500 = Prperty.objects.filter(is_admin=1, purchase_type=0, amount__lte=499).count()
         rent1000 = Prperty.objects.filter(is_admin=1, purchase_type=0, amount__gte=500, amount__lte=999).count()
         rent1500 = Prperty.objects.filter(is_admin=1, purchase_type=0, amount__gte=1000, amount__lte=1499).count()
         rent2500 = Prperty.objects.filter(is_admin=1, purchase_type=0, amount__gte=1500, amount__lte=2499).count()
         rent5000 = Prperty.objects.filter(is_admin=1, purchase_type=0, amount__gte=2500,  amount__lte=4999).count()
         rent10000 = Prperty.objects.filter(is_admin=1, purchase_type=0, amount__gte=5000, amount__lte=9999).count()
         rent100001 = Prperty.objects.filter(is_admin=1, purchase_type=0, amount__gte=10000).count()

         # Buy
         buy100000 = Prperty.objects.filter(is_admin=1, purchase_type=1, amount__lte=99999).count()
         buy250000 = Prperty.objects.filter(is_admin=1, purchase_type=1, amount__gte=100000, amount__lt=250000).count()
         buy500000 = Prperty.objects.filter(is_admin=1, purchase_type=1, amount__gte=250000, amount__lt=500000).count()
         buy1000000 = Prperty.objects.filter(is_admin=1, purchase_type=1, amount__gte=500000, amount__lt=1000000).count()
         buy5000000 = Prperty.objects.filter(is_admin=1, purchase_type=1, amount__gte=1000000, amount__lte=5000000).count()
         buy10000000 = Prperty.objects.filter(is_admin=1, purchase_type=1, amount__gte=5000000, amount__lte=10000000).count()
         buy10000001 = Prperty.objects.filter(is_admin=1, purchase_type=1, amount__gte=1000000).count()

         # Auction
         auc100000 = Prperty.objects.filter(is_admin=1, purchase_type=2, amount__lt=100000).count()
         auc250000 = Prperty.objects.filter(is_admin=1, purchase_type=2, amount__gte=100000, amount__lt=250000).count()
         auc500000 = Prperty.objects.filter(is_admin=1, purchase_type=2, amount__gte=250000, amount__lt=500000).count()
         auc1000000 = Prperty.objects.filter(is_admin=1, purchase_type=2, amount__gte=500000, amount__lt=1000000).count()
         auc5000000 = Prperty.objects.filter(is_admin=1, purchase_type=2, amount__gte=1000000, amount__lt=5000000).count()
         auc10000000 = Prperty.objects.filter(is_admin=1, purchase_type=2, amount__gte=5000000, amount__lt=10000000).count()
         auc10000001 = Prperty.objects.filter(is_admin=1, purchase_type=2, amount__gte=10000000,).count()
         
         # Stay
         stay50 = Prperty.objects.filter(is_admin=1, purchase_type=3, amount__lt=50).count()
         stay100 = Prperty.objects.filter(is_admin=1, purchase_type=3, amount__gte=50, amount__lt=100).count()
         stay150 = Prperty.objects.filter(is_admin=1, purchase_type=3, amount__gte=100, amount__lt=150).count()
         stay250 = Prperty.objects.filter(is_admin=1, purchase_type=3, amount__gte=150, amount__lt=250).count()
         stay500 = Prperty.objects.filter(is_admin=1, purchase_type=3, amount__gte=250, amount__lt=500).count()
         stay1000 = Prperty.objects.filter(is_admin=1, purchase_type=3, amount__gte=500, amount__lt=1000).count()
         stay10001 = Prperty.objects.filter(is_admin=1, purchase_type=3, amount__gte=1000).count()



         data_records = Prperty.objects.all()
         type_counter = Counter()
         feature_counter = Counter()
         amenities_counter = Counter()
         country_counter = Counter()
        #  initial_count ={'0': 0, '1': 0, '2': 0}
         initial_count = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0}
         for record in data_records:
            type_list = ast.literal_eval(record.property_type)  
            type_counter.update(type_list)

         for record in data_records:
            feature_list = ast.literal_eval(record.features)  
            feature_counter.update(feature_list)

         for record in data_records:
            amenities_list = ast.literal_eval(record.amenties)  
            amenities_counter.update(amenities_list)   

         for record in data_records:
            status = record.purchase_type  
            # initial_count[status] += 1
        
        #  for record in data_records:
        #     status = str(record.purchase_type)  # Convert to string to match dictionary keys
        #     if status in initial_count:
        #         initial_count[status] += 1
        
         for record in data_records:
            country_name = record.Country  # Replace 'country' with the actual field name in your model
            country_counter.update([country_name])  



    status_labels = {'0': 'Rent', '1': 'Buy', '2': 'Auction', '3': 'Stay', '4': 'Featured'}  
    type_count = [{'value': value, 'count': count} for value, count in type_counter.items()]
    feature_count = [{'value': value, 'count': count} for value, count in feature_counter.items()]
    amenities_count = [{'value': value, 'count': count} for value, count in amenities_counter.items()]
    # status_count = [{'value': status, 'label': status_labels[status], 'count': count} for status, count in initial_count.items()]
    country_counts = [{'value': value, 'count': count} for value, count in country_counter.items()]


    #Get  Perfect Calculation________________________
   
    exterior_percentiles = database.objects.annotate(
    exterior_percentile=Window(
        expression=PercentRank(),
        order_by=F('exterior').asc()
        )
    ).filter(exterior__gt=0).values('property_id', 'exterior_percentile')

    for ext in exterior_percentiles:
        extrounded = round(ext['exterior_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=ext['property_id']).update(exterior=extrounded)



    interior =  database.objects.annotate(
    interior_percentile=Window(
        expression=PercentRank(),
        order_by=F('interior').asc()
    )).filter(interior__gt=0).values('property_id', 'interior_percentile')
    for ints in interior:
         introunded = round(ints['interior_percentile'] * 100, 2)
         PropertyPercentile.objects.filter(property_id=ints['property_id']).update(interior=introunded)


    energy =  database.objects.annotate(
    energy_percentile=Window(
        expression=PercentRank(),
        order_by=F('energy_efficiency').asc()
    )).filter(energy_efficiency__gt=0).values('property_id', 'energy_percentile')

    for enr in energy:
         enerrounded = round(enr['energy_percentile'] * 100, 2)
         PropertyPercentile.objects.filter(property_id=enr['property_id']).update(energy_efficiency=enerrounded)


    environment =  database.objects.annotate(
    env_percentile=Window(
        expression=PercentRank(),
        order_by=F('environmental_impact').asc()
    )).filter(environmental_impact__gt=0).values('property_id', 'env_percentile')
    for env in environment:
         envrounded = round(env['env_percentile'] * 100, 2)
         PropertyPercentile.objects.filter(property_id=env['property_id']).update(environmental_impact=envrounded)




    # Nearby  
    river =  database.objects.annotate(
    river_percentile=Window(
        expression=PercentRank(),
        order_by=F('riverside').desc()
    )).filter(riverside__gt=0).values('property_id', 'river_percentile')

    for riv in river:
         rivrounded = round(riv['river_percentile'] * 100, 2)
         PropertyPercentile.objects.filter(property_id=riv['property_id']).update(riverside=rivrounded)


    seaside =  database.objects.annotate(
    seaside_percentile=Window(
        expression=PercentRank(),
        order_by=F('seaside').desc()
    )).filter(seaside__gt=0).values('property_id', 'seaside_percentile')

    for sea in seaside:
         searounded = round(sea['seaside_percentile'] * 100, 2)
         PropertyPercentile.objects.filter(property_id=sea['property_id']).update(seaside=searounded)


    bar=  database.objects.annotate(
    bar_percentile=Window(
        expression=PercentRank(),
        order_by=F('bar').desc()
    )).filter(bar__gt=0).values('property_id', 'bar_percentile')

    for bir in bar:
         barrounded = round(bir['bar_percentile'] * 100, 2)
         PropertyPercentile.objects.filter(property_id=bir['property_id']).update(bar=barrounded)


    converience =  database.objects.annotate(
    converience_percentile=Window(
        expression=PercentRank(),
        order_by=F('convenience_store').desc()
    )).filter(convenience_store__gt=0).values('property_id', 'converience_percentile')

    for convince in converience:
         covrounded = round(convince['converience_percentile'] * 100, 2)
         PropertyPercentile.objects.filter(property_id=convince['property_id']).update(convenience_store=covrounded)


    gym =  database.objects.annotate(
    gym_percentile=Window(
        expression=PercentRank(),
        order_by=F('gym').desc()
    )).filter(gym__gt=0).values('property_id', 'gym_percentile')
    for gy in gym:
         gyrounded = round(gy['gym_percentile'] * 100, 2)
         PropertyPercentile.objects.filter(property_id=gy['property_id']).update(gym=gyrounded)


    fire =  database.objects.annotate(
    fire_percentile=Window(
        expression=PercentRank(),
        order_by=F('fire_station').desc()
    )).filter(fire_station__gt=0).values('property_id', 'fire_percentile')

    for fir in fire:
         firrounded = round(fir['fire_percentile'] * 100, 2)
         PropertyPercentile.objects.filter(property_id=fir['property_id']).update(fire_station=firrounded)


    hospital =  database.objects.annotate(
    hospital_percentile=Window(
        expression=PercentRank(),
        order_by=F('hospital').desc()
    )).filter(hospital__gt=0).values('property_id', 'hospital_percentile')

    for hos in hospital:
        hosrounded = round(hos['hospital_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=hos['property_id']).update(hospital=hosrounded)


    nursery =  database.objects.annotate(
    nursery_percentile=Window(
        expression=PercentRank(),
        order_by=F('nursery').desc()
    )).filter(nursery__gt=0).values('property_id', 'nursery_percentile')

    for nurse in nursery:
        nurserounded = round(nurse['nursery_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=nurse['property_id']).update(nursery=nurserounded)

    park =  database.objects.annotate(
    park_percentile=Window(
        expression=PercentRank(),
        order_by=F('park').desc()
    )).filter(park__gt=0).values('property_id', 'park_percentile')

    for par in park:
        parkrounded = round(par['park_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=par['property_id']).update(park=parkrounded)


    petrol =  database.objects.annotate(
    petrol_percentile=Window(
        expression=PercentRank(),
        order_by=F('petrol_station').desc()
    )).filter(petrol_station__gt=0).values('property_id', 'petrol_percentile')

    for pert in petrol:
        petrolrounded = round(pert['petrol_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=pert['property_id']).update(petrol_station=petrolrounded)


    police =  database.objects.annotate(
    police_percentile=Window(
        expression=PercentRank(),
        order_by=F('police_station').desc()
    )).filter(police_station__gt=0).values('property_id', 'police_percentile')

    for pol in police:
        polrounded = round(pol['police_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=pol['property_id']).update(police_station=polrounded)


    restaurant =  database.objects.annotate(
    restaurant_percentile=Window(
        expression=PercentRank(),
        order_by=F('restaurant').desc()
    )).filter(restaurant__gt=0).values('property_id', 'restaurant_percentile')

    for rest in restaurant:
        resrounded = round(rest['restaurant_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=rest['property_id']).update(restaurant=resrounded)


    school =  database.objects.annotate(
    school_percentile=Window(
        expression=PercentRank(),
        order_by=F('school').desc()
    )).filter(school__gt=0).values('property_id', 'school_percentile')

    for sch in school:
        schrounded = round(sch['school_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=sch['property_id']).update(school=schrounded)


    market =  database.objects.annotate(
    market_percentile=Window(
        expression=PercentRank(),
        order_by=F('super_market').desc()
    )).filter(super_market__gt=0).values('property_id', 'market_percentile')

    for mar in market:
        markrounded = round(mar['market_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=mar['property_id']).update(super_market=markrounded)



    # Sizes
    floor =  database.objects.annotate(
    floor_percentile=Window(
        expression=PercentRank(),
        order_by=F('floor_area').asc()
    )).filter(floor_area__gt=0).values('property_id', 'floor_percentile')

    for flow in floor:
        flowrounded = round(flow['floor_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=flow['property_id']).update(floor_area=flowrounded)


    sitearea =  database.objects.annotate(
    site_percentile=Window(
        expression=PercentRank(),
        order_by=F('site_area').asc()
    )).filter(site_area__gt=0).values('property_id', 'site_percentile')

    for site in sitearea:
        siterounded = round(site['site_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=site['property_id']).update(site_area=siterounded)



    kitchen =  database.objects.annotate(
    kitchen_percentile=Window(
        expression=PercentRank(),
        order_by=F('kitchen').asc()
    )).filter(kitchen__gt=0).values('property_id', 'kitchen_percentile')

    for kit in kitchen:
        kitrounded = round(kit['kitchen_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=kit['property_id']).update(kitchen=kitrounded)


    living =  database.objects.annotate(
    living_percentile=Window(
        expression=PercentRank(),
        order_by=F('living_room').asc()
    )).filter(living_room__gt=0).values('property_id', 'living_percentile') 

    for liv in living:
        livrounded = round(liv['living_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=liv['property_id']).update(living_room=livrounded)


    bedrooms1 =  database.objects.annotate(
    bedroom1_percentile=Window(
        expression=PercentRank(),
        order_by=F('bedroom1').asc()
    )).filter(bedroom1__gt=0).values('property_id', 'bedroom1_percentile')

    for bed1 in bedrooms1:
        bedorounded = round(bed1['bedroom1_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=bed1['property_id']).update(bedroom1=bedorounded)


    bedrooms2 =  database.objects.annotate(
    bedroom2_percentile=Window(
        expression=PercentRank(),
        order_by=F('bedroom2').asc()
    )).filter(bedroom2__gt=0).values('property_id', 'bedroom2_percentile')

    for bed2 in bedrooms2:
        bedtrounded = round(bed2['bedroom2_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=bed2['property_id']).update(bedroom2=bedtrounded)

    bedrooms3 =  database.objects.annotate(
    bedroom3_percentile=Window(
        expression=PercentRank(),
        order_by=F('bedroom3').asc()
    )).filter(bedroom3__gt=0).values('property_id', 'bedroom3_percentile')

    for bed3 in bedrooms3:
        bedthrounded = round(bed3['bedroom3_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=bed3['property_id']).update(bedroom3=bedthrounded)


    #Transport 
    airport =  database.objects.annotate(
    airport_percentile=Window(
        expression=PercentRank(),
        order_by=F('airport').desc()
    )).filter(airport__gt=0).values('property_id', 'airport_percentile')

    for air in airport:
        airrounded = round(air['airport_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=air['property_id']).update(airport=airrounded)

    bus_stop=  database.objects.annotate(
    bus_stop_percentile=Window(
        expression=PercentRank(),
        order_by=F('bus_stop').desc()
    )).filter(bus_stop__gt=0).values('property_id', 'bus_stop_percentile')

    for bus in bus_stop:
        busrounded = round(bus['bus_stop_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=bus['property_id']).update(bus_stop=busrounded)

    train_station =  database.objects.annotate(
    train_station_percentile=Window(
        expression=PercentRank(),
        order_by=F('train_station').desc()
    )).filter(train_station__gt=0).values('property_id', 'train_station_percentile')

    for train in train_station:
        trainrounded = round(train['train_station_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=train['property_id']).update(train_station=trainrounded)

    underground_station =  database.objects.annotate(
    underground_station_percentile=Window(
        expression=PercentRank(),
        order_by=F('underground_station').desc()
    )).filter(underground_station__gt=0).values('property_id', 'underground_station_percentile')

    for under in underground_station:
        underrounded = round(under['underground_station_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=under['property_id']).update(underground_station=underrounded)


    CityNames = database.objects.values('city').annotate(name_count=Count('city')).order_by('-name_count', 'city')



    for property in properties:
        database_title =database.objects.filter(property_id=property.id).first()
        if property.hide == "on":
           ini_string = database_title.name
           property.name = ''.join([i for i in ini_string if not i.isdigit()])
        else:  
            property.name = database_title.name

        
          

    return render(request, 'testfilter.html', {'CityNames':CityNames,'country_counts': country_counts,
                                                     'amenities_count': amenities_count,
                                                     'feature_count': feature_count,'type_count': type_count,'properties': properties, 'asia': asia,
                                                     'europe':europe, 'africa':africa, 'antractica':antractica, 'north_america':north_america, 
                                                     'south_america':south_america, 'australia':australia, 'Duplex': Duplex ,'Garden':Garden,
                                                     'Highrise':Highrise, 'House':House, 'Apartment':Apartment, 'Lowrise':Lowrise,'Flat':Flat, 'Bungalow': Bungalow, 'Joint':Joint, 'Luxury': Luxury,
                                                     'Rent':Rent, 'Buy':Buy, 'Auction':Auction, 'Stay':Stay, 'Featured':Featured,
                                                     'Room':Room, 'Studio':Studio, 'Kitchen':Kitchen, 'Garage':Garage, 'Garden_f':Garden_f, 
                                                     'aParking':aParking, 'aPlayground':aPlayground,"camera":camera,'patio':patio, 'Ofurniture':Ofurniture,
                                                     'Odining':Odining,'Salarm':Salarm, 'Calarm':Calarm,'Fextinguisher':Fextinguisher,'Fkit':Fkit ,'Mview':Mview,
                                                     'Vview':Vview,'FkHeatingit':FkHeatingit, 'aSwimming':aSwimming, 'aLaundry':aLaundry, 'aOutdoor':aOutdoor,
                                                     'aGym':aGym, 'aconditioning':aconditioning, 'bedroom1':bedroom1, 'bedroom2': bedroom2, 'bedroom3':bedroom3,
                                                     'bedroom4':bedroom4, 'bedroom5':bedroom5, 'bedroom6':bedroom6,'bedroom7':bedroom7,  'bedroom8':bedroom8,
                                                     'bathroom1' :bathroom1, 'bathroom2':bathroom2, 'bathroom3':bathroom3, 'bathroom4':bathroom4, 'bathroom5':bathroom5,
                                                     'bathroom6':bathroom6 ,'bathroom7':bathroom7, 'bathroom8': bathroom8,  'balcony':balcony, 'ensuite': ensuite,'Afghanistan': Afghanistan,
                                                      'Aland_Islands':Aland_Islands,'Albania':Albania,'Algeria':Algeria,'American_Samoa':American_Samoa,'Andorra':Andorra,'Angola':Angola,'Anguilla':Anguilla,'Antarctica':Antarctica,'Antigua_and_Barbuda':Antigua_and_Barbuda,'Argentina':Argentina,'Armenia':Armenia,'Aruba':Aruba,'Australia':Australia,'Austria':Austria,'Azerbaijan' :Azerbaijan ,'Bahamas': Bahamas,
    'Bahrain': Bahrain,
    'Bangladesh': Bangladesh,
    'Barbados': Barbados,
    'Belarus': Belarus,
    'Belgium': Belgium,
    'Belize': Belize,
    'Benin': Benin,
    'Bermuda': Bermuda,
    'Bhutan': Bhutan,
    'Bolivia': Bolivia,
    'Bonaire_Sint_Eustatius_Saba': Bonaire_Sint_Eustatius_Saba,
    'Bosnia_and_Herzegovina': Bosnia_and_Herzegovina,
    'Botswana': Botswana,
    'Bouvet_Island': Bouvet_Island,
    'Brazil': Brazil,
    'British_Indian_Ocean_Territory': British_Indian_Ocean_Territory,
    'Brunei_Darussalam': Brunei_Darussalam,
    'Bulgaria': Bulgaria,
    'Burkina_Faso': Burkina_Faso,
    'Burundi': Burundi ,'Cambodia': Cambodia,
    'Cameroon': Cameroon,
    'Canada': Canada,
    'Cape_Verde': Cape_Verde,
    'Cayman_Islands': Cayman_Islands,
    'Central_African_Republic': Central_African_Republic,
    'Chad': Chad,
    'Chile': Chile,
    'China': China,
    'Cocos_Islands': Cocos_Islands,
    'Colombia': Colombia,
    'Comoros': Comoros,
    'Congo': Congo,
    'Republic_of_the_Congo': Republic_of_the_Congo,
    'Cook_Islands ': Cook_Islands,
    'Costa_Rica': Costa_Rica,
    "Cote_DIvoire": Cote_DIvoire,
    'Croatia': Croatia,
    'Cuba': Cuba,
    'Curacao': Curacao,
    'Cyprus': Cyprus,
    'Czech_Republic': Czech_Republic,
    'Denmark': Denmark,
    'Djibouti': Djibouti,
    'Dominica': Dominica,
    'Dominican_Republic': Dominican_Republic,
    'Ecuador': Ecuador,
    'Egypt': Egypt,
    'El_Salvador': El_Salvador,
    'Equatorial_Guinea': Equatorial_Guinea,
    'Eritrea': Eritrea,
    'Estonia': Estonia,
    'Ethiopia': Ethiopia,
    'Falkland_Islands': Falkland_Islands,
    'Faroe_Islands': Faroe_Islands,
    'Fiji': Fiji,
    'Finland': Finland,
    'France': France,
    'French_Guiana': French_Guiana,
    'French_Polynesia': French_Polynesia,
    'French_Southern_Territories': French_Southern_Territories ,'Gabon': Gabon,
    'Gambia': Gambia,
    'Georgia': Georgia,
    'Germany': Germany,
    'Ghana': Ghana,
    'Gibraltar': Gibraltar,
    'Greece': Greece,
    'Greenland': Greenland,
    'Grenada': Grenada,
    'Guadeloupe': Guadeloupe,
    'Guam': Guam,
    'Guatemala': Guatemala,
    'Guernsey': Guernsey,
    'Guinea': Guinea,
    'Guinea_Bissau': Guinea_Bissau,
    'Guyana': Guyana,
    'Haiti': Haiti,
    'Heard_Island_and_Mcdonald_Islands': Heard_Island_and_Mcdonald_Islands,
    'Holy_See': Holy_See,
    'Honduras': Honduras,
    'Hong Kong': Hong_Kong,
    'Hungary': Hungary,
    'Iceland': Iceland,
    'India': India,
    'Indonesia': Indonesia,
    'Iran': Iran,
    'Iraq': Iraq,
    'Ireland': Ireland,
    'Isle_of_Man': Isle_of_Man,
    'Israel': Israel,
    'Italy': Italy,
    'Jamaica': Jamaica,
    'Japan': Japan,
    'Jersey': Jersey,
    'Jordan': Jordan,
    'Kazakhstan': Kazakhstan,
    'Kenya': Kenya,
    'Kiribati': Kiribati,
    'Korea': Korea,
    'Kosovo': Kosovo,
    'Kuwait': Kuwait,
    'Kyrgyzstan': Kyrgyzstan,
    "Lao_People_Democratic_Republic": Lao_People_Democratic_Republic,
    'Latvia': Latvia,
    'Lebanon': Lebanon,
    'Lesotho': Lesotho,
    'Liberia': Liberia,
    'Libyan_Arab_Jamahiriya': Libyan_Arab_Jamahiriya,
    'Liechtenstein': Liechtenstein,
    'Lithuania': Lithuania,
    'Luxembourg': Luxembourg,
    'Macao': Macao,
    'Macedonia': Macedonia,
    'Madagascar': Madagascar,
    'Malawi': Malawi,
    'Malaysia': Malaysia,
    'Maldives': Maldives,
    'Mali': Mali,
    'Malta': Malta,
    'Marshall_Islands': Marshall_Islands,
    'Martinique': Martinique,
    'Mauritania': Mauritania,
    'Mauritius': Mauritius,
    'Mayotte': Mayotte,
    'Mexico': Mexico,
    'Micronesia_Federated_States_of': Micronesia_Federated_States_of,
    'Moldova_Republic_of': Moldova_Republic_of,
    'Monaco': Monaco,
    'Mongolia': Mongolia,
    'Montenegro': Montenegro,
    'Montserrat': Montserrat,
    'Morocco': Morocco,
    'Mozambique': Mozambique,
    'Myanmar': Myanmar ,'Namibia': Namibia,
    'Nauru': Nauru,
    'Nepal': Nepal,
    'Netherlands': Netherlands,
    'Netherlands_Antilles': Netherlands_Antilles,
    'New_Caledonia': New_Caledonia,
    'New_Zealand': New_Zealand,
    'Nicaragua': Nicaragua,
    'Niger': Niger,
    'Nigeria': Nigeria,
    'Niue': Niue,
    'Norfolk_Island': Norfolk_Island,
    'Northern_Mariana_Islands': Northern_Mariana_Islands,
    'Norway': Norway,
    'Oman': Oman,
    'Pakistan': Pakistan,
    'Palau': Palau,
    'Palestinian': Palestinian,
    'Panama': Panama,
    'Papua New Guinea': Papua_New_Guinea,
    'Paraguay': Paraguay,
    'Peru': Peru,
    'Philippines': Philippines,
    'Pitcairn': Pitcairn,
    'Poland': Poland,
    'Portugal': Portugal,
    'Puerto_Rico': Puerto_Rico,
    'Qatar': Qatar,
    'Reunion': Reunion,
    'Romania': Romania,
    'Russian_Federation': Russian_Federation,
    'Rwanda': Rwanda,
    'Saint_Barthelemy': Saint_Barthelemy,
    'Saint_Helena': Saint_Helena,
    'Saint_Kitts_and_Nevis': Saint_Kitts_and_Nevis,
    'Saint_Lucia': Saint_Lucia,
    'Saint_Martin': Saint_Martin,
    'Saint_Pierre_and_Miquelon': Saint_Pierre_and_Miquelon,
    'Saint_Vincent_and_the_Grenadines': Saint_Vincent_and_the_Grenadines,
    'Samoa': Samoa,
    'San_Marino': San_Marino,
    'Sao_Tome_and_Principe': Sao_Tome_and_Principe,
    'Saudi_Arabia': Saudi_Arabia,
    'Senegal': Senegal,
    'Serbia': Serbia,
    'Serbia_and_Montenegro': Serbia_and_Montenegro,
    'Seychelles': Seychelles,
    'Sierra_Leone': Sierra_Leone,
    'Singapore': Singapore,
    'Sint_Maarten': Sint_Maarten,
    'Slovakia': Slovakia,
    'Slovenia': Slovenia,
    'Solomon Islands': Solomon_Islands,
    'Somalia': Somalia,
    'South_Africa': South_Africa,
    'South_Georgia_and_the_South_Sandwich_Islands': South_Georgia_and_the_South_Sandwich_Islands,
    'South_Sudan': South_Sudan,
    'Spain': Spain,
    'Sri_Lanka': Sri_Lanka,
    'Sudan': Sudan,
    'Suriname': Suriname,
    'Svalbard_and_Jan_Mayen': Svalbard_and_Jan_Mayen,
    'Swaziland': Swaziland,
    'Sweden': Sweden,
    'Switzerland': Switzerland,
    'Syrian_Arab_Republic': Syrian_Arab_Republic, 'Taiwan': Taiwan,
    'Tajikistan': Tajikistan,
    'Tanzania': Tanzania,
    'Thailand': Thailand,
    'Timor_Leste': Timor_Leste,
    'Togo': Togo,
    'Tokelau': Tokelau,
    'Tonga': Tonga,
    'Trinidad_and_Tobago': Trinidad_and_Tobago,
    'Tunisia': Tunisia,
    'Turkey': Turkey,
    'Turkmenistan': Turkmenistan,
    'Turks_and_Caicos_Islands': Turks_and_Caicos_Islands,
    'Tuvalu': Tuvalu,
    'Uganda': Uganda,
    'Ukraine': Ukraine,
    'United_Arab_Emirates': United_Arab_Emirates,
    'United_Kingdom': United_Kingdom,
    'United_States': United_States,
    'United_States_Minor_Outlying_Islands': United_States_Minor_Outlying_Islands,
    'Uruguay': Uruguay,
    'Uzbekistan': Uzbekistan,
    'Vanuatu': Vanuatu,
    'Venezuela': Venezuela,
    'Viet_Nam': Viet_Nam,
    'Virgin_Islands_British': Virgin_Islands_British,
    'Virgin_Islands_Us': Virgin_Islands_Us,
    'Wallis_and_Futuna': Wallis_and_Futuna,
    'Western_Sahara': Western_Sahara,
    'Yemen': Yemen,
    'Zambia': Zambia,
    'Zimbabwe': Zimbabwe, 

    'rent500': rent500,
    'rent1000': rent1000,
    'rent1500': rent1500,
    'rent2500': rent2500,
    'rent5000': rent5000,
    'rent10000': rent10000,
    'rent100001' : rent100001, 

    'buy100000':buy100000,
    'buy250000':buy250000,
    'buy500000':buy500000,
    'buy1000000':buy1000000,
    'buy5000000':buy5000000,
    'buy10000000':buy10000000,
    'buy10000001' : buy10000001, 

    'auc100000': auc100000,                            
    'auc250000':  auc250000,
    'auc500000': auc500000,
    'auc1000000': auc1000000,               
    'auc5000000': auc5000000,               
    'auc10000000': auc10000000,              
    'auc10000001': auc10000001, 

    'stay50': stay50,              
    'stay100': stay100,              
    'stay150': stay150,              
    'stay250': stay250,              
    'stay500': stay500,              
    'stay1000': stay1000,              
    'stay10001': stay10001,              
                                                     })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def UploadProperty(request):
    return render(request, 'add_property.html')

def testform(request):
    return render(request, 'testform.html')

def get_city(request):
    if is_ajax(request):
        city = request.GET.get("city", '')
        city_list= []
        if city:
            properties = PropertyPercentile.objects.filter(address__icontains=city)
            for property in properties:
                city_list.append({
                    'cities': property.address,
                })

            
        return JsonResponse({'item': city_list})
    else:
        return HttpResponse("This is not an AJAX request")          

def is_ajax(request):
     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
   


def GetData(request):
    continent_val= request.GET.getlist("continent_val[]", '')
    country_val= request.GET.get("country_val", '')
    country_list=[]
    city_list=[]
    continent_str = ', '.join(continent_val)
    continent_list = continent_str.split(', ') 
    if continent_val:
       countries = database.objects.filter(continent__in=continent_list, is_admin=1).values('country').annotate(country_count=Count('country'))

       titles = database.objects.filter(continent__in=continent_list).values('city').annotate(title_count=Count('city')).order_by('-title_count', 'city')

       for country in countries:

           country_list.append({
            'countries': country['country'],
            'country_count': country['country_count']
           }) 

       for title in titles:
            city_list.append({
            'title': title['city'],
            'title_count': title['title_count']
          }) 

       return JsonResponse({'country_list': country_list, 'city_list': city_list}) 
    if country_val:  
        titles = database.objects.filter(country=country_val).values('city').annotate(title_count=Count('city')).order_by('-title_count', 'city')
        city_list=[]
        for title in titles:
          
            city_list.append({
            
            'title': title['city'],
            'title_count': title['title_count']
          })
        return JsonResponse({'city_list': city_list}) 

    else:  
       countries = database.objects.values('country').annotate(country_count=Count('country'))

       titles = database.objects.values('city').annotate(title_count=Count('city')).order_by('-title_count', 'city')

       for country in countries:
           country_list.append({
            'countries': country['country'],
            'country_count': country['country_count']
           }) 

       for title in titles:
            city_list.append({
            'title': title['city'],
            'title_count': title['title_count']
          }) 

       return JsonResponse({'country_list': country_list, 'city_list': city_list})   


def multiple(request):
    return render(request, 'multiple.html')

def cities(request):
    return render(request, 'getcity.html')


def get_cities_by_country(request):
    base_url = 'http://api.geonames.org/searchJSON'

    country_name = request.GET.get("country_name", '')

    params = {
        'q': country_name,
        'maxRows': 100, 
        'username': 'vishal074',
        'type': 'json',
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        # Filter cities based on a population threshold (e.g., 500,000)
        min_population_threshold = 500000
        cities = [
            {
                'city': result.get('toponymName', ''),
                'population': result.get('population', 0)
            }
            for result in data.get('geonames', [])
            if result.get('population', 0) >= min_population_threshold
        ]

        city_list = []
        if cities:
            for city in cities:
                city_list.append({
                    'cityname': city['city'],
                    'population': city['population'],
                })

            return JsonResponse({'city_list': city_list})
        else:
            return JsonResponse({'message': f"No big cities found for {country_name}"}, status=404)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return JsonResponse({'message': 'Failed to retrieve data'}, status=response.status_code)
