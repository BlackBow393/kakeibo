import os

# スクリプトと同じフォルダにサービスアカウントJSONがある場合に環境変数を設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), "turing-energy-462700-m1-ac7f44dbd376.json")

from google.cloud import pubsub_v1

PROJECT_ID = "turing-energy-462700-m1"
SUBSCRIPTION_ID = "t93_gmail_push_topic-sub"

def callback(message):
    print("📩 Pub/Sub 通知を受信:", message.data.decode("utf-8"))
    message.ack()

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

print(f"✅ {subscription_path} を監視中...")
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
streaming_pull_future.result()
