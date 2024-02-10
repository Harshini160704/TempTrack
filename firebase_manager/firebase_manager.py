import firebase_admin
from firebase_admin import db,auth
from .models import TrackingData
import datetime

# Initialize Firebase Admin SDK
firebase_app = firebase_admin.get_app()

# Define reference to the root of the Firebase Realtime Database
ref = db.reference("/",app=firebase_app)

class FirebaseManager:
    """Firebase Manager class."""

    def create_user(self, email, password, display_name):
        try:
            user = auth.create_user(email=email, password=password, display_name=display_name)
            print("Signup successful")
            print(f"User ID: {user.uid}")
        # You can store the user ID or perform other actions after successful signup
        except Exception as e:
            print(f"Signup failed: {e}")
    
    @staticmethod
    def save_tracking_data(tag_id, temperature, location):
        """Save tracking data to Firebase."""
        # Generate a unique key for each tracking data entry
        key = ref.push().key
        # Create a TrackingData object
        tracking_data = TrackingData(tag_id=tag_id, temperature=temperature, location=location, time=datetime.datetime.now())
        # Save the object to Firebase
        ref.child('tracking_data').child(key).set(tracking_data.to_dict())

    @staticmethod
    def get_tracking_data(tag_id):
        """Retrieve tracking data for a given NFC tag."""
        # Get all tracking data for the given tag_id
        tracking_data_list = ref.child('tracking_data').order_by_child('tag_id').equal_to(tag_id).get()
        # Convert the retrieved data to a list of TrackingData objects
        return [TrackingData(**data) for data in tracking_data_list]
