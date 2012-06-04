JSTwitterBot v0.1
============

(For educational purposes only) Easy to use twitter bot that uses the stream API to search for tweets that contain certain word(s) and replies to them.
It autoregulates itself so it doesn't exceed the limit of tweets per hour.

##How to use:
- Fill in the parameters:

```python
consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""

twitter_account_username = ""
twitter_account_password = ""
```

- Specify what tweets you want to filter (searching for a particular keyword)

```python
query = ['search'] # words to search
```

- Customize what you want to reply to those tweets:

```python
reply = "@" + username + " I'm replying to your tweet with a bot!"
```

- **Run locally**:

```bash
python js_twitter_bot.py
```

- Or **deploy to Heroku** and run it as a worker (Procfile included)