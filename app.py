from glob import escape
from textwrap import indent
import streamlit as st
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

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

eras_program = pd.read_excel('erasmus_programs.xlsx')
eras_program = eras_program.dropna(subset=['Related Course of Study'])
def to_remove_bracket_split(courses):
    courses = courses.replace('[','').replace(']','')
    course_split = courses.split(',')
    course_split = [course.strip().lower() for course in course_split]
    return course_split

def to_match_words(words_to_match,main_word,ratio_fuzzy):
    fuzzy_ratio = fuzz.ratio(words_to_match.lower(),main_word.lower())
    if fuzzy_ratio >= ratio_fuzzy:
        return True
    else:
        return False

def take_list_search(list_courses,word_to_match,ratio_fuzzy):
    word_to_match = word_to_match.lower()
    list_courses = to_remove_bracket_split(list_courses)
    for course in list_courses:
        course_list = course.split(' ')
        course_list = [each_course for each_course in course_list if len(each_course) > 3]
        for inner_course in course_list:
            found_match = to_match_words(inner_course,main_word=word_to_match,ratio_fuzzy=ratio_fuzzy)
            if found_match == True:
                return True
    return False

def search_program_name(program_name,word_to_search,ratio_fuzzy):
    word_to_search = word_to_search.lower()
    program_name = program_name.replace('(','').replace(')','')
    program_name_split = program_name.split(' ')
    program_name_list_lower = [program_name_each.lower().replace(',','').replace(':','').replace('&','') for program_name_each in program_name_split if len(program_name_each) >3]
    
    for program in program_name_list_lower:
        program_list = program.split(' ')
        program_list = [each_program for each_program in program_list if len(each_program) > 3]
        found_program = False
        for inner_program in program_list:
            found_match = to_match_words(inner_program,main_word=word_to_search,ratio_fuzzy=ratio_fuzzy)
            if found_match == True:
                return True
    return False
    

def input_words_to_search(words,ratio_fuzzy):
    words_list = words.split(' ')
    words_list = [each_word for each_word in words_list if len(each_word) > 3]
    final_df = pd.DataFrame()
    for each_word in words_list:
        test_cour_series = eras_program['Related Course of Study'].apply(take_list_search,args= (each_word,ratio_fuzzy,))
        new_eras_prog = eras_program[list(test_cour_series)]
        final_df = pd.concat([new_eras_prog,final_df])
    for each_word_prog in words_list:
        test_cour_series = eras_program['Program Full Name'].apply(search_program_name,args= (each_word_prog,ratio_fuzzy,))
        new_eras_prog = eras_program[list(test_cour_series)]
        final_df = pd.concat([new_eras_prog,final_df])
    
    return final_df.drop_duplicates(subset='Erasmus Program').reset_index().drop('index',axis=1)[['Erasmus Program', 'Program Full Name', 'Program Website',
       'Related Course of Study']]

def search_awardee_details(program_name,search_program_name,ratio_fuzzy):
    found_match = to_match_words(program_name.lower(),search_program_name.lower(),ratio_fuzzy)
    if found_match == True:
        return True
    return False

def get_awardee_details(search_program_name,ratio_fuzzy):
    words_list = search_program_name.replace('/',' ').replace('-',' ').split()
    final_df = pd.DataFrame()
    for each_word in words_list:
        awardee_df = eras_awardee_details[list(eras_awardee_details['Program'].apply(search_awardee_details,args=(search_program_name,ratio_fuzzy,)))]
        final_df = pd.concat([awardee_df,final_df])
    return awardee_df.reset_index().drop('index',axis=1)

def head():
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: -35px;'>
        MyErasmusFinder 
        </h1>
    """, unsafe_allow_html=True)
    
    st.write(
        "You are welcome to MyErasmusFinder Platform.",
        "MyErasmusFinder is a platform for searching for relevant Erasmus Mundus Joint Masters Degree Programs with the click of the Button.",
        "This is not related to the European Union nor endorsed by Erasmus Plus \U0001F642.",
    )
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://unsplash.com/photos/_ts3NfjvaXo");
    background-size: cover;
    position: absolute;
    top: 0px;
    right: 0px;
    bottom: 0px;
    left: 0px;
    background-color: rgba(0,0,0,0);
}
footer {
    visibility: hidden;
}
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
<div class ="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://www.linkedin.com/in/ilekuraidowu/" target="_blank">Idowu Oselumhe Ilekura(Linkedln)</a></p>
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://twitter.com/idowuilekura/" target="_blank">Idowu Oselumhe Ilekura(Twitter)</a></p>
</div>
'''
st.markdown(page_bg_img,unsafe_allow_html=True)
head()
body_erasm = st.container()
with body_erasm:
    st.subheader("Search for your Prefered Erasmus Program")
    st.text("\
            You can search for your preferred Erasmus Mundus course by typing the course name \ninside the box. Kindly avoid abbreviations while typing the course name for instance \nyou should type Mathematics instead of Maths.You can search for more than one course\nYou just need to seperate the courses with a space, for instace if you are \nsearching for a course that is related to Biology Science and Mathematical Science \nyou will need to type Biology Science and Mathematical Science. \nYou can choose to omit the and but ensure you replace the add with a space.\nIf you choose to search for a single course with more than two words ensure you \nseperate each words with a space e.g Biology Science instead of BiologyScience")
        
    user_input = st.text_input("Type your course of study inside the box, click on the Enter Button on your keyboard once you are done. Click on the Search Button for result")

    btn = st.button('search')

    if btn:
        final_df = input_words_to_search(str(user_input),ratio_fuzzy=70)
        if len(final_df) >0:
            st.write('Find below relevant erasmus programs that match your search, scroll to your left for more information')
            st.write(final_df.to_html(escape=False,index=False),unsafe_allow_html=True)
        else:
            st.write("Oops the course you searched for couldn't be found, kindly use a different or similar keyword",
                    "Erasmus Mundus Program are interwovened, i.e a single program can combine several fields of study",
                "Instead of searching for petroleum engineering, you can search for chemical engineering or energy engineering."
                )



    st.subheader("Search for Profiles of Erasmus Awardees")
    st.text("\
            Below, you can search for the profiles of Scholars from Nigeria,who got accepted \ninto specific Erasmus Programs. Ensure you type the acronym and not the full program \nname. If you don't know the acronym, you can firstly search for the Erasmus program \nand then copy the acronym into the box below.")
    
    user_input_awardee = st.text_input('Kindly type the Erasmus Mundus course acronym, and not the full name e.g Type Emplant as against the full name')
    
    btn_awardee = st.button('get awardee details')

    if btn_awardee:
        awardee_df = get_awardee_details(str(user_input_awardee),76)
        if len(awardee_df) > 0:
            st.write('Find below the Profile of Erasmus Scholars from Nigeria that match your search, scroll to your left for more information')
            st.write(awardee_df.to_html(escape=False,index=False),unsafe_allow_html=True)

        else:
             st.write("Oops there are no Nigerian Awardee for  you searched for couldn't be found, kindly use a different or similar keyword",
                    "Erasmus Mundus Program are interwovened, i.e a single program can combine several fields of study",
                "Instead of searching for petroleum engineering, you can search for chemical engineering or energy engineering."
                )


