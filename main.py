import firebase_admin
from firebase_admin import credentials
import streamlit as st
from firebase_admin import storage

cred = credentials.Certificate("service_account.json")

firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://splitproject-653ea.appspot.com'
}, name='splitproject')

# Function to get image URLs from Firebase Storage
def get_image_urls_from_storage():
    # Code here
    image_urls = ""

    return image_urls

def main():
    st.title("View Images from Firebase Storage")

    # Get image URLs from Firebase Storage
    image_urls = get_image_urls_from_storage()

    # Display images
    if image_urls:
        st.subheader("Images from Firebase Storage")
        for url in image_urls:
            st.image(url, caption='Image from Firebase Storage', use_column_width=True)
    else:
        st.write("No images found in Firebase Storage.")

if __name__ == "__main__":
    main()