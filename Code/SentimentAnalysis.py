import csv
import pymysql
import sys
from happyfuntokenizing import Tokenizer
from os import listdir

def main():
    total_tweets=1578614
    positive_tweets=790178
    negative_tweets=788436
    
    
    positiveProb=(1.00*positive_tweets)/total_tweets
    negativeProb=(1.00*negative_tweets)/total_tweets

    print positiveProb
    print negativeProb
    

    positiveWords_Dictionary=ConvertCSVToDictionary('PositiveWords.csv')    
    negativeWords_Dictionary=ConvertCSVToDictionary('NegativeWords.csv')
    sum_count_pos_words=SumValuesOfDictionary(positiveWords_Dictionary)
    sum_count_neg_words=SumValuesOfDictionary(negativeWords_Dictionary)
    
    allMovieCSV=[]
    filenames = listdir('F:\\\TwitterSentimentAnalysis\\\New folder')
    
    for filename in filenames :
        if filename.endswith('.csv') :
            allMovieCSV.append('F:\\\TwitterSentimentAnalysis\\\New folder\\'+filename)    
    print allMovieCSV
    for movieFile in allMovieCSV:            
        CalculateTweetAnalysis(movieFile,
                               positiveWords_Dictionary,
                               negativeWords_Dictionary,
                               sum_count_pos_words,
                               sum_count_neg_words,
                               positiveProb,
                               negativeProb)
                
  
    
def SumValuesOfDictionary(passedDictionary):
    total=0.0
    for key in passedDictionary:
        total=total+passedDictionary[key]
    return total
def LaplaceSmoothingValue(tweet_word,wordFrequency,count_total_words):
    vocabulary=len(wordFrequency)
    freq_count=0
    if tweet_word in wordFrequency:
        freq_count=wordFrequency[tweet_word]+1
    else:
        freq_count=1
    numerator=freq_count
    denominator=count_total_words+vocabulary
    
    laplaceSmmothin=numerator/denominator
    return laplaceSmmothin
def CalculateTweetAnalysis(movie_tweets_path,
                           positive_words_dict,
                           negative_words_dict,
                           sum_count_pos,
                           sum_count_neg,
                           class_prob_pos,
                           class_prob_neg):
    csv.field_size_limit(sys.maxsize)
    ifile  = open(movie_tweets_path, "rb")
    reader = csv.reader(ifile)
    sentimentList=[]
   
    for row in reader:     
        if(len(row)!=0):
        
            tweet_sentiment=NaiveBesianClassifer(positive_words_dict,
                                 negative_words_dict,
                                 sum_count_pos,
                                 sum_count_neg,
                                 row[0],
                                 class_prob_pos,
                                 class_prob_neg)
            
            sentimentList.append(tweet_sentiment)
    positiveTweets=0.00
    negativeTweets=0.00
    for probValue in sentimentList:
        if(probValue[1]==1):
            positiveTweets=positiveTweets+1
        else:
            negativeTweets=negativeTweets+1
    total=positiveTweets+negativeTweets
    perPos=positiveTweets/total*100
    
    print "positive :"+str(perPos)+" %"+ " :"+ movie_tweets_path
    ifile.close()
        
    
def NaiveBesianClassifer(positive_word_frequency,
                         negative_words_frequency,
                         count_pos_words,
                         count_neg_words,
                         tweet,
                         class_pos_prob,
                         class_neg_prob):
    tok = Tokenizer(preserve_case=False)   
    tokens=tok.tokenize(tweet)
    positiveClassProb=1.00
    negativeClassProb=1.00    
            
    for token in tokens:
        positiveClassProb=positiveClassProb*LaplaceSmoothingValue(token,positive_word_frequency,count_pos_words)
        negativeClassProb=negativeClassProb*LaplaceSmoothingValue(token,negative_words_frequency,count_neg_words)
    positiveClassProb=positiveClassProb*class_pos_prob
    negativeClassProb=negativeClassProb*class_neg_prob            
    
    if(positiveClassProb >=negativeClassProb):
        print positiveClassProb,1
        return positiveClassProb,1
    else:
        print negativeClassProb,1
        return negativeClassProb,-1
  
    
def calcProbabitlities(dictionary_Words,maxValue):
    for key in dictionary_Words:
        count=dictionary_Words[key]
        dictionary_Words[key]=count/maxValue
    return dictionary_Words 
def saveTweeet():
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='test')    
    cur = conn.cursor()
    data =('Thor the great','bad movie','2012-15-09 23:59:59')
    cur.execute("INSERT INTO movie_tweets(movie,TWEET_TEXT,INSERT_DATETIME) VALUES (%s,%s,%s)",data)
    cur.connection.commit()
    cur.close()
    conn.close()
def GetWordDictionary(filePAth):
    csv.field_size_limit(sys.maxsize)
    ifile  = open(filePAth, "rb")
    reader = csv.reader(ifile)
    word_dictionary={}       
    tok = Tokenizer(preserve_case=False)    
    for row in reader:
        tokens=[]
        try:
            tokens=tok.tokenize(row[3])
        except Exception,e:
            print e
        for token in tokens:
            if token in word_dictionary:
                token_count=word_dictionary.get(token)
                token_count=token_count+1
                word_dictionary[token]=token_count
            else:
                word_dictionary[token]=1               
    ifile.close() 
    return word_dictionary
def InsertWordCountCSV(wordDictionary,filename):
    f=open(filename, "wb")
    w = csv.writer(f)
    for key, val in wordDictionary.items():
        w.writerow([key, val])
    f.close()
def ConvertCSVToDictionary(filePAth):
    csv.field_size_limit(sys.maxsize)
    ifile  = open(filePAth, "rb")
    reader = csv.reader(ifile)
    tokens_count={}
    for row in reader:
        tokens_count[row[0]]=float(row[1])
    ifile.close()
    return tokens_count
def ClassWordsCount():
    postiveDictionary=GetWordDictionary('F:\\TwitterSentimentAnalysis\\TwitterData\\PositiveTweets.csv')
    negativeDictionary=GetWordDictionary('F:\\TwitterSentimentAnalysis\\TwitterData\\NegativeTweets.csv')
    InsertWordCountCSV(postiveDictionary,'PositiveWords.csv')
    InsertWordCountCSV(negativeDictionary,'NegativeWords.csv')
    return postiveDictionary,negativeDictionary
if __name__ == '__main__':    
    main()