import streamlit as st
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

from utils import * 

import streamlit as st

# Set page configuration
# st.set_page_config(page_title="MyErasmusFinder", page_icon=":mag:", layout="wide")
# st.image('path_to_your_logo.png', width=200, use_container_width=True)
# st.write("<div style='display: flex; justify-content: center; align-items: center;'>", unsafe_allow_html=True)

# # Display the logo image and title
# st.image('./MYERASMUSFINDER.png', width=500)
# st.title("MyErasmusFinder")
st.set_page_config(page_title="MyErasmusFinder", page_icon=":mag:", layout="wide")
custom_css = """
<style>
    body {
        color: #2596be; /* Change the text color to your desired color */
    }
</style>
"""

# Apply the custom CSS to the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)

# Rest of your Streamlit code

# Close the row layout
st.write("</div>", unsafe_allow_html=True)
# Center-align the title and adjust its position relative to the logo
# st.markdown("""
#     <h1 style='text-align: center; margin-top: -100px;'>MyErasmusFinder</h1>
#     <p style='text-align: center;'>Subtitle or additional information goes here.</p>
# """, unsafe_allow_html=True)

# Set background color 
st.markdown(
    """
    <style>
    body {
        background-color: #2596be;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add title and description
# st.title("Welcome to MyErasmusFinder Platform!")
st.markdown("""
    <h1 style='text-align: center;'>Welcome to MyErasmusFinder Platform!</h1>
""", unsafe_allow_html=True)

st.write("MyErasmusFinder is a user-friendly platform designed to help you search for relevant Erasmus Mundus Joint Masters Degree Programs with just a click of a button. Please note that this platform is an independent initiative and is not directly affiliated with the European Union or endorsed by Erasmus Plus.")


@st.cache_data
def read_eras_file():
    eras_file = pd.read_excel('New_Erasmus Program Selection Aid.xlsx')
    eras_awardee_details = eras_file.drop('S/N',axis=1
                )
    mymap = {'NIL':np.NaN} 
    eras_awardee_details= eras_awardee_details.applymap(lambda x: mymap.get(x) if x in mymap else x).dropna(subset=['University'])
    grade_map = {1.0:'First Class',2.1:'Second Class Upper',2.2:'Second Class Lower'}
    eras_awardee_details['Grade']=eras_awardee_details['Grade'].apply(lambda x: grade_map.get(x) if x in grade_map else x)
    eras_awardee_details['Year'] = eras_awardee_details.Year.astype(int).astype(str)
    mymap_new = {np.NaN:'None'}
    eras_awardee_details= eras_awardee_details.applymap(lambda x: mymap_new.get(x) if x in mymap_new else x)
    return eras_awardee_details

eras_awardee_details = read_eras_file()

@st.cache_data
def read_eras_program():
    eras_program = pd.read_excel('erasmus_programs.xlsx')
    eras_program = eras_program.dropna(subset=['Related Course of Study'])
    return eras_program

eras_program = read_eras_program()

body_erasm = st.container()
#with body_erasm:
    #st.subheader("Search for your Prefered Erasmus Program")
    #st.text("\
          #  You can search for your preferred Erasmus Mundus course by typing the course name \ninside the box. Avoid abbreviations while typing the course name; for instance, \nyou should type Mathematics instead of Maths. You can search for more than one course\nYou just need to separate the courses with space; for instance, if you are \nsearching for a course related to Biology Science and Mathematical Science, \nyou will need to type Biology Science and Mathematical Science. \nYou can choose to omit the and but ensure you replace the add with a space.\nIf you decide to search for a single course with more than two words ensure you \nseperate each words with a space e.g., Biology Science instead of BiologyScience")
    

def search_courses(course_search):
    #user_input = st.text_input("Type your course of study inside the box, click on the Enter Button on your keyboard once you are done. Click on the Search Button for result")

    # btn = st.button('search')

    if len(str(course_search)) > 1:
        final_df = input_words_to_search(str(course_search),ratio_fuzzy=70,eras_program=eras_program)
        if len(final_df) >0:
            # st.write('Here are the Erasmus programs that closely match your search. You can scroll to the left for more information')
            # st.write(final_df.to_html(escape=False,index=False),unsafe_allow_html=True)
            collapse_programs_df = st.expander("Click to Expand/Collapse Erasmus Programs")
            with collapse_programs_df:
                st.write('Here are the Erasmus programs that closely match your search. You can scroll to the left for more information')
                st.write(final_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.write("Oops, the course you searched for couldn't be found; kindly use a different or similar keyword.",
    "Erasmus Mundus Program are interwoven, i.e., a single program can combine several fields of study.",
    "Instead of searching for petroleum engineering, you can search for chemical or energy engineering."
                    )
    else:
        st.write("Oops, enter a valid word into the box")
    # Implement your course search functionality here
    st.write("Course search results")

def search_awardees(course_name):
    # Implement your awardee search functionality here
    if len(str(course_name)) > 1:
        awardee_df = get_awardee_details(str(course_name),76,eras_awardee_details=eras_awardee_details)
        if len(awardee_df) > 0:
            st.write('Find below the Profile of Erasmus Scholars from Nigeria that match your search, scroll to your left for more information')
            # st.write(awardee_df.to_html(escape=False,index=False),unsafe_allow_html=True)
            collapse_awardee_df = st.expander("Click on ► to Expand/Collapse Awardee Details")
            with collapse_awardee_df:
                st.write(awardee_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
             st.write("Oops, there are no Nigerian awardees for the program you searched for; it couldn't be found. Kindly use a different or similar keyword.",
    "Erasmus Mundus Programs are interwoven, i.e., a single program can combine several fields of study.",
    "Instead of searching for petroleum engineering, you can search for chemical engineering or energy engineering."
                )
    else:
        st.write("Oops, enter a valid word into the box")
    # st.write("Awardee search results")


# Add an expandable section for search guidelines


# Create a sidebar
st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #007bff;
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

st.markdown(
    """
   <p>Click ► below to expand and learn how to search for your preferred Erasmus Mundus Program:</p>

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
# Course search section
course_search = st.text_input("Search Courses")
course_button = st.button("Search Courses")
if course_button:
    search_courses(course_search=course_search)

st.markdown(
    """
   <p>Click ► to expand and learn how to search for profiles of Erasmus awardees:</p>

<details>
    <summary><strong>Search for Profiles of Erasmus Awardees</strong></summary>
    
    - Below, you have the option to search for profiles of scholars from Nigeria who were accepted into specific Erasmus Programs.
    - Please make sure to enter the program acronym - not the full program name.
    - If you are unsure of the acronym, you can first search for the Erasmus program and then copy the acronym into the box below.
    - These guidelines will help you effectively search for profiles of Erasmus awardees from Nigeria using the search box.
</details>
    """,
    unsafe_allow_html=True
)
# Awardee search section
awardee_search = st.text_input("Search Awardees")
awardee_button = st.button("Search Awardees")
if awardee_button:
    search_awardees(course_name=awardee_search)


