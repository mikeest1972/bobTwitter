from os import error
import tweepy
import time
import urllib
class BobTwitterBot():

    def __init__(self):
        self.apiKey = None
        self.apiSecretKey = None
        self.accesToken = None
        self.accesTokenSecret = None
        self.hashTags = []
        self.getKeys()
        self.auth()
        self.loadHashTags()
        #self.user = self.api.me()

    def getKeys(self):
        # gets the keys from the files 
        f = open("apiKey", 'r')
        self.apiKey = f.read()
        f.close()
        f = open("apiSecretKey", 'r')
        self.apiSecretKey = f.read()
        f.close()
        f = open("accessToken",'r')
        self.accesToken = f.read()
        f.close()
        f = open("accessTokenSecret",'r')
        self.accesTokenSecret = f.read()
        f.close()

    def auth(self):
        auth = tweepy.OAuthHandler(self.apiKey, self.apiSecretKey)
        auth.set_access_token(self.accesToken,self.accesTokenSecret)
        self.api = tweepy.API(auth,wait_on_rate_limit=True)#,wait_on_rate_limit_notify=True)
    
    def loadHashTags(self):
        f = open("hashtags.txt", 'r')
        s = f.read()
        self.hashTags = s.split(",")
        
            
        pass
    def findWhatToRetweet(self, hashTag):
        selected = None
        for tweet in tweepy.Cursor(self.api.search_tweets, q=hashTag).items(20):
            if(selected == None):
                selected = tweet
            
            elif(selected.favorite_count < tweet.favorite_count):
                selected = tweet
            #print("Temp fav: " + str(selected.favorite_count))
        #print("Hahstag: " + hashTag)
        #print("Favorite count: " + str(selected.favorite_count))
        print("Should retweet: " + selected.text)
        try:
            self.api.retweet(selected.id)
            self.api.create_favorite(selected.id)
        except Exception as identifier:#tweepy.errors as identifier:
            print(identifier)
            print("Failed will not tweet or like")
        

    def controlFunc(self):
        for hashtag in self.hashTags:
            self.findWhatToRetweet(hashtag)
            #time.sleep(300) # should be 3,000 sec for 5 min


print("Bob twitter bot")

bob = BobTwitterBot()
bob.controlFunc() # tweets everything every time it runs

#bob.findWhatToRetweet("#100DaysOfCode")

