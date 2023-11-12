from bson import json_util
import pika
import models
from seed import seed

COUNT_USERS = 100
EXCHANGE_NAME = "WEB16"
QUEUE_LIST = ['email', 'sms']


def create_model():
    try:
        models
        return True
    except Exception as e:
        print(e)
        return False


def seeding_data():
    try:
        seed(COUNT_USERS)
        return True
    except Exception as e:
        print(e)
        return False


def get_data(data_object):
    for el in data_object:
        tr = el.to_mongo().to_dict()
        print(tr.get["priority"])


def send_data_to_queue():
    count_phone = 0
    count_email = 0

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
    for item in QUEUE_LIST:
        channel.queue_declare(queue=item)
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=item)

    for el in models.User.objects():
        data = el.to_mongo().to_dict()
        message = json_util.dumps(data).encode('utf-8')
        prior = data.get("priority")
        if prior == "email":
            count_email += 1
        else:
            count_phone += 1
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=prior, body=message)
    connection.close()
    return f"До біржі {EXCHANGE_NAME} відправлено {COUNT_USERS} повідомлень: {count_email} - email, {count_phone} - sms"


def main():

    print("Створюємо Моделі...")
    cm = create_model()
    if cm:
        print(f"Наповнюємо даними кількістю: {COUNT_USERS} шт.")
        sd = seeding_data()
        if sd:
            send = send_data_to_queue()
            return send
