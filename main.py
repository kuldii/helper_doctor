import firebase_admin
from firebase_admin import credentials, storage
import streamlit as st
from google.cloud import firestore
from PIL import Image
import io

def initialize_app():
    # Initialize Firebase SDK
    cred = credentials.Certificate("service_account.json")
    if not firebase_admin._apps:
        app = firebase_admin.initialize_app(cred, {
            'storageBucket': 'splitproject-653ea.appspot.com'
        }, name='splitproject')
    else:
        app = firebase_admin.get_app('splitproject')
    return app

def main():
    app = initialize_app()
    
    st.title("View Images from Firebase Storage")
    
    # Authenticate to Firestore with the JSON account key.
    db = firestore.Client.from_service_account_json("service_account.json")

    # Create a reference to the Google post.
    doc_ref = db.collection("tests").document("sItSpfHhKoDy9MEXE3KW")

    # Then get the data at that reference.
    doc = doc_ref.get()

    # Let's see what we got!
    st.write("The id is: ", doc.id)
    st.write("The contents are: ", doc.to_dict())

    # Image path in Firebase Storage
    image_path = 'raw/2.png'
    
    bucket = storage.bucket(app=app)
    blob = bucket.blob(image_path)
    image_bytes = blob.download_as_bytes()
    
    if image_bytes:
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption='Image from Firebase Storage', use_column_width=True)
    else:
        st.write("Image not found.")

if __name__ == "__main__":
    main()