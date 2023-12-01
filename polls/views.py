from queue import Empty
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
import numpy as np
from django.db.models import F, Window
from django.db.models.functions import PercentRank
from django.db.models import F
from django.db.models import Avg
from django.db import connection
from .models import (
    index,
    category,
    Contact,
    Prperty,
    Propertyuser,
    CustomUser,
    database,
    Rating,
    Entry,
    PropertyPercentile
    
)
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
# from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers
from django.db.models import F, ExpressionWrapper,Func, fields
# admin functions_________________________________________________________________________________________________

# LOGIN AND AUTHENTICATION==============================================================


def admin_login(request):
    if request.method == "GET":
        context = ""
        return render(request, "admin/login.html", {"context": context})

    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return HttpResponseRedirect("dashboard/")

        elif user is not None and user.is_staff:
            login(request, user)
            return HttpResponseRedirect("dashboard/")

        else:
            context = {"error": "Please enter valid credentials"}  # to display error?
            return render(request, "admin/login.html", {"context": context})


def admin_logout(request):
    logout(request)
    return redirect("admin")


def dashboard(request):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    users = CustomUser.objects.filter(is_superuser=0)
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    dbcount = database.objects.all().count()
    name = CustomUser.objects.filter(is_staff=1)
    approved_count = Prperty.objects.filter(is_admin=1).count()
    # print(is_superuser)
    # return HttpResponse(is_superuser)
    return render(
        request,
        "admin/AdminBase.html",
        {
            "users": users,
            "properties": properties,
            "index_count": index_count,
            "is_superuser": is_superuser,
            "dbcount": dbcount,
            "name": name,
            "approved_count": approved_count,
        },
    )


# INDEX====================================================================================
def ad_index(request):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    st = index.objects.all()
    for sin in st:
        count = category.objects.filter(index_id=sin.id)
        sin.cat_count = count.count()

    cat = category.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()
    return render(
        request,
        "admin/index/index.html",
        {
            "st": st,
            "cat": cat,
            "users": users,
            "properties": properties,
            "is_superuser": is_superuser,
            "count": count,
            "index_count": index_count,
            "dbcount": dbcount,
            "approved_count" : approved_count,
        },
    )


def ad_index_add(request):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser
    else:
        is_superuser = False

    index_count = index.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    properties = Prperty.objects.all()
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()

    if request.method == "POST":
        name = request.POST.get("name")
        active = request.POST.get("active")
        image = request.FILES.get("image")

        if name and active and image:
            index.objects.create(
                name=name,
                active=active,
                image=image,
            )
            context = {"success": "Successfully submitted details !!"}
        else:
            context = {"error": "Missing form data."}

    else:
        context = {}

    return render(
        request,
        "admin/index/add.html",
        {
            "context": context,
            "is_superuser": is_superuser,
            "index_count": index_count,
            "users": users,
            "properties": properties,
            "dbcount": dbcount,
            "approved_count":approved_count,
        },
    )


def ad_index_edit(request, id):
    try:
        user = request.user

        if user.is_authenticated:
            is_superuser = user.is_superuser

        indexObj = index.objects.get(id=id)
        index_count = index.objects.all()
        users = CustomUser.objects.filter(is_superuser=0)
        properties = Prperty.objects.all()
        dbcount = database.objects.all().count()
        approved_count = Prperty.objects.filter(is_admin=1).count()
        if request.method == "POST":
            indexObj.name = request.POST["name"]
            indexObj.active = request.POST["active"]
            image = request.FILES.get("image")
            if image:
                indexObj.image = image
            indexObj.save()

            context = {"success": "Successfully updated details !!"}
            return render(
                request,
                "admin/index/edit.html",
                {
                    "context": context,
                    "indexObj": indexObj,
                    "is_superuser": is_superuser,
                    "users": users,
                    "properties": properties,
                    "index_count": index_count,
                    "dbcount": dbcount,
                    "approved_count" : approved_count,
                },
            )

        elif request.method == "GET":
            return render(
                request,
                "admin/index/edit.html",
                {
                    "indexObj": indexObj,
                    "is_superuser": is_superuser,
                    "users": users,
                    "properties": properties,
                    "index_count": index_count,
                    "dbcount": dbcount,
                    "approved_count" : approved_count,
                },
            )

    except index.DoesNotExist:
        context = {"error": "Data has not been submitted."}
        return render(
            request,
            "admin/index/edit.html",
            {
                "context": context,
                "is_superuser": is_superuser,
                "users": users,
                "properties": properties,
                "index_count": index_count,
                "dbcount": dbcount,
                "approved_count" : approved_count,
            },
        )


def ad_index_delete(request, id):
    record = get_object_or_404(index, id=id)
    record.delete()
    return JsonResponse({"success": "success"})

    return JsonResponse({"error": "error"})


