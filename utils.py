import pandas as pd
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

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
    

def input_words_to_search(words,ratio_fuzzy,eras_program):
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

def get_awardee_details(search_program_name,ratio_fuzzy,eras_awardee_details):
    words_list = search_program_name.replace('/',' ').replace('-',' ').split()
    final_df = pd.DataFrame()
    for each_word in words_list:
        awardee_df = eras_awardee_details[list(eras_awardee_details['Program'].apply(search_awardee_details,args=(search_program_name,ratio_fuzzy,)))]
        final_df = pd.concat([awardee_df,final_df])
    return awardee_df.reset_index().drop('index',axis=1)