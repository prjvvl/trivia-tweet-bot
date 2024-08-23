import html
import os
import random
import requests
import tweepy

def tweet():
    # Fetch environment variables
    X_CONSUMER_KEY = os.environ.get('X_CONSUMER_KEY')
    X_CONSUMER_SECRET = os.environ.get('X_CONSUMER_SECRET')
    X_ACCESS_TOKEN = os.environ.get('X_ACCESS_TOKEN')
    X_ACCESS_TOKEN_SECRET = os.environ.get('X_ACCESS_TOKEN_SECRET')

    # Check if all environment variables are set
    if not all([X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
        print("Please set the environment variables X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET")
        return

    # Initialize Twitter client
    client = tweepy.Client(
        consumer_key=X_CONSUMER_KEY,
        consumer_secret=X_CONSUMER_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET
    )

    # Fetch trivia question
    try:
        response = requests.get('https://opentdb.com/api.php?amount=10')
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()
        results = response_json.get('results', [])

        targets = ["General Knowledge", "Science & Nature", "Science: Mathematics", "History", "Politics", "Geography", "Science: Gadgets"]
        results = [item for item in results if html.unescape(item["category"]) in targets]
        
        if results:
            result = results[0]
            tag = html.unescape(result['category']).replace(":", "").replace(" ", "").replace("&", "")
            question = html.unescape(result['question'])
            
            answers = result['incorrect_answers']
            answers.append(result['correct_answer'])
            answers = [html.unescape(answer) for answer in answers]
            random.shuffle(answers)
            
            text = f"#{tag}\n{question}"
            client.create_tweet(text=text, poll_duration_minutes=1440, poll_options=answers)
        else:
            print("No valid result found from the trivia API.")

    except requests.RequestException as e:
        print(f"Error fetching trivia question: {e}")
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")

if __name__ == "__main__":
    tweet()