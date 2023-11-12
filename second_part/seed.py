import random

from models import User
from faker import Faker

fake = Faker()


def seed(count=0):
    if count == 0:
        return None
    for el in range(count):
        try:
            user = User(fullname=fake.name(), email=fake.email(),
                        phone_number=fake.phone_number(), priority=random.choice(["email", "sms"]))
            user.save()
        except Exception as e:
            print(e)
