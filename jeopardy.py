import pandas as pd
import numpy as np
import math
import random
from bs4 import BeautifulSoup

pd.options.display.width = 0
pd.options.display.max_colwidth = 120
pd.options.display.max_rows = 0
data = pd.read_csv('Jeopardy.csv')

#Changing columns name to avoid issues in the future
data.columns = ["show_number", "air_date", "round", "category", "value", "question", 'answer']
#print(data.head())

#Defining a list of words to be found
words = ['city', 'state']

#Creating a function that finds the words of the previous list in the provided dataframe
def word_finder(lst):

    data_filtered = data.question[data['question'].apply(lambda x: all(word.lower() in x.lower() for word in lst))]
    return data_filtered

#print(word_finder(words))

#Creating a column with values from 'value' column, but as floats
data['clean_value'] = data['value'].apply(lambda x: float(x[1:].replace(',','')) if x[0] == '$' else 0)

#Creating a column with air dates as datetime-format
data['datetime'] = pd.to_datetime(data.air_date)

#Creating a column with text only, from 'question' column
data['question_clean'] = data['question'].apply(lambda x: BeautifulSoup(x, "html.parser").get_text())

#Rearranging the columns order
data2 = data.reindex(columns= ['show_number', 'datetime', 'round', 'category', 'clean_value', 'question_clean', 'answer'])

#Creating a function that finds the average value of questions containing a specific word, given by user.
def average_value_with_word():

    word = input("Please type in a word, so it's possible to calculate the average value of questions containing it.")
    data3 = data2[data2['question_clean'].str.contains(word)]
    average = data3.clean_value.mean()
    return "The average value of questions containing the word {} is ${}".format(word, round(average, 2))

#print(average_value_with_word())

#Finding how many unique answers are
#print(data3.answer.nunique())

###How many times does 'Computer' gets cited in questions along the decades (form 1990's to 2010's)?
###Does the percentage (related to the total of questions in the period) changes along time?
###Does the average value changes as well?

def word_along_time(df, word, start_date, end_date):

    df_temp_date = df.loc[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]
    df_temp_word = df.loc[(df['question_clean'].str.contains(word.lower() or word.upper() or word.title()))]
    df_merged = pd.merge(df_temp_date, df_temp_word)

    num_questions = len(df_merged)
    percent = round(len(df_merged)/len(df_temp_date)*100, 2)
    average = round(df_merged['clean_value'].mean(), 2)
    if math.isnan(average) == True: average = 0

    return "The word '{word}' can be found in {num_questions} question(s) between {start_date} and {end_date}, representing {percent}% of all questions in that period. " \
             "In this case, the average value was {average}".format(word=word, num_questions=num_questions, start_date=start_date, end_date=end_date, percent=percent, average=average)

#print(word_along_time(data2, 'Computer', '1990-1-1', '1999-12-31'))
#print(word_along_time(data2, 'Computer', '2000-1-1', '2009-12-31'))

def jeopardy():
    print("Welcome to an adapted version of Jeopardy! You have to correctly answer a question to win the game, with 3 chances. Good luck!")
    input("Press 'Enter' to start the game")
    for i in range(3):
        random_int = random.randint(0, len(data2))
        user_input = input("""
What's the answer to the following sentence?: 
'{}'""".format(data2.question_clean[random_int]))

        if user_input.lower() == data2.answer[random_int].lower():
            print('Well done! You won!')
            result = 'win'
            break
        else:
            print("What a shame, that's not correct.")
            print("The right answer was: {}".format(data2.answer[random_int]))
            result = 'lose'

    if result == 'win': print("Well played, congrats!")
    else: print("Bummer, you lose!")

#Calls the main function to play Jeopardy
#jeopardy()




