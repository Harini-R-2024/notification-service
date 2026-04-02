import time
import random
from app.workers.queue import notification_queue, counter


def process_notifications():
    while True:
        if not notification_queue.empty():
            priority, _, data = notification_queue.get()

            retry_count = data.get("retry_count", 0)

            print(f"Processing notification: {data}")

            # simulate random failure
            success = random.choice([True, False])

            if success:
                print(f"✅ Notification sent: {data}")
            else:
                print(f"❌ Failed to send: {data}")

                if retry_count < 3:
                    retry_count += 1

                    # exponential backoff
                    delay = 2 ** retry_count
                    print(f"Retrying in {delay} seconds... (attempt {retry_count})")

                    time.sleep(delay)

                    # re-add to queue
                    data["retry_count"] = retry_count
                    notification_queue.put((priority, next(counter), data))
                else:
                    print(f"🚫 Max retries reached: {data}")

        time.sleep(1)