import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render
import re
from .library import isEmpty
from email_validator import validate_email, EmailNotValidError
from .models import User
from .constants import EMAIL_ALREADY_EXIST, SUCCESS, YOU_ARE_NOT_REGISTERED, PASSWORD_INVALID
from passlib.hash import sha256_crypt

# Create your views here.
def home(request):
    if 'userlogin' in request.session and request.session['userlogin'] == True:
        if data:= User.objects.get(email=request.session['userEmail']):
            return render(request, 'index.html', {'data': data})        
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def login_validation(request):
    if request.method != 'POST':
        return
    login_email = request.POST.get("login_email")
    login_password = request.POST.get("login_password")

    if isEmpty(login_email):
        return JsonResponse({'message': 'Please enter Email ID', 'status': 0})

    if isEmpty(login_password):
        return JsonResponse({'message': 'Please enter your password', 'status': 0})

    try:
        validated_email = validate_email(login_email).email # email is validated
        print('email is validated')
        if data := User.objects.filter(email=validated_email):
            for row in data:
                fullname = f'{row.first_name} {row.last_name}'
                userpassword = row.password
                user_email = row.email

            if (sha256_crypt.verify(login_password, userpassword)):
                new_data = verifyUser(fullname, request, user_email)
            else:
                new_data = {'data': {}, 'message': PASSWORD_INVALID, 'status': 0}
        else:
            new_data = {'data': {}, 'message': YOU_ARE_NOT_REGISTERED, 'status': 0}
        return JsonResponse(new_data)

    except EmailNotValidError as e:
        print(e)
        return JsonResponse({'message': 'Email is invalid', 'status': 0})



# TODO Rename this here and in `login_validation`
def verifyUser(fullname, request, user_email):
    request.session['username'] = fullname
    request.session['userlogin'] = True
    request.session['userEmail'] = user_email
    return {
        'data': {'message': 'Logged in successfully'},
        'message': SUCCESS,
        'status': 1,
    }

def logout(request):
    del request.session['username']
    del request.session['userlogin']
    return redirect("home")

def signup(request):
    return render(request, 'sign-up.html')

def signup_validation(request):
    if request.method != 'POST':
        return
    first_name = request.POST.get("signup_first_name")
    last_name = request.POST.get("signup_last_name")
    date_of_birth = request.POST.get("date_of_birth")
    month_of_birth = request.POST.get("month_of_birth")
    year_of_birth = request.POST.get("year_of_birth")
    email = request.POST.get("signup_email")
    phone_number = request.POST.get("signup_phone")
    signup_password = request.POST.get("signup_password")

    if isEmpty(first_name):
        new_data={'data': {}, 'message': 'Please enter first name', 'status': 0}
        return JsonResponse(new_data)
    
    if isEmpty(last_name):
        new_data={'data': {}, 'message': 'Please enter last name', 'status': 0}
        return JsonResponse(new_data)
    
    if isEmpty(date_of_birth):
        new_data={'data': {}, 'message': 'Please enter your date of birth', 'status': 0}
        return JsonResponse(new_data)

    if isEmpty(month_of_birth):
        new_data={'data': {}, 'message': 'Please confirm your month of birth', 'status': 0}
        return JsonResponse(new_data)
    
    if isEmpty(year_of_birth):
        new_data={'data': {}, 'message': 'Please confirm your year of birth', 'status': 0}
        return JsonResponse(new_data)

    if isEmpty(phone_number):
        new_data={'data': {}, 'message': 'Please enter your phone number', 'status': 0}
        return JsonResponse(new_data)

    if isEmpty(email):
        new_data={'data': {}, 'message': 'Please enter email address', 'status': 0}
        return JsonResponse(new_data)
    
    x = datetime.datetime(int(year_of_birth), int(month_of_birth), int(date_of_birth))

    complete_dob = x.strftime('%Y-%m-%d')
    
    today = datetime.date.today()
    current_year = today.year
    
    age = current_year - int(year_of_birth)

    try:
        validated_email = validate_email(email).email # email is validated

        # CONFIRM IF THE EMAIL IS ALREADY IN THE DATABASE OR NOT
        data = User.objects.filter(email=validated_email)
        if data:
            new_data = {'data': {}, 'message': EMAIL_ALREADY_EXIST, 'status': 0}
        else:
            encrypted_password = sha256_crypt.encrypt(signup_password)
            data = User(first_name=first_name, last_name=last_name, date_of_birth=complete_dob, email=validated_email, phone_number=phone_number, age=age, password=encrypted_password)
            data.save()
            new_data = {'data': {'message': 'Data has been saved successfully'}, 'message': SUCCESS, 'status': 1}
        return JsonResponse(new_data)

    except EmailNotValidError as e:
        print(e)
        print(e)
        

