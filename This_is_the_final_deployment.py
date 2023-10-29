import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import base64

st.set_page_config(page_title = "College_checker", page_icon=":smiling_face_with_horns:", layout = "wide")
#Background image
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    backdrop-filter: blur(1000px);
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background(r"udents-smiling-talking-social-campus.webp")

# Load your college data into a DataFrame (assuming you have a DataFrame named df)
college_data = pd.read_csv("Clean college rankings.csv")

def recommend_colleges(course_fee_max, review_score_min, average_package_min, highest_package, cutoff_rank, num_colleges):
    # Filter colleges based on the student's criteria
    filtered_colleges = college_data[
        (college_data["course_fees"] <= course_fee_max) &
        (college_data["review"] >= review_score_min) &
        (college_data["Average Package"] >= average_package_min) &
        (college_data["Highest Package"] >= highest_package) &
        (college_data["Cutoff rank in CSE"] >= cutoff_rank)
    ]

    # Return the top recommended colleges, limited to the specified number
    return filtered_colleges.head(num_colleges)

# Header section
st.subheader("Check this page out")
st.title("")
st.write("Hey there, future engineer! Welcome to our college recommendation page. Based on your hard work, you can check in which college you can get the Computer Science branch")

# Body section
left_column, right_column = st.columns(2)
# def load_lottieurl(url):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_college = load_lottieurl("https://lottie.host/63160ac6-2091-43db-a153-49ab78c5a0cb/YDB40RDjYR.json")

# with right_column:
#     if lottie_college is not None:
#         st_lottie(lottie_college, height = 300, key = "coding")
#     else:
#         st.write("Lottie animation could not be loaded.")

with left_column:
    # Input criteria from the student
    course_fee_max = st.number_input('Enter the course fees')
    review_score_min = st.number_input('Enter the review for college')
    average_package_min = st.number_input('Enter the average package')
    highest_package = st.number_input('Enter the highest package')
    cutoff_rank = st.number_input('Enter a cutoff rank for CSE')

    # Ask the user for the number of colleges to display
    num_colleges_to_display = int(st.number_input('Enter the number of college you would like to see'))

    # Recommend the colleges that match the entered criteria
    recommended_colleges = recommend_colleges(course_fee_max, review_score_min, average_package_min, highest_package, cutoff_rank, num_colleges_to_display)

    # Display the recommended colleges
    st.write("Recommended colleges:")
    if recommended_colleges is not None and not recommended_colleges.empty:
        st.table(recommended_colleges)
    else:
        st.write("No colleges match the specified criteria.")
