from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

scope = ["https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("cred.json",scope)

gc = gspread.authorize(credentials)

# Credentials twitter
consumer_key = 'K4qODxM5WgxksSxEFSxocDcOO'
consumer_secret = 'LqKknbzirDRjTT8n1FOMDu9z67oT0u58ETHJAtCXiubCV0oQ0i'
access_token = '931857533056172032-2GUzUXYZlI8VniuAKKLsEHs6ramWxqQ'
access_secret = 'y6Zqjlds7EYnIaFfGJK6lmMzHU34Pjua3ijpbN5uw4YRJ'

class listener(StreamListener):

    def on_data(selfself,data):
        try:

            wks = gc.open("Streaming").sheet1

            jsondata = json.loads(data)

            tweet_id = str(jsondata["id"])

            try:
                tweet = jsondata["extended_tweet"]["full_text"]
            except:
                tweet = jsondata["text"]
            retweet_count = jsondata["retweet_count"]
            favorite_count = jsondata["favorite_count"]
            date = jsondata["created_at"]
            source = jsondata["source"].split(">")[1].split("<")[0]

            location = jsondata["user"]["location"]
            user_screename = jsondata["user"]["screen_name"]

            try:
                hashtag = jsondata["entities"]["hashtags"][0]["text"]
            except:
                hashtag = "-"
            try:
                mention_screen = jsondata["entities"]["user_mentions"][0]["screen_name"]
            except:
                mention_screen = "-"




            # print tweet
            # print retweet_count
            # print favorite_count
            # print date
            # print source
            # print hashtag
            # print mention_screen
            # print location
            # print user_screename
            wks.append_row([tweet, retweet_count, favorite_count,date, source, hashtag, mention_screen, location, user_screename,tweet_id])



            return True
        except BaseException, e:
            print "failed on data", str(e)
            time.sleep(15)

    def on_error(self,status):
        print status



auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
#
twitterStream = Stream(auth,listener())

# word = raw_input("What do you want to track ? (Separate words by comma)\n").split(",")

# print word

twitterStream.filter(track=["Narendra Modi"])



