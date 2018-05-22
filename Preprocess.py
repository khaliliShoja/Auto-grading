# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import re
import numpy as np
import scipy as sp
from textblob import TextBlob
from textblob import Word
import language_check
import enchant

class PreprocessData:
    def  __init__ (self):
        pass
    
    def processData_(self, row):
        analyser=[]
        ess = TextBlob(row['essay'])
        
        words_list = ess.words
        sentences_list = ess.sentences
        
        #Number of words in each essay
        analyser.append(len(words_list))
        
        
        #Number of sentences in each essay
        analyser.append(len(sentences_list))
        
        #Average lenght of sentences in each essay
        sum_ = 0
        for i in sentences_list:
            #Catch each sentence
            sen_ = i.split(' ')
            sen_len = len(sen_)
            sum_ = sum_ + sen_len
        analyser.append(sum_/len(sentences_list))
        
        # Number of words larger than 7 char
        sum_ = 0
        for i in words_list:
            if (len(i) >= 7):
                sum_ = sum_ +1
        analyser.append(sum_)
        
        # Essay sentiment
        analyser.append(ess.sentiment.polarity)
        
            
        
        # POS counting 
        countNoun = 0
        countVerb = 0
        countAdverb = 0
        countAdjective = 0
        for i in ess.tags:
            if(i[1][0].lower() == 'n'):
                countNoun = countNoun +1
            elif(i[1][0].lower() == 'v'):
                countVerb = countVerb +1        
            elif(i[1][0].lower() == 'r'):
                countAdverb = countAdverb +1   
            elif(i[1][0].lower() == 'j'):
                countAdjective = countAdjective +1   
        
        analyser.append(countNoun)
        analyser.append(countVerb)
        analyser.append(countAdverb)
        analyser.append(countAdjective)
        
        
        
        tool = language_check.LanguageTool('en-US')
        matches = tool.check(str(ess))
        analyser.append(len(matches))
        
        a = row['essay']
        clean_essay = re.sub('@[a-z A-Z 0-9]+', ' ', a)
        

        #Spell mistakes after removing @WORDs
        d = enchant.Dict('en_US')
        ess = TextBlob(clean_essay)
        words_list = ess.words
        sum_ = 0
        for i in words_list: 
            if(d.check(str(i)) == False):
                sum_ = sum_ + 1
        analyser.append(sum_)
        
        
        
        return pd.Series(analyser)
        
    
        
    
    
    def processData(self, df):
        df [['*_# of words_*' , '*_# of sentences_*',
            '*_Average lenght of sentences_*' , '*_# of large words_*', '*_Sentiment_Polarity_*',
            '*_# of Nouns_*', '*_# of Verbs_*', '*_# of Adverbs_*', '*_# of Adjectives_*',
            '*_# of grammer mistakes_*', '*_# of spelling mistakes*']] =df.apply(self.processData_, axis = 1)
