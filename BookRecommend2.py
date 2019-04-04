# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:40:08 2019

@author: Bhaskar Rao
"""

import tensorflow
import itertools
import numpy as np
import pandas as pd
from rake_nltk import Rake
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from rake_nltk import Rake
import json
#df = pd.read_csv('C:/Users/Bhaskar Rao/Downloads/IMDB_Top250Engmovies2_OMDB_Detailed.csv')
pd.set_option('display.max_columns', 100)

# TO SET THE PATH OF THE BELOW CSVS
#D:/Study/Masters/Adaptive Applications/UserModel.csv
#D:/Study/Masters/Adaptive Applications/bookrecommendationdata.csv

#################################### Data Load and preprocessing #################################################################

bookDFComplete = pd.read_csv('D:/Study/Masters/Adaptive Applications/bookrecommendationdata.csv',sep=',',encoding = "ISO-8859-1")
bookDFComplete.head()
bookDF = bookDFComplete[['genreVector','Book','Author','Summary']]



### Book  database preprocessing
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


bookDF['Author'] = bookDF['Author'].map(lambda x: x.split(',')[:3])

# putting the genres in a list of words
bookDF['genreVector'] = bookDF['genreVector'].map(lambda x: x.lower().split(','))



for index, row in bookDF.iterrows():
    row['Author'] = [x.lower().replace(' ','') for x in row['Author']]
    row['genreVector'] = [x.lower().replace(' ','') for x in row['genreVector']]
    row['genreVector'] = ''.join(row['genreVector']).lower()


bookDF['Key_words'] = ""

for index, row in bookDF.iterrows():
    plot = row['Summary']
    
    # instantiating Rake, by default is uses english stopwords from NLTK
    # and discard all puntuation characters
    r = Rake()

    # extracting the words by passing the text
    r.extract_keywords_from_text(plot)

    # getting the dictionary whith key words and their scores
    key_words_dict_scores = r.get_word_degrees()
    
    # assigning the key words to the new column
    row['Key_words'] = list(key_words_dict_scores.keys())

# dropping the Plot column
bookDF.drop(columns = ['Summary'], inplace = True)

bookDF.set_index('Book', inplace = True)

bookDF['bag_of_words'] = ''
columns = bookDF.columns
for index, row in bookDF.iterrows():
    words = ''
    for col in columns:
        if col != 'genreVector':
            words = words + ' '.join(row[col])+ ' '
        else:
            words = words + row[col]+ ' '
    row['bag_of_words'] = words
    
bookDF.drop(columns = [col for col in bookDF.columns if col!= 'bag_of_words'], inplace = True)


#reading the user models DB
userDB = pd.read_csv('D:/Study/Masters/Adaptive Applications/UserModel.csv',sep=',',encoding = "ISO-8859-1")

############################################  Function 1 : Books Info based on Genre    ####################################################################################
# this function gives the top 5 books based on the require Genres
# input: genre name , can pass multiple genres as list
# output: A json object of book names and Genre values.

#def topBooksForGenre(genre,output):
#    topBooksDF = bookDFComplete.loc[bookDFComplete['genreVector'] == genre].head(5)
#    if output == "Data": print(topBooksDF) #return topBooksDF      pr         
#    if output == "Names":
#            topBookNames = []
#            for index, rows in topBooksDF.iterrows(): 
#                     # Create list for the current row 
#                tempListBookname = rows.Book
#                    # append the list to the final list 
#                topBookNames.append(tempListBookname) 
#            return  topBookNames         
        
def topBooksForGenre(genre):
    topBookNames = pd.DataFrame(columns=['genreVector','Book','Author','Summary','bookcoverURL','BookUrlGoodread'])
    for x in genre: 
          topBooksDFTemp = bookDFComplete.loc[bookDFComplete['genreVector'] == x].head(5)
          topBookNames = topBookNames.append(topBooksDFTemp)
    topBookNamesDict = topBookNames[["genreVector","Book"]].to_dict()
    return json.dumps(topBookNamesDict)
    
        
# bookjson=json.dumps(topBookNames)
 #               print(bookjson)
  #              arr = {'1':1,'2':2,'3':3,'4':4,'5': [2,23,23],'6': 456}
   #             b = (json.dumps(arr))

# function test
            
#genre = "Mystery"
genre = ["Mystery","Humor"]
      #output = "Names"
#output = "Data"
topBooksForGenre(genre)
            
############################################  Function 2 : Books Info based on Bookname    ####################################################################################        
# this function provides the dataset which has the information about the genre,author, summary, goodread url, Cover picture Url.
# input: bookname, note please provide only a single name at a time and don't pass list
# output: json object with all the information about the book
            
        
def bookInfo(bookName):
        bookInfoDF = bookDFComplete.loc[bookDFComplete['Book'] == bookName]
        bookInfoDFDict = bookInfoDF.to_dict()
        return json.dumps(bookInfoDFDict)

# function test
#bookName = "And Then There Were None"
# bookName = ["And Then There Were None"  ,"Gone Girl"] , failed
# bookInfo(bookName)     

############################################  Function 3 : User Model    ####################################################################################

# function to add the liked books to the user model
# input: user name, list of books liked by the user (likedBookVector)
# output: stores the information into a CSV file

def storeUserLikedBooks(userName,likedBookVector,userDB = userDB):
    userDataTemp = pd.DataFrame()
    userName1 = None
    userName1 =  np.repeat(userName,len(likedBookVector))
    userDataTemp["User"]= userName1
    userDataTemp["likes"] = likedBookVector
    
    finalUserDF = userDB.append(userDataTemp)
    finalUserDF.drop_duplicates(  keep = 'first', inplace = True) 
    finalUserDF.to_csv('D:/Study/Masters/Adaptive Applications/UserModel.csv', sep=',', encoding='ISO-8859-1',index=False)


#function test
#userName = 'user_3'
#likedBookVector = ["Divergent","Fool"]
#storeUserLikedBooks(userName,likedBookVector)

############################################   Function 4 : Recommendation  ####################################################################################

##function to generate recommendations based on the user and his mood
## input : user name and emotion
## output : json object with top 3 recommended books and thier Genre

def recommendations(userName,emotion):
    userDB = pd.read_csv('D:/Study/Masters/Adaptive Applications/UserModel.csv',sep=',',encoding = "ISO-8859-1")
    userDataRemdFilt = userDB[userDB.User.isin([userName])]
    userLikedBooksList = []

# Iterate over each row 
    for index, rows in userDataRemdFilt.iterrows(): 
        # Create list for the current row 
        tempListUser = rows.likes
      # append the list to the final list 
        userLikedBooksList.append(tempListUser) 
  


#filtering keywords from the user liked books
    bookDBKeywordFilt = bookDF[bookDF.index.isin(userLikedBooksList)]

    for x in range(0,len(bookDBKeywordFilt.index)-1):
        if x == 0: userString = bookDBKeywordFilt.iloc[0][0]  
        if x < len(bookDBKeywordFilt.index)-1:
            userString = userString + bookDBKeywordFilt.iloc[x+1][0]
         
    userString = ' '.join(unique_list(userString.split()))

    bookDF.loc[userName] = [userString]

# instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(bookDF['bag_of_words'])
    indices = pd.Series(bookDF.index)
    #indices[:5]

    cosine_sim = cosine_similarity(count_matrix, count_matrix)
#recommendation function
    recommended_books = []
    
    # gettin the index of the movie that matches the title
    idx = indices[indices == userName].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar movies
   # top_10_indexes = list(score_series.iloc[1:11+len(userLikedBooksList)].index)
    top_indexes = list(score_series.iloc[1:len(score_series)].index)
   
    # populating the list with the titles of the best 10 matching movies
    for i in top_indexes:
        recommended_books.append(list(bookDF.index)[i])
  
    recommended_books_noUser = [e for e in recommended_books if e  not in userLikedBooksList ]
    
    # getting the genres of all the books
    genreRecommedBooks = []
    coverURLRecBook = []
    tempGenre = []
    tempBookCover = []
    for i in range(0,len(recommended_books_noUser)):
        tempGenre = bookDFComplete.genreVector.loc[bookDFComplete['Book'] == recommended_books_noUser[i]].values[0]
        tempBookCover = bookDFComplete.bookcoverURL.loc[bookDFComplete['Book'] == recommended_books_noUser[i]].values[0]
        coverURLRecBook.append(tempBookCover)
        genreRecommedBooks.append(tempGenre) 
    #for i in top_10_indexes:
     #   recommended_books.append(list(bookDF.index)[i])
        
     # creating new recommeded data frame which has book titles and genres
     
    recommendedDataFrame = pd.DataFrame(
    {'Book': recommended_books_noUser,
     'Genre': genreRecommedBooks,
     'CoverUrl':coverURLRecBook
    })
    
       # Anger : mystery, Humor
    #Joy: Romance, Sci-fi
    #Sadness: Adventure, Humor
    #Fear: Adventure, Sci-fi
    #Disgust: Humor, Romance
    
    if emotion == "Anger":
                            recommendedGenre1DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Mystery"]
                            recommendedGenre2DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Humor"]
    if emotion == "Joy":
                            recommendedGenre1DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Romance"]
                            recommendedGenre2DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Science Fiction"]
                
    if emotion == "Sadness":
                            recommendedGenre1DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Adventure"]
                            recommendedGenre2DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Humor"]
    
    if emotion == "Fear":
                            recommendedGenre1DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Adventure"]
                            recommendedGenre2DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Science Fiction"]
                  
    if emotion == "Disgust":
                            recommendedGenre1DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Humor"]
                            recommendedGenre2DF = recommendedDataFrame.loc[recommendedDataFrame['Genre']== "Romance"]
    
    final_output_dataframe = recommendedGenre1DF.head(2).append(recommendedGenre2DF.head(1))
    final_output_dataframeDict = final_output_dataframe.to_dict()
         
    return json.dumps(final_output_dataframeDict)
    
    

    
#function test
recommendations("user_3","Joy")  
    
    
    
    
    
    
    
    
    
    
    
  



