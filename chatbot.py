
#Meet Robo: your friend

#import necessary libraries
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only


#Reading in the corpus
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "yo", "what's up","hey", "konnichiwa", "ohayo", "konbanwa")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me", "konbanwa", "ohayo"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)



# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"Semimasen! Wakarimasen"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
print("ALICE: Konnichiwa, Enigumabotto e y??koso, Saya akan membantu menjawab pertanyaan mengenai Enigmacamp. Jika ingin keluar, silahkan ketikan Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='ja'):
        if(user_response=='arigato' or user_response=='arigatai' ):
            flag=False
            print("ALICE: Doitashimaste..")
        else:
            if(greeting(user_response)!=None):
                print("ALICE: "+greeting(user_response))
            else:
                print("ALICE: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("ALICE: mata ashitane! gengki ne..")    
        
        

