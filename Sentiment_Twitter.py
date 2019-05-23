import re
import tweepy
from textblob import TextBlob

class TweepyExample(object):

    def __init__(self):
        consumer_key = "B4foCJyXABFv01oFjsfDnNTSD"
        consumer_secret_key = "OkXsih9S6eJNBk8IBsnYqMOxzgbEJeWHs70eGla8NkLJlNpPJS"
        access_token = "1923202261-DpJOEEDEQFOyYncqy01skCtv5RQlRuCaMjHL9yz"
        access_token_secret = "uudkilJk3mKg4ZNpXXIVCcYDbJHjuzlGEAXVRz8g3WSgC"

        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print "Authentication Failed."


    def getPersonalDetails(self):
        print "\n" + self.api.me()

    def getUserDetails(self, id):
        print self.api.get_user(id)

    def getHomeTimelineTweets(self):
        timelineTweets = self.api.home_timeline()
        for tweet in timelineTweets:
            print tweet.text

    def getListFriends(self):
        for friend in tweepy.Cursor(self.api.friends).items():
            print friend.name

    def cleanTweet(self, tweet):
        return ''.join(re.sub("(@[A-Za-z0-9]+)|(^0-9A-Za-z \t)|(\w+:\/\/\S+)", " ", tweet).split())

    def getTweetSentiment(self, tweet):
        analysis = TextBlob(self.cleanTweet(tweet))
        if analysis.sentiment.polarity > 0:
            print "positive " + str(analysis.sentiment.polarity)
        elif analysis.sentiment.polarity < 0:
            print "negative " + str(analysis.sentiment.polarity)
        else:
            print "neutral"

    def getTweets(self, query, limit = 5):
        tweets= []
        try:
            fetchedTweets = self.api.search(q=query, count=limit)
            for tweet in fetchedTweets:
                parsedTweet = {}
                parsedTweet['text'] = tweet.text
                parsedTweet['sentiment'] = self.getTweetSentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsedTweet not in tweets:
                        tweets.append(parsedTweet)
                else:
                    tweets.append(parsedTweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error: " + str(e))


def main():
    api = TweepyExample()
    query = raw_input("Enter query to search tweets:")
    api.getTweets(query, 10)


if __name__ == "__main__":
    main()










# reference: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/


# query = raw_input("Enter query to search tweets:")
# fetched_tweets = api.search(query,count= 20, lang="en")
# fetched_tweets = ["I'm bad", "I liked it very much!", "It was worse.", "I didn't liked it though!"]
# for tweet in fetched_tweets:
#     print "\n" + tweet
#     analysis = TextBlob(tweet)
#     if analysis.sentiment.polarity > 0:
#         print "positive " + str(analysis.sentiment.polarity)
#     elif analysis.sentiment.polarity < 0:
#         print "negative " + str(analysis.sentiment.polarity)
#     else:
#         print "neutral"