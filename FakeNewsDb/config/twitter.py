import tweepy


consumer_key = '6U4RQbILxgWSguOlLIFZKPyPV'
consumer_secret = 'Inewccz8TAZSJ3iGj2mUa4S8zd2mjnIBxBsA5mS7Mv2tGgLd6f'
access_token = '2828790701-zDI3WX7Nr56NZiAmmBrTmADPjQOZZbZtCNLgmxp'
access_token_secret = 'd1yRuIKqyVwPrXVu4oXYGd1ElDS6DXbCoHR5wR8JlCaGv'
#acces token api level 2
bearertoken='AAAAAAAAAAAAAAAAAAAAACJzlQEAAAAABO1sjsSdy5xz1GgWODzGUTU8b0o%3D3QzjbUOZU7eSBbYfVgfwdiLt9dpR6IwnSmCsogl1qqUntQjap6'

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# Authenticate with the Twitter API level 2
client = tweepy.Client(bearer_token=bearertoken)

