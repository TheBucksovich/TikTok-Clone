from celery import Celery
import time
import pika

def wait_for_rabbitmq(host="localhost", retries=20, delay=3):
    for attempt in range(retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host)
            )
            connection.close()
            return
        except Exception:
            if attempt == retries - 1:
                raise RuntimeError("RabbitMQ не запустился после максимального числа попыток")
            time.sleep(delay)

wait_for_rabbitmq()

celery_app = Celery(
    "tasks",
    broker="pyamqp://guest@localhost//",
    backend="rpc://",
)

celery_app.conf.update(
    task_routes={"tik_tok.tasks.video_tasks.*": {"queue": "video_queue"}},
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
)