# CATEGORY====================================================================================
def ad_category(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    cat = category.objects.filter(index_id=id)
    indexObj = index.objects.get(id=id)
    users = CustomUser.objects.filter(is_superuser=0)
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()
    return render(
        request,
        "admin/category/index.html",
        {
            "indexObj": indexObj,
            "cat": cat,
            "users": users,
            "properties": properties,
            "is_superuser": is_superuser,
            "index_count": index_count,
            "dbcount": dbcount,
            "approved_count":approved_count,
        },
    )


def ad_category_add(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    indexObj = index.objects.get(id=id)
    index_count = index.objects.all()
    properties = Prperty.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()

    if request.method == "POST":
        name = request.POST["name"]
        active = request.POST["active"]
        index_id = request.POST["index_id"]
        image = request.FILES["image"]

        category.objects.create(
            name=name, active=active, image=image, index_id=index_id
        )
        context = {"success": "Successfully submitted details !!"}
        return render(
            request,
            "admin/category/add.html",
            {
                "context": context,
                "indexObj": indexObj,
                "is_superuser": is_superuser,
                "index_count": index_count,
                "properties": properties,
                "users": users,
                "dbcount": dbcount,
                "approved_count": approved_count,
            },
        )

        context = {"error": "Data has not been submitted."}
        return render(
            request,
            "admin/category/add.html",
            {"context": context, "is_superuser": is_superuser},
        )

    elif request.method == "GET":
        context = ""
        return render(
            request,
            "admin/category/add.html",
            {
                "context": context,
                "indexObj": indexObj,
                "is_superuser": is_superuser,
                "index_count": index_count,
                "properties": properties,
                "users": users,
                "dbcount": dbcount,
                "approved_count": approved_count,
            },
        )


def ad_category_edit(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    cat = category.objects.get(id=id)
    indexObj = index.objects.filter(id=cat.index_id).first()
    index_count = index.objects.all()
    properties = Prperty.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()

    try:
        if request.method == "POST":
            cat.name = request.POST["name"]
            cat.active = request.POST["active"]
            image = request.FILES.get("image")
            if image:
                cat.image = image
            cat.save()

            context = {"success": "Successfully updated details !!"}
            return render(
                request,
                "admin/category/edit.html",
                {
                    "context": context,
                    "cat": cat,
                    "indexObj": indexObj,
                    "is_superuser": is_superuser,
                    "index_count": index_count,
                    "properties": properties,
                    "users": users,
                    "dbcount": dbcount,
                    "approved_count":approved_count,
                },
            )

        elif request.method == "GET":
            return render(
                request,
                "admin/category/edit.html",
                {
                    "cat": cat,
                    "indexObj": indexObj,
                    "is_superuser": is_superuser,
                    "index_count": index_count,
                    "properties": properties,
                    "users": users,
                    "dbcount": dbcount,
                    "approved_count":approved_count,
                },
            )

    except index.DoesNotExist:
        context = {"error": "Data has not been submitted."}
        return render(
            request,
            "admin/category/edit.html",
            {
                "context": context,
                "cat": cat,
                "indexObj": indexObj,
                "is_superuser": is_superuser,
                "index_count": index_count,
                "properties": properties,
                "users": users,
                "dbcount": dbcount,
                "approved_count": approved_count,
            },
        )


def ad_category_delete(request, id):
    record = get_object_or_404(category, id=id)
    record.delete()
    return JsonResponse({"success": "success"})

    return JsonResponse({"error": "error"})


# USER====================================================================================
def admin_user(request):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    users = CustomUser.objects.filter(is_superuser=0)
    properties = Prperty.objects.all()
    return render(
        request,
        "admin/user/user.html",
        {"users": users, "properties": properties, "is_superuser": is_superuser},
    )


def admin_user_add(request):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    users = CustomUser.objects.filter(is_superuser=0)
    index_count = index.objects.all()
    properties = Prperty.objects.all()
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()
    return render(
        request,
        "admin/user/add.html",
        {
            "users": users,
            "index_count": index_count,
            "properties": properties,
            "is_superuser": is_superuser,
            "dbcount": dbcount,
            "approved_count": approved_count,
        },
    )


# Property section==============================================================================


def viewproperties(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    properties = Prperty.objects.filter(id=id)
    users = CustomUser.objects.filter(is_superuser=0)
    return render(
        request,
        "admin/user/properties.html",
        {"properties": properties, "users": users, "is_superuser": is_superuser},
    )


def activate(request, id):
    property_obj = Prperty.objects.filter(id=id).update(is_admin="1")

    properties = Prperty.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    return redirect("properties")


def deactivate(request, id):
    property_obj = Prperty.objects.filter(id=id).update(is_admin="0")
    users = CustomUser.objects.filter(is_superuser=0)
    properties = Prperty.objects.all()
    return redirect("properties")


def properties(request):
    properties_data = Propertyuser.objects.all().order_by("-id")
    properties = Prperty.objects.all()
    # latest_prop = reversed(list(Propertyuser.objects.all()))
    properties = Prperty.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    index_count = index.objects.all()
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()


    for property in properties_data:
        prop = Prperty.objects.filter(user_id=property.id).first()
        count = Prperty.objects.filter(user_id=property.id).count()

        if prop is not None:
            property.property_id = prop.id
            property.property_count = count
        else:
            property.property_id = 0

    user = request.user
    is_superuser = user.is_authenticated and user.is_superuser

    page = request.GET.get("page", 1)
    properties_per_page = 50

    paginator = Paginator(properties_data, properties_per_page)

    try:
        properties_data = paginator.page(page)
    except PageNotAnInteger:
        properties_data = paginator.page(1)
    except EmptyPage:
        properties_data = paginator.page(paginator.num_pages)

    return render(
        request,
        "admin/property/property.html",
        {
            "properties_data": properties_data,
            "properties": properties,
            "users": users,
            "is_superuser": is_superuser,
            "index_count": index_count,
            "dbcount": dbcount,
            "approved_count" : approved_count,
        },
    )


# def properties(request):
#     property_users = Propertyuser.objects.all()

#     for property_user in property_users:
#         property_list = Prperty.objects.filter(user_id=property_user.id).first()
#         count = Prperty.objects.filter(user_id=property_user.id).count()

#         if property_list is not None:
#             id = property_list.id
#             property_user.property_id = id
#             property_user.property_count = count
#         else:
#             property_user.property_id = 0
#             property_user.property_count = 0

#     user = request.user

#     if user.is_authenticated:
#         is_superuser = user.is_superuser

#     page = request.GET.get("page", 1)  # Get the page parameter from the query string
#     properties_per_page = 10  # Number of properties to display per page

#     properties = Propertyuser.objects.all()

#     users = CustomUser.objects.filter(is_superuser=0)

#     # Paginate the properties based on the page parameter
#     paginator = Paginator(properties, properties_per_page)
#     try:
#         properties = paginator.page(page)
#     except PageNotAnInteger:
#         properties = paginator.page(1)
#     except EmptyPage:
#         properties = paginator.page(paginator.num_pages)

#     return render(
#         request,
#         "admin/property/property.html",
#         {"properties": properties, "users": users, "is_superuser": is_superuser},
#     )


def adminproperty(request):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    if request.method == "POST":
        index = request.POST.get("index", "")
        category = request.POST.get("category", "")  # Assign a value to category
        weburl = request.POST.get("weburl", "")
        address = request.POST.get("address", "")
        # title = request.POST.get('title', '')
        image = request.FILES["image"]
        purchase_type = request.POST.get("purchase_type", "")
        floor_area = request.POST.get("floor_area", "")
        property_type = request.POST.getlist("property_type", "")
        Bedroom = request.POST.get("Bedroom", "")
        bathroom = request.POST.get("bathroom", "")
        amenties = request.POST.getlist("amenties")
        features = request.POST.getlist("features")
        duration = request.POST.get("duration", "")
        amount = request.POST.get("amount", "")
        floor_area_value = request.POST.get("floor_area_value", "")
        site_area = request.POST.get("site_area", "")
        site_area_value = request.POST.get("site_area_value", "")
        country = request.POST.get("country", "")
        continent = request.POST.get("continent", "")
        hide = request.POST.get("hide", "")
        is_admin = "1"

        # Store user data in second model
        name = request.POST.get("name", "")
        company_name = request.POST.get("company_name", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")

        words = address.split()
        first_few_words = " ".join(words[:3])

        Addproperty = Prperty.objects.create(
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
        )

        property_user = Propertyuser.objects.create(
            property_id=Addproperty.id,  # Save the Prperty object's ID
            name=name,
            company_name=company_name,
            phone=phone,
            email=email,
        )

        messages = {"success": "Property has been added."}
        return render(
            request,
            "admin/user/add.html",
            {"messages": messages, "is_superuser": is_superuser},
        )

    messages = {"error": "Property has not been added."}
    return render(
        request,
        "admin/user/add.html",
        {"messages": messages, "is_superuser": is_superuser},
    )


def registeredUser(request):
    user = request.user
    is_superuser = False

    if user.is_authenticated:
        is_superuser = user.is_superuser

    properties_data = CustomUser.objects.all()
    users = CustomUser.objects.filter(is_superuser=0, is_staff=0, is_delete=0)
    index_count = index.objects.all()
    properties = Prperty.objects.all()
    dbcount = database.objects.all().count()
    deleted_users = CustomUser.objects.filter(is_delete=1)
    approved_count = Prperty.objects.filter(is_admin=1).count()


    page = request.GET.get("page", 1)
    properties_per_page = 50

    paginator = Paginator(properties_data, properties_per_page)

    try:
        properties_data_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        # If page is not an integer or out of range, deliver first page
        properties_data_page = paginator.page(1)

    return render(
        request,
        "admin/user/registeruser.html",
        {
            "users": users,
            "properties_data": properties_data_page,
            "deleted_users": deleted_users,
            "is_superuser": is_superuser,
            "index_count": index_count,
            "properties": properties,
            "dbcount": dbcount,
            "approved_count": approved_count,
        },
    )


def edit_user(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    edit = CustomUser.objects.filter(id=id).first()
    properties_data = Prperty.objects.filter(user_id=id).first()
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()

    return render(
        request,
        "admin/user/edit.html",
        {
            "edit": edit,
            "is_superuser": is_superuser,
            "properties_data": properties_data,
            "properties": properties,
            "index_count": index_count,
            "users": users,
            "dbcount": dbcount,
            "approved_count" : approved_count,
        },
    )


def update_user(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    edit = get_object_or_404(CustomUser, id=id)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        is_active = request.POST.get("is_active")

        edit.first_name = first_name
        edit.last_name = last_name
        edit.is_active = is_active
        edit.save()

        context = {"success": "User  information has been Updated !!"}
        return render(
            request,
            "admin/user/edit.html",
            {"edit": edit, "context": context, "is_superuser": is_superuser},
        )

    context = {"error": "Operation failed !!"}

    return render(
        request,
        "admin/user/edit.html",
        {"edit": edit, "context": context, "is_superuser": is_superuser},
    )


def delete_user(request, id):
    delete = CustomUser.objects.filter(id=id).update(is_delete="1")
    return redirect("registeredUser")


def view_property(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    properties_data = Prperty.objects.filter(user_id=id).first()
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()


    # if request.method == "POST":
    #     properties.is_admin = request.POST["is_admin"]
    #     properties.save()

    keys_data = None
    features = None
    if properties_data is not None:
        keys_data = properties_data.features
        features = "".join(
            str(elem).replace("[", "").replace("]", "").replace("'", "")
            for elem in keys_data
        )

    keyvalue = None
    amenties = None
    if properties_data is not None:
        keyvalue = properties_data.amenties
        amenties = "".join(
            str(elem).replace("[", "").replace("]", "").replace("'", "")
            for elem in keyvalue
        )

    keypair = None
    property_type = None
    if properties_data is not None:
        keypair = properties_data.property_type
        property_type = "".join(
            str(elem).replace("[", "").replace("]", "").replace("'", "")
            for elem in keypair
        )

    if properties_data is not None:
        properties_data.features = features
        properties_data.amenties = amenties
        properties_data.property_type = property_type

    users_data = Propertyuser.objects.filter(id=id).first()
    return render(
        request,
        "admin/property/viewproperty.html",
        {
            "properties_data": properties_data,
            "users_data": users_data,
            "is_superuser": is_superuser,
            "properties": properties,
            "index_count": index_count,
            "users": users,
            "dbcount": dbcount,
            "approved_count": approved_count,
        },
    )


def AddUser(request):
    user = request.user
    users = CustomUser.objects.filter(is_superuser=0)
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()

    if user.is_authenticated:
        is_superuser = user.is_superuser
    return render(
        request,
        "admin/user/adduser.html",
        {
            "is_superuser": is_superuser,
            "users": users,
            "properties": properties,
            "index_count": index_count,
            "dbcount": dbcount,
            "approved_count": approved_count
        },
    )


def ajaxadduser(request):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = make_password(request.POST["password1"])
        CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password1,
        )
        context = {"success": "Successfully updated details !!"}
    # print(amenties )

    # return HttpResponse(result )

    return render(
        request,
        "admin/user/adduser.html",
        {"is_superuser": is_superuser, "context": context},
    )
    context = {"error": "Oops! Something went wrong"}
    return render(
        request,
        "admin/user/adduser.html",
        {"is_superuser": is_superuser, "context": context},
    )


## Database


def Database(request):
    if is_ajax(request):
       properties_data = database.objects.all().order_by('-property_id')

       search_value = request.GET.get('search[value]', '')
       draw = request.GET.get('draw')
      
       order_column = int(request.GET.get('order[0][column]'))
       order_dir = request.GET.get('order[0][dir]')


       if order_column==0: 
          if order_dir =='desc':
             properties_data = database.objects.all().order_by('-property_id')

          elif  order_dir =='asc':  
             properties_data = database.objects.all().order_by('property_id') 
          
       
       elif order_column==2:
          if  order_dir =='desc':
              properties_data = database.objects.all().order_by('-date_uploaded')
          
          elif order_dir =='asc':
              properties_data = database.objects.all().order_by('date_uploaded')  

       elif order_column==3:
          if  order_dir =='desc':
              properties_data = database.objects.all().order_by('-date_approved')
          
          elif order_dir =='asc':
              properties_data = database.objects.all().order_by('date_approved')    

       elif order_column==4:
          if  order_dir =='desc':
                properties_data = database.objects.all().order_by('expired_date')
          
          elif order_dir =='asc':
               properties_data = database.objects.all().order_by('-expired_date')

       elif order_column==5:
          if  order_dir =='desc':
              properties_data = database.objects.all().order_by('-duration')
          
          elif order_dir =='asc':
              properties_data = database.objects.all().order_by('duration')  
       
        

       if search_value:
          userinfo= Propertyuser.objects.filter(Q(email__icontains=search_value) |
            Q(phone__icontains=search_value)).values_list('id', flat=True)
           
          user_ids = list(userinfo) 

          property_info= Prperty.objects.filter(user_id__in=user_ids).values_list('id', flat=True)

          property_ids =list(property_info)
          properties_data = database.objects.filter(Q(property_id__in=property_ids) | Q(property_id=search_value)).all()
        
               

          
           
            
   

       start = int(request.GET.get('start', 0))
       length = int(request.GET.get('length', 10))  # Default to 10 records per page
       properties_data = properties_data[start:start + length]

       properties_list=[]
       for property_data in properties_data:
           duration = Prperty.objects.filter(id=property_data.property_id).first()
            

           if property_data.duration=='0':
              property_data.duration ="ongoing"
            

            # Duration Functionality
           if duration and duration.duration == "ongoing":
                property_data.expired_date = "ongoing"

           elif duration:
                int_duration = int(duration.duration)

                input_date_str = property_data.date_uploaded + timedelta(days=int_duration)
                if isinstance(input_date_str, str):
                   
                    input_date = datetime.strptime(input_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                else:
                   
                    input_date = input_date_str 
                property_data.expired_date  = input_date.strftime("%Y-%m-%d, %I:%M %p")
            

            # Uploaded Date
           uploaded_date= property_data.date_uploaded 

           if isinstance(uploaded_date, str):   
                upload_date = datetime.strptime(uploaded_date, "%Y-%m-%dT%H:%M:%S.%fZ")

           else:    
                upload_date = uploaded_date 

           property_data.date_uploaded  = upload_date.strftime("%Y-%m-%d, %I:%M %p")
           
           approved_date = property_data.date_approved

           if isinstance(approved_date, str):   
                approve_date = datetime.strptime(approved_date, "%Y-%m-%dT%H:%M:%S.%fZ")

           else:    
                approve_date = approved_date 

           property_data.date_approved  = approve_date.strftime("%Y-%m-%d, %I:%M %p")



           duration_str =property_data.duration +" "+"days",
               

           properties_list.append({
            'expired_date':property_data.expired_date,
            'duration':duration_str,
            'name':property_data.name,
            'property_id':property_data.property_id,
            'date_uploaded':property_data.date_uploaded,
            'date_approved':property_data.date_approved,
            'number':property_data.number,
            'street':property_data.street,
            'postcode':property_data.postcode,
            'city_town':property_data.city_town,
            'country':property_data.country,
            'continent':property_data.continent,
            'status':property_data.status,
            'status_value':property_data.status_value,
            'prop_type':property_data.prop_type,
            'features':property_data.features,
            'exterior':property_data.exterior,
            'interior':property_data.interior,
            'energy_efficiency':property_data.energy_efficiency,
            'environmental_impact':property_data.environmental_impact,
            'riverside':property_data.riverside,
            'seaside':property_data.seaside,
            'bar':property_data.bar,
            'convenience_store':property_data.convenience_store,
            'fire_station':property_data.fire_station,
            'gym':property_data.gym,
            'hospital':property_data.hospital,
            'nursery':property_data.nursery,
            'park':property_data.park,
            'petrol_station':property_data.petrol_station,
            'police_station':property_data.police_station,
            'restaurant':property_data.restaurant,
            'school':property_data.school,
            'super_market':property_data.super_market,
            'floor_area':property_data.floor_area,
            'site_area':property_data.site_area,
            'kitchen':property_data.kitchen,
            'living_room':property_data.living_room,
            'bedroom1':property_data.bedroom1,
            'bedroom2':property_data.bedroom2,
            'bedroom3':property_data.bedroom3,
            'airport':property_data.airport,
            'bus_stop':property_data.bus_stop,
            'train_station':property_data.train_station,
            'underground_station':property_data.underground_station,
           })   

       
    #    properties_list = list(properties_data.values())
       total_records = database.objects.count()
       return JsonResponse({
            'data': properties_list,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
        })

    
    users = CustomUser.objects.filter(is_superuser=0)
    index_count = index.objects.all()
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()
    properties = Prperty.objects.all()
    user = request.user
    is_superuser = user.is_authenticated and user.is_superuser

    # page = request.GET.get("page", 1)
    # properties_per_page = 50

    # paginator = Paginator(properties_data, properties_per_page)

    # try:
    #     properties_data = paginator.page(page)
    # except PageNotAnInteger:
    #     properties_data = paginator.page(1)
    # except EmptyPage:
    #     properties_data = paginator.page(paginator.num_pages)

    return render(
        request,
        "admin/database/database.html",
        {
            # "properties_data": properties_data,
            'properties':properties,
            "users": users,
            "is_superuser": is_superuser,
            "index_count": index_count,
            "approved_count": approved_count,
            "dbcount": dbcount,
        },
    )
 
def is_ajax(request):
     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'   

# def conversion(cov_floor):
#     try:
#         value_floor, unit_floor = cov_floor.split(" ")
#         value_floor = float(value_floor)
#         unit_floor = unit_floor.strip().lower()

#         if unit_floor == "m²":
#             value_floor = square_meters_to_square_feet(value_floor)
#             unit_floor = "ft²"
#         elif unit_floor == "ft²":
#             value_floor = square_feet_to_square_meters(value_floor)
#             unit_floor = "m²"

#         cov_floor = f"{value_floor:.2f} {unit_floor}"
#     except ValueError:
#         # Handle invalid format or conversion errors gracefully
#         pass

#     return cov_floor


def db_edit(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    edit = database.objects.filter(property_id=id).first()
    properties_data = Prperty.objects.filter(id=id).first()
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()
    
    cov_floor = int(properties_data.floor_area_value)
    floor_area = properties_data.floor_area
    
    cov_site = int(properties_data.site_area_value)
    site_area = properties_data.site_area
    

    if floor_area == "m²":
      sqf = round (cov_floor * 10.7639, 2)
      properties_data.sqf = str(sqf) + " ft²"
    else :
      sqf = round(cov_floor * 0.092903, 2) 
      properties_data.sqf = str(sqf) + " m²"
      
    if site_area == "m²":
      mts = round (cov_site * 10.7639, 2)
      properties_data.mts = str(mts) + " ft²"
    else :
      mts = round(cov_site * 0.092903, 2) 
      properties_data.mts = str(mts) + " m²"
    
    
    return render(
        request,
        "admin/database/db_edit.html",
        {
            "edit": edit,
            "is_superuser": is_superuser,
            "properties_data": properties_data,
            "approved_count" : approved_count,
            "properties": properties,
            "index_count": index_count,
            "users": users,
            "dbcount": dbcount,
            
        },
    )


# def square_meters_to_square_feet(sq_m):
#     # 1 m² = 10.7639 ft²
#     return sq_m * 10.7639


# def square_feet_to_square_meters(sq_ft):
#     # 1 ft² = 0.092903 m²
#     return sq_ft * 0.092903


def db_update(request, id):
    user = request.user
    if user.is_authenticated:
        is_superuser = user.is_superuser
    edit = get_object_or_404(database, id=id)
    databaseID = database.objects.filter(id=id).first()
    percentile = get_object_or_404(PropertyPercentile, property_id=databaseID.property_id)
    properties_data = Prperty.objects.filter(id=id).first()
    properties_city = Prperty.objects.filter(id=databaseID.property_id).first()
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()


    if request.method == "POST":
        name = request.POST.get("name")
        # date_uploaded = request.Post.get("date_uploaded")
        number = request.POST.get("number")
        street = request.POST.get("street")
        postcode = request.POST.get("postcode")
        city_town = request.POST.get("city_town")
        country = request.POST.get("country")
        continent = request.POST.get("continent")
        city = request.POST.get("city")
        # status = request.POST.get("status")
        # status_value = request.POST.get("status_value")
        prop_type = request.POST.get("prop_type")
        features = request.POST.get("features")
        exterior = request.POST.get("exterior")
        interior = request.POST.get("interior")
        energy_efficiency = request.POST.get("energy_efficiency")
        environmental_impact = request.POST.get("environmental_impact")
        riverside = request.POST.get("riverside")
        seaside = request.POST.get("seaside")
        bar = request.POST.get("bar")
        convenience_store = request.POST.get("convenience_store")
        fire_station = request.POST.get("fire_station")
        gym = request.POST.get("gym")
        hospital = request.POST.get("hospital")
        nursery = request.POST.get("nursery")
        park = request.POST.get("park")
        petrol_station = request.POST.get("petrol_station")
        police_station = request.POST.get("police_station")
        restaurant = request.POST.get("restaurant")
        school = request.POST.get("school")
        super_market = request.POST.get("super_market")
        # floor_area = request.POST.get("floor_area")
        # site_area = request.POST.get("site_area")
        kitchen = request.POST.get("kitchen")
        living_room = request.POST.get("living_room")
        bedroom1 = request.POST.get("bedroom1")
        bedroom2 = request.POST.get("bedroom2")
        bedroom3 = request.POST.get("bedroom3")
        bus_stop = request.POST.get("bus_stop")
        airport = request.POST.get("airport")
        train_station = request.POST.get("train_station")
        underground_station = request.POST.get("underground_station")
        sort = request.POST.get("sort")

        edit.name = name
        # edit.date_added = date_uploaded
        edit.number = number
        edit.street = street
        edit.postcode = postcode
        edit.city_town = city_town
        edit.country = country
        edit.continent = continent
        edit.city = city
        # edit.status = status
        # edit.status_value = status_value
        edit.prop_type = prop_type
        edit.features = features
        edit.exterior = exterior
        edit.interior = interior
        edit.energy_efficiency = energy_efficiency
        edit.environmental_impact = environmental_impact
        edit.riverside = riverside
        edit.seaside = seaside
        edit.bar = bar
        edit.convenience_store = convenience_store
        edit.fire_station = fire_station
        edit.gym = gym
        edit.hospital = hospital
        edit.nursery = nursery
        edit.park = park
        edit.petrol_station = petrol_station
        edit.police_station = police_station
        edit.restaurant = restaurant
        edit.school = school
        edit.super_market = super_market
        # edit.floor_area = floor_area
        # edit.site_area = site_area
        edit.kitchen = kitchen
        edit.living_room = living_room
        edit.bedroom1 = bedroom1
        edit.bedroom2 = bedroom2
        edit.bedroom3 = bedroom3
        edit.bus_stop = bus_stop
        edit.airport = airport
        edit.train_station = train_station
        edit.underground_station = underground_station
        edit.sort = sort

        edit.save()

        percentile.city=city
        percentile.save()

        properties_city.city=city
        properties_city.save()
        
        messages.success(request, 'Property  information has been Updated.')
        return render(
            request,
            "admin/database/db_edit.html",
            {
                "edit": edit,
                "is_superuser": is_superuser,
                "properties_data": properties_data,
                "properties": properties,
                "index_count": index_count,
                "users": users,
                "dbcount": dbcount,
                "approved_count": approved_count,
            },
        )

    context = {"error": "Operation failed !!"}

    return render(
        request,
        "admin/database/db_edit.html",
        {
            "edit": edit,
            "context": context,
            "is_superuser": is_superuser,
            "properties_data": properties_data,
            "properties": properties,
            "index_count": index_count,
            "users": users,
            "dbcount": dbcount,
            "approved_count":approved_count,
        },
    )


##Ratings
def rating(request):
    user = request.user
    users = CustomUser.objects.filter(is_superuser=0)
    super_admin = CustomUser.objects.filter(is_superuser=1).first()
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    dbcount = database.objects.all().count()
    properties_data = Rating.objects.all()
    is_admin_rating = Rating.objects.filter(admin_id=user.id).first()
    # ratings = Rating.objects.filter(admin_id=user.id).all()
    ratings = database.objects.all()
    
    for rating in ratings:
        is_exist = database.objects.filter(property_id=rating.property_id).first()
        
        if is_exist is not None:
            rating.is_exist = 'active'
        else:
            rating.is_exist = 'not_active'

       
    
    # print(user.is_superuser)
    # return HttpResponse(user.is_superuser)
    
    approved_count = Prperty.objects.filter(is_admin=1).count()

    
    # for rating in ratings:
    #     if is_admin_rating:
    #         rating.interior_rating = is_admin_rating.interior
    #         rating.exterior_rating = is_admin_rating.exterior
    # else:
    #     # If the user doesn't have a rating, you might want to set default values or handle it accordingly.
    #     rating.interior_rating = 0
    #     rating.exterior_rating = 0

    # if user.is_authenticated:
    #     is_superuser = user.is_superuser

    is_superuser = user.is_authenticated and user.is_superuser

    page = request.GET.get("page", 1)
    properties_per_page = 50

    paginator = Paginator(properties_data, properties_per_page)

    try:
        properties_data = paginator.page(page)
    except PageNotAnInteger:
        properties_data = paginator.page(1)
    except EmptyPage:
        properties_data = paginator.page(paginator.num_pages)

    return render(
        request,
        "admin/rating/rating.html",
        {
            "user": user,
            "super_admin": super_admin,
            "is_superuser": is_superuser,
            "users": users,
            "properties": properties,
            "ratings": ratings,
            "index_count": index_count,
            "dbcount": dbcount,
            "properties_data": properties_data,
            "approved_count": approved_count
        },
    )


def rating_edit(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    
    properties_data = Prperty.objects.filter(id=id).first()
    properties = Prperty.objects.all()
    index_count = index.objects.all()
    users = CustomUser.objects.filter(is_superuser=0)
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()
    edit = database.objects.filter(property_id=id).first()
    
    

    # print(edit)
    # return HttpResponse(ratings)
    return render(
        request,
        "admin/rating/rating_edit.html",
        {
            "edit": edit,
            "is_superuser": is_superuser,
            "properties_data": properties_data,
            "properties": properties,
            "index_count": index_count,
            "users": users,
            "dbcount": dbcount,
            "approved_count" : approved_count,
            "property_id":id
        },
    )

 
def add_rating(request):
    user = request.user
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        interior = request.POST.get('interior')
        exterior = request.POST.get('exterior')

        property= Prperty.objects.filter(id=property_id).first()
           
        rating = database.objects.get(property_id=property_id)
     
        
        rating.interior = interior
        rating.exterior = exterior
        
        rating.save()

        messages.success(request, 'Rating updated successfully.')
        

    
    previous_page_url = request.META.get('HTTP_REFERER')
    return redirect(previous_page_url)

    

def new_rating(request):
    user = request.user
    users = CustomUser.objects.filter(is_superuser=1).first()
    is_not = Rating.objects.filter(admin_id=user.id).values_list('property_id', flat=True)
  
    rating = Rating.objects.filter(admin_id=users.id).exclude(property_id__in=is_not)

    for sin in rating:
        propertyName=Prperty.objects.filter(id=sin.property_id).first()

        sin.property_name = propertyName.title


    return render(
        request,
        "admin/rating/new_rating.html",
        {
            "rating" :rating
        },
    )
def property_view(request):
    property_id = request.GET.get('property_id')
    property= Prperty.objects.filter(id=property_id).first()
    
    page_url = property.weburl
    return redirect(page_url)

def add_new_rating(request):
    user = request.user

    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        interior = request.POST.get('interior')
        exterior = request.POST.get('exterior')

        property= Prperty.objects.filter(id=property_id).first()
        
        rating = Rating.objects.create(
            property_id=property_id,
            admin_id=user.id,
            interior=interior,
            exterior=exterior,
            name = property.title,
            link = property.weburl,
            date_added = timezone.now()
        )

        messages.success(request, 'Rating added successfully.')
    
    
    previous_page_url = request.META.get('HTTP_REFERER')
    return redirect('/admin/rating')

def view_all_rating(request, id):
    user = request.user
    rating = Rating.objects.filter(property_id=id).all()
    for sin in rating:
       admin_name=CustomUser.objects.filter(id=sin.admin_id).first()
       sin.admin_name=admin_name.first_name


    # print(id)
    # return HttpResponse(id)
    page = request.GET.get("page", 1)
    properties_per_page = 10

    paginator = Paginator(rating, properties_per_page)

    try:
        properties_data = paginator.page(page)
    except PageNotAnInteger:
        properties_data = paginator.page(1)
    except EmptyPage:
        properties_data = paginator.page(paginator.num_pages)
    return render(
        request,
        "admin/rating/view_rating.html",
        {
            "rating" :rating
        },
    )
   

def approve(request, id):
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    prperty = get_object_or_404(Prperty, id=id)
    prperty.is_admin = 1
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%H:%M, %d/%m/%Y")
    parsed_datetime = datetime.strptime(formatted_datetime, "%H:%M, %d/%m/%Y")
    user_id = prperty.user_id
    # floor_area_combined = f"{prperty.floor_area_value} {prperty.floor_area}"
    # site_area_combined = f"{prperty.site_area_value} {prperty.site_area} "
    floor_area_combined = int(prperty.floor_area_value)
    site_area_combined = int(prperty.site_area_value)
    prperty.save()

    features = "".join(
        str(elem).replace("[", "").replace("]", "").replace("'", "")
        for elem in prperty.features
    )

    prop_type = "".join(
        str(elem).replace("[", "").replace("]", "").replace("'", "")
        for elem in prperty.property_type
    )
    duration=prperty.duration
    if duration=="ongoing":
       duration=0
    else:
       duration=prperty.duration

    int_duration = int(duration)

    input_date_str = prperty.created_at + timedelta(days=int_duration)

    Addproperty = database.objects.create(
        name=prperty.title,
        date_uploaded=prperty.created_at,
        date_approved=parsed_datetime,
        city_town=prperty.address,
        country=prperty.Country,
        continent=prperty.Continent,
        status=prperty.purchase_type,
        status_value=prperty.amount,
        prop_type=prop_type,  # Use the modified prop_type variable
        features=features,  # Use the modified features variable
        floor_area=floor_area_combined,
        site_area=site_area_combined,
        link=prperty.weburl,
        city=prperty.city,
        duration=duration,
        expired_date=input_date_str,
        property_id=id,
        interior = 0,
        exterior = 0,
       
        energy_efficiency = 0,
        environmental_impact = 0,
        riverside = 0,
        seaside = 0,
        bar = 0,
        convenience_store = 0,
        fire_station = 0,
        gym = 0,
        hospital = 0,
        park = 0,
        petrol_station = 0,
        police_station = 0,
        restaurant = 0,
        super_market = 0,
        kitchen = 0,
        living_room = 0,
        bedroom1 = 0,
        bedroom2 = 0,
        bedroom3 = 0,
        airport = 0,
        bus_stop = 0,
        train_station = 0,
        underground_station = 0,
        nursery = 0,
        school = 0
    )

    admin_id = user.id
    property_id = id

    Rating.objects.create(
        admin_id=admin_id,
        name=prperty.title,
        date_added=prperty.created_at,
        link=prperty.weburl,
        property_id=id,
        interior = 0,
        exterior = 0,
    )
    
    
  
    percent = PropertyPercentile.objects.create(
        property_id=id,
        date_uploaded=prperty.created_at,
        date_approved=parsed_datetime,
        index=prperty.index,
        category=prperty.category,
        weburl=prperty.weburl,
        address=prperty.address,
        purchase_type=prperty.purchase_type,
        property_type=prperty.property_type,
        Bedroom=prperty.Bedroom,
        bathroom=prperty.bathroom,
        features=prperty.features,
        amenties=prperty.amenties,
        duration=prperty.duration,
        is_admin=1,
        title=prperty.title,
        user_id=prperty.user_id,
        amount=prperty.amount,
        Country=prperty.Country,
        Continent=prperty.Continent,
        hide=prperty.hide,
        city=prperty.city,
        )
        
    return redirect("view_property", user_id)
def update_special(request):
    # prperties = Prperty.objects.all()
    
    # for prty in prperties:
    #     PropertyPercentile.objects.filter(property_id=prty.id).update(
    #         property_type=prty.property_type,
    #         purchase_type=prty.purchase_type
    #     )

    return HttpResponse("Update complete.")

def unapprove(request, id):
    prperty = get_object_or_404(Prperty, id=id)
    prperty.is_admin = 0
    user_id = prperty.user_id
    prperty.save()

    # Delete the corresponding entry from the 'database' table
    database.objects.filter(property_id=id).delete()
    Rating.objects.filter(property_id=id).delete()
    PropertyPercentile.objects.filter(property_id=id).delete()

    return redirect("view_property", user_id)

def delete_property(request, id):
    user_id= Prperty.objects.filter(id=id).first()
    Propertyuser.objects.filter(id=user_id.user_id).delete()
    Prperty.objects.filter(id=id).delete()
    database.objects.filter(property_id=id).delete()
    Rating.objects.filter(property_id=id).delete()
    PropertyPercentile.objects.filter(property_id=id).delete()

    messages.success(request, 'Property Has been  successfully removed.')
    return redirect("database")


def Index(request):
    # Count
    user = request.user

    if user.is_authenticated:
        is_superuser = user.is_superuser

    all_properties = Prperty.objects.all()

    # print(properties.count())
    # return HttpResponse(properties.count())

    index_count = index.objects.all()
    dbcount = database.objects.all().count()
    approved_count = Prperty.objects.filter(is_admin=1).count()

    super_admin = CustomUser.objects.filter(is_superuser=1).first()
    # Database Index according to serial
    dbproperties = database.objects.values('name', 'property_id',
     'date_uploaded', 'date_approved', 'number', 'street',
     'postcode', 'city_town', 'country', 'continent','status', 'status_value', 'prop_type', 'features').order_by('-property_id')
    
    
    #Get  Perfect Calculation 
   
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


    bedroom1 =  database.objects.annotate(
    bedroom1_percentile=Window(
        expression=PercentRank(),
        order_by=F('bedroom1').asc()
    )).filter(bedroom1__gt=0).values('property_id', 'bedroom1_percentile')

    for bed1 in bedroom1:
        bedorounded = round(bed1['bedroom1_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=bed1['property_id']).update(bedroom1=bedorounded)


    bedroom2 =  database.objects.annotate(
    bedroom2_percentile=Window(
        expression=PercentRank(),
        order_by=F('bedroom2').asc()
    )).filter(bedroom2__gt=0).values('property_id', 'bedroom2_percentile')

    for bed2 in bedroom2:
        bedtrounded = round(bed2['bedroom2_percentile'] * 100, 2)
        PropertyPercentile.objects.filter(property_id=bed2['property_id']).update(bedroom2=bedtrounded)

    bedroom3 =  database.objects.annotate(
    bedroom3_percentile=Window(
        expression=PercentRank(),
        order_by=F('bedroom3').asc()
    )).filter(bedroom3__gt=0).values('property_id', 'bedroom3_percentile')

    for bed3 in bedroom3:
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
    

    






    modified_properties = []
        # print(name)
        # return HttpResponse(name)
    for record in dbproperties:

        # Amenities
        property_id = record['property_id']
        prty=  properties = Prperty.objects.filter(id=property_id).first()

        amenities = prty.amenties
        amenities_array = [part.strip() for part in amenities.split(',')] 
        
        Parking_facilities ="No"
        Playground ="No"
        Swimming_pool ="No"
        Laundry_facilities ="No"
        Outdoor_spaces ="No"
        Gym ="No"
        Air_conditioning ="No"
        Security_cameras ="No"
        Private_patio ="No"
        Outdoor_furniture= "No"
        Outdoor_dining_area= "No"
        Smoke_alarm= "No"
        Carbon_monoxide_alarm= "No"
        Fire_extinguisher= "No"
        First_aid_kit= "No"
        Mountain_view= "No"
        Valley_view= "No"
        Heating= "No"


        for a in range(len(amenities_array)):
             if "Parking facilities" in amenities_array[a]:
                 Parking_facilities ="Yes"

             if "Playground" in amenities_array[a]:
                 Playground ="Yes" 

             if "Swimming pool" in amenities_array[a]:
                 Swimming_pool ="Yes"

             if "Laundry facilities" in amenities_array[a]:
                 Laundry_facilities ="Yes" 

             if "Outdoor spaces" in amenities_array[a]:
                 Outdoor_spaces ="Yes"

             if "Gym" in amenities_array[a]:
                 Gym ="Yes"

             if "Air conditioning" in amenities_array[a]:
                 Air_conditioning ="Yes"

             if "Security cameras" in amenities_array[a]:
                 Security_cameras ="Yes"  

             if "Private patio" in amenities_array[a]:
                 Private_patio ="Yes" 

             if "Outdoor furniture" in amenities_array[a]:
                 Outdoor_furniture ="Yes"  

             if "Outdoor dining area" in amenities_array[a]:
                 Outdoor_dining_area ="Yes" 

             if "Smoke alarm" in amenities_array[a]:
                 Smoke_alarm ="Yes" 

             if "Carbon monoxide alarm" in amenities_array[a]:
                 Carbon_monoxide_alarm ="Yes" 

             if "Fire extinguisher" in amenities_array[a]:
                 Fire_extinguisher ="Yes" 

             if "First aid kit" in amenities_array[a]:
                 First_aid_kit ="Yes"   

             if "Mountain view" in amenities_array[a]:
                 Mountain_view ="Yes" 

             if "Valley view" in amenities_array[a]:
                 Valley_view ="Yes"

             if "Heating" in amenities_array[a]:
                 Heating ="Yes" 
                      


        #Features 
        features=record['features']

        my_array = [part.strip() for part in features.split(',')] 
        Living_Room = "No"
        Studio = "No"
        Garage = "No"
        Garden = "No"
        Balcony = "No"
        En_suite = "No"
        Kitchen = "No"
        for i in range(len(my_array)):
            if "Living Room" in my_array[i]:
                Living_Room ="Yes"
               
           

            if "Studio" in  my_array[i]:
                Studio ="Yes"
               
            

            if "Garage" in  my_array[i]:
                Garage ="Yes"
                
         

            if "Garden" in  my_array[i]:
                Garden ="Yes"
                
       

            if "Balcony" in  my_array[i]:
                Balcony ="Yes"
                
           

            if "En-suite" in my_array[i]:
                En_suite ="Yes"
                
        

            if "Kitchen" in  my_array[i]:
                Kitchen ="Yes"
                
         

        # # Round OFF
        property_id = record['property_id']
        riverside =  PropertyPercentile.objects.filter(property_id=property_id).values_list('riverside', flat=True).first()
        riverside_rounded = riverside
        seapercentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('seaside', flat=True).first()

        energy_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('energy_efficiency', flat=True).first()
        env_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('environmental_impact', flat=True).first()

        exterior_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('exterior', flat=True).first()
        interior_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('interior', flat=True).first()

        bar_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('bar', flat=True).first()
        converience_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('convenience_store', flat=True).first()
        fire_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('fire_station', flat=True).first()
        gym_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('gym', flat=True).first()
        hospital_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('hospital', flat=True).first()
        nursery_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('nursery', flat=True).first()
        park_percentile=  PropertyPercentile.objects.filter(property_id=property_id).values_list('park', flat=True).first()
        petrol_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('petrol_station', flat=True).first()
        police_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('police_station', flat=True).first()
        restaurant_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('restaurant', flat=True).first()

        school_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('school', flat=True).first()
        market_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('super_market', flat=True).first()
        floor_percentile=PropertyPercentile.objects.filter(property_id=property_id).values_list('floor_area', flat=True).first()
        site_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('site_area', flat=True).first()
        kitchen_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('kitchen', flat=True).first()
        living_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('living_room', flat=True).first()
        bedroom1_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('bedroom1', flat=True).first()
        bedroom2_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('bedroom2', flat=True).first()
        bedroom3_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('bedroom3', flat=True).first()
        airport_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('airport', flat=True).first()
        bus_stop_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('bus_stop', flat=True).first()
        train_station_percentile= PropertyPercentile.objects.filter(property_id=property_id).values_list('train_station', flat=True).first()
        underground_station_percentile = PropertyPercentile.objects.filter(property_id=property_id).values_list('underground_station', flat=True).first()

        # print(floor_percentile)
        # return HttpResponse(floor_percentile)


        # Count 1 to 3
        if underground_station_percentile is None:
            under_count = ''
        else:
           
            underground_station_percentile = float(underground_station_percentile)
            
            if underground_station_percentile >= 75:
                under_count = 3
            elif underground_station_percentile >= 25:
                under_count = 2
            elif underground_station_percentile >= 0:
                under_count = 1
            else:
                under_count = ''

        if train_station_percentile is None:
            train_count=''
        else:
            train_station_percentile = float(train_station_percentile)
            if train_station_percentile >= 75:
                train_count = 3
            elif train_station_percentile >= 25:
                train_count = 2
            elif train_station_percentile >= 0:
                train_count = 1    
            else:
                train_count = ''


        if bus_stop_percentile is None:
            bus_count= ''

        else:
            bus_stop_percentile = float(bus_stop_percentile)
            if bus_stop_percentile >= 75:
                bus_count = 3
            elif bus_stop_percentile >= 25:
                bus_count = 2
            elif bus_stop_percentile >= 0:
                bus_count = 1     
            else:
                bus_count = ''


        if airport_percentile is None:
            airport_count=''
        else:
            airport_percentile = float(airport_percentile)
            if airport_percentile >= 75:
                airport_count = 3
            elif airport_percentile >= 25:
                airport_count = 2
            elif airport_percentile >= 0:
                airport_count = 1    
            else:
                airport_count = ''

        if bedroom3_percentile is None:
            bedroom3_count =''
        else:
            bedroom3_percentile = float(bedroom3_percentile)
            if bedroom3_percentile >= 75:
                bedroom3_count = 3
            elif bedroom3_percentile >= 25:
                bedroom3_count = 2
            elif bedroom3_percentile >= 0:
                bedroom3_count = 1    
            else:
                bedroom3_count = ''

        if bedroom2_percentile is None:
            bedroom2_count =''
        else:   
            bedroom2_percentile = float(bedroom2_percentile)
            if bedroom2_percentile >= 75:
                bedroom2_count = 3
            elif bedroom2_percentile >= 25:
                bedroom2_count = 2
            elif bedroom2_percentile >= 0:
                bedroom2_count = 1     
            else:
                bedroom2_count = ''

        
        if bedroom1_percentile is None:
            bedroom1_count =''
        else:    
            bedroom1_percentile = float(bedroom1_percentile)
            if bedroom1_percentile >= 75:
                bedroom1_count = 3
            elif bedroom1_percentile >= 25:
                bedroom1_count = 2
            elif bedroom1_percentile >= 0:
                bedroom1_count = 1    
            else:
                bedroom1_count = ''

        if living_percentile is None:
            living_count =''
        else:
            living_percentile = float(living_percentile)    
            if living_percentile >= 75:
               living_count = 3
            elif living_percentile >= 25:
                living_count = 2
            elif living_percentile >= 0:
                living_count = 1    
            else:
                living_count = ''

        if kitchen_percentile is None:
            kitchen_count =''
        else:
            kitchen_percentile= float(kitchen_percentile)
            if kitchen_percentile >= 75:
               kitchen_count = 3
            elif kitchen_percentile >= 25:
                kitchen_count = 2
            elif kitchen_percentile >= 0:
                kitchen_count = 1    
            else:
                kitchen_count = ''

        if site_percentile is None:
            site_count =''
        else:
            site_percentile = float(site_percentile)
            if site_percentile >= 75:
               site_count = 3
            elif site_percentile >= 25:
                site_count = 2
            elif site_percentile >= 0:
                site_count = 1    
            else:
                site_count = ''


        if floor_percentile is None:
            floor_count =''
        else: 
             
            floor_percentile = float(floor_percentile) 
       
           

            if floor_percentile >= 75:
                floor_count = 3
            elif floor_percentile >= 25:
                floor_count = 2
            elif floor_percentile >= 0:
                floor_count = 1     
            else:
                floor_count = ''

        if hospital_percentile is None:
            hospital_count =''
        else:   
            hospital_percentile = float(hospital_percentile)
            if hospital_percentile >= 75:
                 hospital_count = 3
            elif hospital_percentile >= 25:
                hospital_count = 2
            elif hospital_percentile >= 0:
                hospital_count = 1   
            else:
                hospital_count = ''

        if market_percentile is None:
            market_count =''
        else:
            market_percentile =float(market_percentile)    
            if market_percentile >= 75:
                 market_count = 3
            elif market_percentile >= 25:
                market_count = 2
            elif market_percentile >= 0:
                market_count = 1    
            else:
                market_count = ''

        if school_percentile is None:
            school_count =''
        else:
            school_percentile =float(school_percentile)
            if school_percentile >= 75:
                school_count = 3
            elif school_percentile >= 25:
                school_count = 2
            elif school_percentile >= 0:
                school_count = 1   
            else:
                school_count = ''

        if restaurant_percentile is None:
            resturant_count =''
        else:
            restaurant_percentile =float(restaurant_percentile)
            if restaurant_percentile >= 75:
                resturant_count = 3
            elif restaurant_percentile >= 25:
                resturant_count = 2
            elif restaurant_percentile >= 0:
                resturant_count = 1    
            else:
                resturant_count = ''


        if police_percentile is None:
            police_count =''
        else:
            police_percentile =float(police_percentile)
            if police_percentile >= 75:
                 police_count = 3
            elif police_percentile >= 25:
                police_count = 2
            elif police_percentile >= 0:
                police_count = 1  
            else:
                police_count = ''

        if petrol_percentile is None:
            petrol_count =''
        else:
            petrol_percentile =float(petrol_percentile)
            if petrol_percentile >= 75:
                 petrol_count = 3
            elif petrol_percentile >= 25:
                petrol_count = 2
            elif petrol_percentile >= 0:
                petrol_count = 1    
            else:
                petrol_count = ''


        if park_percentile is None:
            park_count =''  
        else:
            park_percentile =float(park_percentile)
            if park_percentile >= 75:
                 park_count = 3
            elif park_percentile >= 25:
                park_count = 2
            elif park_percentile >= 0:
                park_count = 1   
            else:
                park_count = ''


        if nursery_percentile is None:
            nursery_count ='' 
        else:
            nursery_percentile =float(nursery_percentile)
            if nursery_percentile >= 75:
                 nursery_count = 3
            elif nursery_percentile >= 25:
                nursery_count = 2
            elif nursery_percentile >= 0:
                nursery_count = 1    
            else:
                nursery_count = ''


        if hospital_percentile is None:
            hosipital_count =''
        else:   
            hospital_percentile =float(hospital_percentile)
            if hospital_percentile >= 75:
                hosipital_count = 3
            elif hospital_percentile >= 25:
                hosipital_count = 2
            elif hospital_percentile >= 0:
                hosipital_count = 1    
            else:
                hosipital_count = ''


        if gym_percentile is None:
            gym_count =''
        else:
            gym_percentile =float(gym_percentile)
            if gym_percentile >= 75:
                gym_count = 3
            elif gym_percentile >= 25:
                gym_count = 2
            elif gym_percentile >= 0:
                gym_count = 1    
            else:
                gym_count = ''

        if fire_percentile is None:
            fire_count =''
        else:
            fire_percentile =float(fire_percentile)
            if fire_percentile >= 75:
                fire_count = 3
            elif fire_percentile >= 25:
                fire_count = 2
            elif fire_percentile >= 0:
                fire_count = 1    
            else:
                fire_count = ''


        if converience_percentile is None:
            conver_count =''
        else:
            converience_percentile =float(converience_percentile)
            if converience_percentile >= 75:
                conver_count = 3
            elif converience_percentile >= 25:
                conver_count = 2
            elif converience_percentile >= 0:
                conver_count = 1    
            else:
                conver_count = '' 


        if bar_percentile is None:
            bar_count =''
        else:
            bar_percentile =float(bar_percentile)
            if bar_percentile >= 75:
                bar_count = 3
            elif bar_percentile >= 25:
                bar_count = 2
            elif bar_percentile >= 0:
                bar_count = 1    
            else:
                bar_count = '' 


        if interior_percentile is None:
            int_count =''
        else:
            interior_percentile =float(interior_percentile)
            if interior_percentile >= 75:
                int_count = 3
            elif interior_percentile >= 25:
                int_count = 2
            elif interior_percentile >= 0:
                int_count = 1
            else:
                int_count = '' 


        if exterior_percentile is None:
            ext_count =''
        else:
            exterior_percentile =float(exterior_percentile)
            if exterior_percentile >= 75:
                ext_count = 3
            elif exterior_percentile >= 25:
                ext_count = 2
            elif exterior_percentile >= 0:
                ext_count = 1    
            else:
                ext_count = ''




        if energy_percentile is None:
            energy_count =''
        else:
            energy_percentile =float(energy_percentile)
            if energy_percentile >= 75:
                energy_count = 3
            elif energy_percentile >= 25:
                energy_count = 2
            elif energy_percentile >= 0:
                energy_count = 1    
            else:
                energy_count = '' 


        if env_percentile is None:
            env_count =''
        else:
            env_percentile =float(env_percentile)
            if env_percentile >= 75:
                env_count = 3
            elif env_percentile >= 25:
                env_count = 2
            elif env_percentile >= 0:
                env_count = 1    
            else:
                env_count = ''    

        if riverside is None:
            riverside_value =''
        else:
            riverside =float(riverside)
            if riverside >= 75:
                riverside_value = 3
            elif riverside >= 25:
                riverside_value = 2
            elif riverside >= 0:
                riverside_value = 1    
            else:
                riverside_value = ''


        if seapercentile is None:
            sea_count =''
        else:
            seapercentile =float(seapercentile)
            if seapercentile >= 75:
                sea_count = 3
            elif seapercentile >= 25:
                sea_count = 2
            elif seapercentile >= 0:
                sea_count = 1
            else:
                sea_count = ''    




        modified_properties.append({
            'name': record['name'],
            'property_id': record['property_id'],
            'date_uploaded': record['date_uploaded'],
            'date_approved': record['date_approved'],
            'street': record['street'],
            'number': record['number'],
            'postcode': record['postcode'],
            'city_town': record['city_town'],
            'continent': record['continent'],
            'country': record['country'],
            'riverside_count': riverside_value,
            'river_percentile': riverside_rounded,
            'seapercentile': seapercentile,
            'sea_count': sea_count,
            'status_value': record['status_value'],
            'status':  record['status'],
            'features':  record['features'],
            'prop_type':  record['prop_type'],
            'property_id':record['property_id'],
            'exterior_percentile':  exterior_percentile,
            'ext_count':  ext_count,
            'interior_percentile':  interior_percentile,
            'int_count':  int_count,
            'energy_percentile':  energy_percentile,
            'energy_count':  energy_count,
            'env_percentile':  env_percentile,
            'env_count':  env_count,
            'gym_count':  gym_count,
            'bar_percentile':  bar_percentile,
            'bar_count':  bar_count,
            'converience_percentile':  converience_percentile,
            'conver_count':  conver_count,
            'fire_percentile':  fire_percentile,
            'fire_count':  fire_count,
            'gym_percentile':  gym_percentile,
            'hospital_percentile':  hospital_percentile,
            'hospital_count':  hospital_count,
            'nursery_percentile':  nursery_percentile,
            'nursery_count':  nursery_count,
            'park_percentile':  park_percentile,
            'park_count':  park_count,
            'petrol_percentile':  petrol_percentile,
            'petrol_count':  petrol_count,
            'police_percentile':  police_percentile,
            'police_count':  police_count,
            'restaurant_percentile':  restaurant_percentile,
            'resturant_count':  resturant_count,
            'school_percentile': school_percentile,
            'school_count':  school_count,
            'market_percentile':  market_percentile,
            'market_count':  market_count,
            'floor_percentile':  floor_percentile,
            'floor_count':  floor_count,
            'site_percentile':  site_percentile,
            'site_count':  site_count,
            'kitchen_percentile':  kitchen_percentile,
            'kitchen_count':  kitchen_count,
            'living_percentile':  living_percentile,
            'living_count':  living_count,
            'bedroom1_percentile':  bedroom1_percentile,
            'bedroom1_count':  bedroom1_count,
            'bedroom2_percentile':  bedroom2_percentile,
            'bedroom2_count':  bedroom2_count,
            'bedroom3_count':  bedroom3_count,
            'bedroom3_percentile':  bedroom3_percentile,
            'underground_station_percentile': underground_station_percentile,
            'under_count': under_count,
            'train_station_percentile': train_station_percentile,
            'train_count': train_count,
            'airport_percentile': airport_percentile,
            'airport_count': airport_count,
            'bus_stop_percentile': bus_stop_percentile,
            'bus_count': bus_count,
            'Living_Room': Living_Room,
            'Studio': Studio,
            'Kitchen': Kitchen,
            'Garage': Garage,
            'Garden': Garden,
            'Balcony': Balcony,
            'En_suite': En_suite,
            'amenities': amenities,
            'Parking_facilities': Parking_facilities,
            'Playground': Playground,
            'Swimming_pool': Swimming_pool,
            'Laundry_facilities': Laundry_facilities,
            'Gym': Gym,
            'Air_conditioning': Air_conditioning,
            'Security_cameras': Security_cameras,
            'Private_patio': Private_patio,
            'Outdoor_furniture': Outdoor_furniture,
            'Outdoor_dining_area': Outdoor_dining_area,
            'Smoke_alarm': Smoke_alarm,
            'Carbon_monoxide_alarm': Carbon_monoxide_alarm,
            'Fire_extinguisher': Fire_extinguisher,
            'First_aid_kit': First_aid_kit,
            'Mountain_view': Mountain_view,
            'Valley_view': Valley_view,
            'Heating': Heating,
           
        })

    page = request.GET.get("page", 1)
    properties_per_page = 100

    paginator = Paginator(modified_properties, properties_per_page)

    try:
        modified_properties = paginator.page(page)
    except PageNotAnInteger:
        modified_properties = paginator.page(1)
    except EmptyPage:
        modified_properties = paginator.page(paginator.num_pages)


    return render(request, "admin/count/index.html", {'properties': all_properties, 'index_count':index_count, 'dbcount':dbcount, 'approved_count':approved_count, 'dbproperties':modified_properties, 'is_superuser':is_superuser, 'users':user}
     )  
def Percentile(request):
    allPrperties =  database.objects.values('name', 'property_id', 'seaside')
    approved_count = Prperty.objects.filter(is_admin=1).count()
    properties =Prperty.objects.all()
    for sin in properties:
        if sin.duration=="ongoing":
         duration= 0
        else:
         duration=   sin.duration
        int_duration = int(duration)

        input_date_str = sin.created_at + timedelta(days=int_duration)
        property_id=sin.id
        
        database.objects.filter(property_id=property_id).update(expired_date=input_date_str)

    dbproperties = database.objects.annotate(
     seapercentile=Window(
        expression=PercentRank(),
        order_by=F('seaside').asc()
    )
    ).filter(seaside__gt=0).values('name',  'seaside', 'seapercentile', 'id', 'property_id')
  
  
    print(properties)
    return HttpResponse(properties)
    modified_properties = []
    for record in dbproperties:
        

        seapercentile= round(record['seapercentile'] * 100, 2)
        # Modify 'riverside' based on conditions

        modified_properties.append({
            'name': record['name'],
            'seaside': record['seaside'],
            'seapercentile': seapercentile, 
            'property_id': record['property_id'], 
        })

    

    return render(request, "percentile.html", {'allPrperties': allPrperties ,'dbproperties': modified_properties, 'approved_count':approved_count, 'properties': properties})
