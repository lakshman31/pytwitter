#these lib are required to execute this pls install textblob,tweepy,sqlite,matplotlib,wordcloud
from textblob import TextBlob
import tweepy
import sqlite3
from matplotlib import pyplot as plt
from wordcloud import WordCloud,STOPWORDS
#setting up sql
conn=sqlite3.connect('twitter')
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS twitter(comment TEXT)''')
conn.commit()
#authenication info
consumer_key= "rX4k9Uw579E5UKm8O02x89TRE"
consumer_secret= "GLiK8lSLvGmdHjcgGNU7vjVIjLbWqhXfxYb4E4FxJ4LPNxAHre"
#access token info
token_key= "2993560776-atXto2CzzJaET6LLt8GL7USTkOGK0rJHJSqqioO"
token_secret= "rAST7FhNjmD3tIW9hAM6YCnHz063AaKmrpye38W8j0Wdu"
#authenticating
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(token_key,token_secret)
api=tweepy.API(auth)
#recieving the inputs from the user
dat=input('enter the key to be searched')
comment_words=' '
stopwords=set(STOPWORDS)
p_tweets=api.search(dat)

tot=0
pos=0
neg=0
neu=0
tweet1=[]
for tweet in p_tweets:
    if tweet not in tweet1:
        tweet1.append(tweet.text)
        cur.execute('''INSERT INTO twitter VALUES(?)''',(tweet.text,))
        conn.commit()   
        analysis=TextBlob(tweet.text)
        if analysis.sentiment.polarity>0:
            print('positive')
            pos+=1
            tot+=1

        elif analysis.sentiment.polarity<0:
            print('negetive')
            neg+=1
            tot+=1 
        else:
            print('neutral')
            neu+=1
            tot+=1   
cur.close
print(pos)
print(neg)
print(neu)
print(tot)  
#calc the percentage
pos_per=(pos/tot)*100
neg_per=(neg/tot)*100
neu_per=(neu/tot)*100
x=[1,2,3]
y=[int(pos_per),int(neg_per),int(neu_per)]
tick_label=['pos','neg','neu']
# plotting a bar chart
plt.bar(x, y, tick_label = tick_label,width = 0.8, color = ['green', 'red','yellow'])

# naming the x-axis
plt.xlabel('sentiment')
# naming the y-axis
plt.ylabel('percentage')
plt.show()
# CREATING WORDCLOUD
for val in tweet1:
    comment_words=str(val)
wordcloud = WordCloud(width = 500, height = 500,background_color ='white',stopwords = stopwords,min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                       
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()
    
       
    



