import tweepy
import discord
from discord.ext import commands
from collections import defaultdict

# Twitter API credentials
TWITTER_API_KEY = 'your_twitter_api_key'
TWITTER_API_SECRET = 'your_twitter_api_secret'
TWITTER_ACCESS_TOKEN = 'your_twitter_access_token'
TWITTER_ACCESS_TOKEN_SECRET = 'your_twitter_access_token_secret'

# Discord bot credentials
DISCORD_TOKEN = 'your_discord_bot_token'
DISCORD_CHANNEL_ID = 1234567890  # Replace with your Discord channel ID

# Coin tags to track
COIN_TAGS = ['#bitcoin', '#ethereum', '#dogecoin']  # Add more as needed

# Twitter authentication
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth, wait_on_rate_limit=True)

# Discord bot setup
bot = commands.Bot(command_prefix='!')

# Dictionary to store aggregated data
coin_data = defaultdict(lambda: {'likes': 0, 'retweets': 0, 'quotes': 0})

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='update')
async def update_data(ctx):
    for coin_tag in COIN_TAGS:
        tweets = tweepy.Cursor(twitter_api.search, q=coin_tag, lang='en', tweet_mode='extended').items(100)
        
        for tweet in tweets:
            coin_data[coin_tag]['likes'] += tweet.favorite_count
            coin_data[coin_tag]['retweets'] += tweet.retweet_count
            coin_data[coin_tag]['quotes'] += tweet.quote_count

    # Sort coins based on total engagement
    sorted_coins = sorted(coin_data.items(), key=lambda x: x[1]['likes'] + x[1]['retweets'] + x[1]['quotes'], reverse=True)

    # Create and send a Discord message with the rankings
    message = "Coin Rankings:\n"
    for i, (coin_tag, data) in enumerate(sorted_coins, start=1):
        message += f"{i}. {coin_tag}\n  Likes: {data['likes']} | Retweets: {data['retweets']} | Quotes: {data['quotes']}\n"

    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    await channel.send(message)

# Run the bot
bot.run(DISCORD_TOKEN)
