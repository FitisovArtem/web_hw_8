import json
import sys
from time import sleep

import pika

from second_part.models import User

queue_name = 'email'


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode('utf-8'))
        print(f"Отримав таску {method.delivery_tag}. Відправляю email для: {message.get('fullname')}")
        sleep(0.1)
        print("Помічаю в БД як виконано")
        mark_result = mark_data(message.get('_id'))
        if mark_result:
            print("Виконано!")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def mark_data(user_id):
    try:
        user = User.objects(id=user_id.get('$oid'))
        user.update(is_send=True)
        return True
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
