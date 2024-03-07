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

def list_files_in_bucket(bucket):
    blobs = bucket.list_blobs()

    file_paths = []
    for blob in blobs:
        file_paths.append(blob.name)

    return file_paths

def main():
    app = initialize_app()
    
    bucket = storage.bucket(app=app)
    
    file_paths = list_files_in_bucket(bucket)

    st.title("All Image Files:")
    for image_path in file_paths:
        blob = bucket.blob(image_path)
        image_name = blob.name
        image_bytes = blob.download_as_bytes()
        
        if image_bytes:
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption=image_name, use_column_width=True)
        else:
            st.write("Image not found.")
    
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

if __name__ == "__main__":
    main()