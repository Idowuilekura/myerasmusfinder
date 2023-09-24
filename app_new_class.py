import streamlit as st

def search_courses():
    # Implement your course search functionality here
    st.write("Course search results")

def search_awardees():
    # Implement your awardee search functionality here
    st.write("Awardee search results")

# Set page configuration
st.set_page_config(page_title="MyErasmusFinder", page_icon=":mag:", layout="wide")

# Set background color
st.markdown(
    """
    <style>
    body {
        background-color: #004494;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add title and description
st.title("Welcome to MyErasmusFinder Platform!")
st.write("MyErasmusFinder is a user-friendly platform designed to help you search for relevant Erasmus Mundus Joint Masters Degree Programs with just a click of a button. Please note that this platform is an independent initiative and is not directly affiliated with the European Union or endorsed by Erasmus Plus.")

# Add an expandable section for search guidelines
st.markdown(
    """
    <details>
    <summary><strong>Search for your Preferred Erasmus Program</strong></summary>
    
    To search for your preferred Erasmus Mundus course, follow these guidelines:
    - Type the complete name of the course you are searching for inside the provided box.
    - Avoid using abbreviations when typing the course name. For example, use "Mathematics" instead of "Maths".
    - You can search for multiple courses simultaneously. Simply separate each course name with a space. For instance, if you are searching for courses related to Biology Science and Mathematical Science, type "Biology Science Mathematical Science" in the search box.
    - If you prefer, you can omit the word "and" and replace it with a space while searching for multiple courses.
    - When searching for a single course with multiple words, ensure that you separate each word with a space. For example, type "Biology Science" instead of "BiologyScience".
    
    These guidelines will help you effectively search for your preferred Erasmus Mundus courses using the search box.
    </details>
    """,
    unsafe_allow_html=True
)

# Create a sidebar
st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #004494;
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add the "Developed with ❤" section to the sidebar
st.sidebar.markdown(
    """
    Developed with ❤ by
    [Idowu Oselumhe Ilekura (LinkedIn)](https://www.linkedin.com/in/your-linkedin-profile) |
    [Idowu Oselumhe Ilekura (Twitter)](https://www.twitter.com/your-twitter-profile)
    """,
    unsafe_allow_html=True
)

# Course search section
course_search = st.text_input("Search Courses")
course_button = st.button("Search Courses")
if course_button:
    search_courses()

# Awardee search section
awardee_search = st.text_input("Search Awardees")
awardee_button = st.button("Search Awardees")
if awardee_button:
    search_awardees()


# import streamlit as st

# def search_courses():
#     # Implement your course search functionality here
#     st.write("Course search results")

# def search_awardees():
#     # Implement your awardee search functionality here
#     st.write("Awardee search results")

# # Set page configuration with blue background color
# st.set_page_config(page_title="MyErasmusFinder", page_icon=":mag:", layout="wide", theme="primary color")

# # Add title and description
# st.title("Welcome to MyErasmusFinder Platform!")
# st.write("MyErasmusFinder is a user-friendly platform designed to help you search for relevant Erasmus Mundus Joint Masters Degree Programs with just a click of a button. Please note that this platform is an independent initiative and is not directly affiliated with the European Union or endorsed by Erasmus Plus.")

# # Add an expandable section for search guidelines
# st.markdown(
#     """
#     <details>
#     <summary><strong>Search for your Preferred Erasmus Program</strong></summary>
    
#     To search for your preferred Erasmus Mundus course, follow these guidelines:
#     - Type the complete name of the course you are searching for inside the provided box.
#     - Avoid using abbreviations when typing the course name. For example, use "Mathematics" instead of "Maths".
#     - You can search for multiple courses simultaneously. Simply separate each course name with a space. For instance, if you are searching for courses related to Biology Science and Mathematical Science, type "Biology Science Mathematical Science" in the search box.
#     - If you prefer, you can omit the word "and" and replace it with a space while searching for multiple courses.
#     - When searching for a single course with multiple words, ensure that you separate each word with a space. For example, type "Biology Science" instead of "BiologyScience".
    
#     These guidelines will help you effectively search for your preferred Erasmus Mundus courses using the search box.
#     </details>
#     """,
#     unsafe_allow_html=True
# )

# # Create a sidebar
# st.sidebar.markdown(
#     """
#     <style>
#     .sidebar .sidebar-content {
#         background-color: #007bff;
#         padding: 10px;
#         color: white;
#         text-align: center;
#         font-size: 14px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Add the "Developed with ❤" section to the sidebar
# st.sidebar.markdown(
#     """
#     Developed with ❤ by
#     [Idowu Oselumhe Ilekura (LinkedIn)](https://www.linkedin.com/in/your-linkedin-profile) |
#     [Idowu Oselumhe Ilekura (Twitter)](https://www.twitter.com/your-twitter-profile)
#     """,
#     unsafe_allow_html=True
# )

# # Course search section
# course_search = st.text_input("Search Courses")
# course_button = st.button("Search Courses")
# if course_button:
#     search_courses()

# # Awardee search section
# awardee_search = st.text_input("Search Awardees")
# awardee_button = st.button("Search Awardees")
# if awardee_button:
#     search_awardees()
