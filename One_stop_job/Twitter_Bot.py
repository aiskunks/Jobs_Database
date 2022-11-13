from venv import create
import tweepy
import csv
import MySQLdb
import requests

api_key = "mxbTZJsWiAqO8whGK99QMxn8t"
api_key_secret = "EaqMa00oKmNEniD5RAfnVWN7rqW9bE6pU2RbgqnRamgtiD9KZ2"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAD6liQEAAAAAE5nJkaSWrwIl%2By9Bsc41Xsx338k%3D1hl6eawGWpIppLmAQ35qbP6VqJWBB4b9VndQ80ajiHzqxhC9CK"
access_token = "2915508242-hROMHfa8X6OAGCZU6GT3ab4TEYqg0dAdYSkwIIm"
access_token_secret = "eM7cuQo6n2JtY15FptJ0zl9bhsW3EAiVvdtH6YCsm6e2P"
client_id = "NG1BWGJsRmwtdHhjb3hqQ1UxVEk6MTpjaQ"
client_secret = "KuklliQ6BUNhiYMbudptk_Pt_PQ2WLi9lRJgCKLifUgU9ZlBcd"
mydb = MySQLdb.connect(host="127.0.0.1", user="root", password="Vigilant@22", database="twitter_schema")
mycursor = mydb.cursor()
authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticator, wait_on_rate_limit=False)
client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret, return_type = requests.Response, wait_on_rate_limit=False)                

osj_users = []
osj_users.append(["SinchanaKumara", "Abcd1234", "seeker"])
osj_users.append(["namithajc27", "HIK1234", "seeker"])
osj_users.append(["Maheswarasairam", "KILE", "admin"])

user_insert_query = 'insert ignore into `osj_account` (`twitter_handle`, `password`, `role`) values (%s, %s, %s)'
mycursor.executemany(user_insert_query, osj_users)
mydb.commit()

mycursor.execute("Select twitter_handle FROM osj_account where role='seeker'")
myresult = mycursor.fetchall()
user_info = []
for x in myresult:
  user = api.get_user(screen_name=x[0])
  user_info.append([user.screen_name, user.id_str, user.name, user.description, user.location, user.created_at])

user_info_insert_query = 'insert ignore into `osj_users` (`twitter_handle`, `user_id`, `screen_name`, `description`, `location`, `joined_date`) values (%s, %s, %s, %s, %s, %s)'
mycursor.executemany(user_info_insert_query, user_info)
mydb.commit()

hashtags = ["#databaseJobs", "#paidinternships", "#highestpaidjobs", "#bakingjobs"]
# excess = ["#cloudjobs","#microsoft", "#google", "#mncjobs", "#metajobs", "#applejobs", "#teslajobs", "fooddeliveryjobs", "#financialjobs", "#fortune500jobs", "#productmanagerjobs", "#publicsectorbanks", "#bankingjobs", "#financecompanyjobs"]
job_tweets = []
job_urls = []
job_tags = []
for hashtag in hashtags:
    for tweet in tweepy.Cursor(api.search_tweets,q=hashtag,count=5, #The q variable holds the hashtag 
                           lang="en").items():
                           print(tweet)
                           media = tweet.entities.get('media', [])
                           media = tweet.entities.get('media')
                           job_tweets.append([tweet.id_str,tweet.author.screen_name, tweet.text.encode("utf-8"), tweet.created_at, tweet.author.profile_image_url, tweet.author.location])
                           job_tags.append([tweet.id_str, hashtag])
                           if(tweet.entities.get('urls',[])) :
                            job_urls.append([tweet.id_str, tweet.entities.get('urls')[0]['expanded_url']])
                           else:
                            job_urls.append([tweet.id_str, None])

jobs_tweet_query  = 'insert ignore into `tweets_table` (`tweet_id`, `recruiter_twitter_handle`, `tweet_text`, `tweet_date`, `profile_image_url`, `recruiter_tweet_location`) values (%s, %s, %s, %s, %s, %s)'
jobs_urls_query = 'insert ignore into `job_urls` (`tweet_id`, `job_url`) values (%s, %s)'
job_tags_query = 'insert ignore into `tweet_tags` (`tweet_id`, `tags`) values (%s, %s)'
mycursor.executemany(jobs_tweet_query, job_tweets)
mydb.commit()
mycursor.executemany(jobs_urls_query, job_urls)
mydb.commit()
mycursor.executemany(job_tags_query, job_tags)
mydb.commit()

mycursor.execute("Select user_id, twitter_handle FROM osj_users")
myresult = mycursor.fetchall()
user_saved_application = []
for x in myresult:
    saved_tweets = client.get_liked_tweets(x[0], max_results = 10, media_fields=None, pagination_token=None, place_fields=None, poll_fields=None, tweet_fields=["attachments","author_id","created_at"], 
    user_fields=None, user_auth=False).json()
    if(saved_tweets.get('data',[])) :
        for tweet in saved_tweets['data']:
            user_saved_application.append([tweet['id'], tweet['author_id'], x[1], tweet['created_at']])

user_saved_application_query = 'insert ignore into `my_saved_applications` (`job_tweet_id`, `recruiter_twitter_handle`, `user_handle`, `post_date`) values (%s, %s, %s, %s)'
mycursor.executemany(user_saved_application_query, user_saved_application)
mydb.commit()


mycursor.execute("Select twitter_handle FROM osj_users")
myresult = mycursor.fetchall()
applied_tweets_list = []
for x in myresult:
    applied_tweets = api.user_timeline(screen_name=x[0])
    for tweet in applied_tweets:
        applied_tweets_list.append([tweet.id, tweet.entities.get('urls')[0]['expanded_url'], tweet.user.screen_name, tweet.created_at])

# print(applied_tweets_list)
applied_jobs_query = 'insert ignore into `jobs_applied` (`application_tweet_id`, `job_url`, `user_twitter_handle`, `applied_tweet_date`) values (%s, %s, %s, %s)'
mycursor.executemany(applied_jobs_query, applied_tweets_list)
mydb.commit()