def update_profile(request):
    if 'userEmail' in request.session:
         if data := User.objects.get(email=request.session['userEmail']):
            return render(request, 'update-profile.html', {"mydata":data})
    return render(request, 'update-profile.html')

def update_validation(request):
    if request.method != 'POST':
        return
    profile_pic = request.FILES.get('profile_pic', None)
    gender = request.POST.get("gender")
    religion = request.POST.get("religion")
    motherTongue = request.POST.get("motherTongue")
    userReligion = request.POST.get("userReligion")
    userMotherTongue = request.POST.get("userMotherTongue")

    if isEmpty(gender):
        return JsonResponse({'message': 'Please enter your gender', 'status': 0})

    if isEmpty(religion):
        return JsonResponse({'message': 'Please enter your religion', 'status': 0})

    if isEmpty(motherTongue):
        return JsonResponse({'message': 'Please enter your mother tongue', 'status': 0})

    try:
        if isEmpty(profile_pic) or profile_pic is None:
            print("profile pic is empty")
            if religion is None and motherTongue is None:
                if data := User.objects.get(email=request.session['userEmail']):
                    return updateUser(userReligion, data, gender, userMotherTongue)
            if data := User.objects.get(email=request.session['userEmail']):
                return updateUser(religion, data, gender, motherTongue)
        #     return
        
        if data := User.objects.get(email=request.session['userEmail']):
            if religion is None and motherTongue is None:
                data.profile_image = profile_pic
                data.religion = userReligion
                data.gender = gender
                data.mother_tongue = userMotherTongue
                data.save()
                return JsonResponse({'message': 'You details updated successfully', 'status': 1})
            
            data.profile_image = profile_pic
            data.religion = religion
            data.gender = gender
            data.mother_tongue = motherTongue
            data.save()
            return JsonResponse({'message': 'You details updated successfully', 'status': 1})
        print("work in progress")
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Something is wrong', 'status': 0})


# TODO Rename this here and in `update_validation`
def updateUser(religion, data, gender, mother_tongue):
    data.religion = religion
    data.gender = gender
    data.mother_tongue = mother_tongue
    data.save()
    return JsonResponse({'message': 'You details updated successfully', 'status': 1})

def profiles(request):
    if request.method != 'POST':
        return
    
    gender = request.POST.get("gender").lower()
    aged = request.POST.get("aged")
    religion = request.POST.get("religion").lower()
    motherTongue = request.POST.get("motherTongue").lower()
    
    try:
        if data := User.objects.filter(gender=gender, age=aged, religion=religion, mother_tongue= motherTongue):
            if new_data:= data.exclude(email=request.session['userEmail']):
                if userData:= User.objects.get(email=request.session['userEmail']):
                    return render(request, 'profiles.html', {'data': new_data,'userData': userData})
                return render(request, 'profiles.html', {'data': new_data})
        if userData:= User.objects.get(email=request.session['userEmail']):
            return render(request, 'profiles.html', {'userData': userData})
        return redirect('home')
    except Exception as e:
        print(e)