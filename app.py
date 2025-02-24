import streamlit as st
from PIL import Image

def main():
    st.title("Art Therapy Analysis Tool")
    st.write("Upload your artwork for analysis and interpretation")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Artwork", use_column_width=True)

if __name__ == "__main__":
    main() 