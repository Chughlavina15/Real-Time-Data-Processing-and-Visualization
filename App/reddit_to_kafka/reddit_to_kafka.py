import os
from dotenv import load_dotenv
import praw
from kafka import KafkaProducer
import json

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'], 
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


subreddit_name = "all"  
topic_name = "topic1"    

def fetch_and_send():
    subreddit = reddit.subreddit(subreddit_name)
    for comment in subreddit.stream.comments(skip_existing=True):
        data = {
            "id": comment.id,
            "author": str(comment.author),
            "body": comment.body,
            "created_utc": comment.created_utc,
            "subreddit": comment.subreddit.display_name
        }
        # print(f"Sending comment to Kafka: {data}")  
        producer.send(topic_name, value=data)
        producer.flush() 

if __name__ == "__main__":
    print("Starting to fetch data from Reddit and send to Kafka...")
    try:
        fetch_and_send()
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        producer.close()