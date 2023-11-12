from mongoengine import connect, Document, StringField, BooleanField

connect(db="web16_hw88", host="mongodb+srv://artemF_web16:wubmyw-bysroK-0fuwnu@cluster0.94vozhi.mongodb.net/?retryWrites=true&w=majority")


class User(Document):
    fullname = StringField(max_length=100, required=True, unique=True)
    email = StringField(max_length=50)
    phone_number = StringField(max_length=30)
    priority = StringField(max_length=10)
    is_send = BooleanField(default=False)
