from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from firebase_manager.models import NfcTag, TrackingData
from firebase_manager.firebase_manager import FirebaseManager
from firebase_admin import db,auth
from datetime import datetime
import pytemperature
import time
import nfc



def signup(request):
    if request.method == 'POST':
        # Get data from form
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if the email and username already exist
        if existing_email(email):
            # Show error message for existing email
            return render(request, 'signup.html', {'error_message': 'Email already exists. Choose a different email.'})
        elif existing_username(username):
            # Show error message for existing username
            return render(request, 'signup.html', {'error_message': 'Username already exists. Choose a different username.'})
        else:
            # Email and username do not exist, proceed to add the new user
            data = {
                "user_name": username,
                "email": email,
                "password": password
            }
            ref = db.reference("/")
            ref.child("Users").child(username).set(data)
            print("Signup successfully")
            
            # Redirect to login page
            return redirect('login')

    return render(request, 'signup.html')

def existing_email(email):
    ref = db.reference("Users")
    user_data = ref.get()
    if user_data:
        for user_id, user_info in user_data.items():
            if user_info.get('email') == email:
                return True
    return False

def existing_username(username):
    ref = db.reference("Users")
    user_data = ref.get()
    if user_data:
        return username in user_data
    return False

def login(request):
    if request.method == 'POST':
        # Get data from the form
        email = request.POST['email']
        password = request.POST['password']

        ref = db.reference('Users')
        user_data = ref.get()

        if user_data:
            for user_id, user_info in user_data.items():
                
                if user_info.get('email') == email:
                    if user_info.get('password') == password:
                        # Password is correct, redirect to home
                        return redirect('home')
                    else:
                        # Password is incorrect, show error message
                        return render(request, 'login.html', {'error_message': 'Incorrect password.'})
            
            # Email not found in the loop, show error message
            return render(request, 'login.html', {'error_message': 'User with this email not found.'})

        else:
            # User data is empty, show error message
            return render(request, 'login.html', {'error_message': 'User not found.'})

    return render(request, 'login.html')

def logout(request):
    logout(request)
    return redirect('login')


def write(request):
    if request.method == 'POST':
        # Get data from form
        product_name = request.POST['product_name']
        batch_no = request.POST['batch_no']
        model_no = request.POST['model_no']
        manufacture_date = request.POST['manufacture_date']
        expiry_date = request.POST['expiry_date']
        source_address = request.POST['source_address']
        destination_address = request.POST['destination_address']
        quantity = request.POST['quantity']
        min_temp = request.POST['min_temp']
        max_temp = request.POST['max_temp']
        tag_id=request.POST['tag_id']
        # Write data to NFC tag
        data={
            "Product_name":product_name,
            "Batch_no":batch_no,
            "Model_no":model_no,
            "Manufacture_date":manufacture_date,
            "Expiry_date":expiry_date,
            "Source_address":source_address,
            "Destination_address":destination_address,
            "Quantity":quantity,
            "Min_temp":min_temp,
            "Max_temp":max_temp
        }
        ref=db.reference("/")
        ref.child("Tag_Details").child(tag_id).set(data)

        # Redirect to home page
        return redirect('home')

    return render(request, 'write.html')


def read(request):
    if request.method == 'POST':
        # Get NFC tag ID and location from the user
        tag_id = request.POST['tag_id']
        location = request.POST['location']
        time=datetime.now().isoformat()
        data={
            "Location": location,
            "Time":time
        }
        ref=db.reference("/")
        db_path = f"Tag_Details/{tag_id}/Locations"
        ref.child(db_path).child(location).set(data)
        ref.child("Tag_Details").child(tag_id).child("Place_of_arriving").set(location)
        product_details=ref.child("Tag_Details").child(tag_id).get()

        return render(request, 'readed.html', {'Product_details': product_details})

    return render(request, 'read.html')




def track(request):
    tag_id = None  # Initialize tag_id to None
    
    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')  # Use get method to avoid MultiValueDictKeyError

    if tag_id:
        ref = db.reference("/")
        db_path = f"Tag_Details/{tag_id}/Locations"
        tracking_data = ref.child(db_path).get()
        product_details=ref.child("Tag_Details").child(tag_id).get()
        print("location retrived")
        return render(request, 'tracked.html', {'tracking_data': tracking_data,'Product_details': product_details})
    
    else:
        print("no locations available")
        return render(request, 'track.html', {'error_message': 'Tag ID not provided.'})


def home(request):
    return render(request, 'home.html')