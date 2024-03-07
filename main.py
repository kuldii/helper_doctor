import firebase_admin
from firebase_admin import credentials, storage
import streamlit as st
from google.cloud import firestore
from PIL import Image
import io
import uuid

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
    
    st.title("Select doctor:")
    selected_option = st.selectbox(
        label='Select doctor:',
        label_visibility="hidden",
        options=('none', 'Doctor A', 'Doctor B', 'Doctor C')
    )
    
    if(selected_option != "none"):
        # Authenticate to Firestore with the JSON account key.
        db = firestore.Client.from_service_account_json("service_account.json")
        
        if(selected_option == "Doctor A"):
            all_docs = db.collection("doctorA").get()
            dict_selected_images = dict()
            for doc in all_docs:
                data = doc.to_dict()
                dict_selected_images[data["image"]] = data["status"]
            
            st.title("All Image Files:")
            for image_path in file_paths:
                blob = bucket.blob(image_path)
                image_name = blob.name
                image_bytes = blob.download_as_bytes()
                
                if image_bytes:
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, use_column_width=True)
                    unique_key = str(uuid.uuid4())
                    options = ['none', 'Good', 'Std 1', 'Std 2', 'Std 3']
                    selected_option_index = options.index(dict_selected_images[image_name]) if image_name in dict_selected_images else 0
                    
                    status = st.radio(
                        key=unique_key,
                        label='Select status:',
                        options=options,
                        index=selected_option_index
                    )
                    
                    # Need logic to update when doctor change the option
                    # if image_name in dict_selected_images:
                    #     if(status != dict_selected_images[image_name]):
                    #         doc_ref = db.collection("doctorA").document(doc.id)
                    #         doc_ref.update({"status": status})
                    
                else:
                    st.write("Image not found.")

if __name__ == "__main__":
    main()