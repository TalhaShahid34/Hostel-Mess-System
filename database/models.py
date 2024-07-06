from .db import db
from mongoengine import ListField


class Menu(db.Document):
    day = db.StringField(required=True)
    lunch = db.StringField(required=True)
    lunchPrice = db.StringField(required=True)
    lunchPic=db.StringField(required=True)
    dinner = db.StringField(required=True)
    dinnerPrice = db.StringField(required=True)
    dinnerPic = db.StringField(required=True)
class Poll(db.Document):
    food1 = db.StringField(required = True)
    food2 = db.StringField(required = True)
    count1 = db.IntField(required = True)
    count2 = db.IntField(required = True)

class User(db.Document):
    fullName = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    phone = db.StringField(required=True)
    cnic = db.StringField(required=True)
    paymentStatus = db.StringField(required=True)
    gender = db.StringField(required=True)
    bio = db.StringField(required=True)


class Attendence (db.Document):
    Date = db.StringField(required=True)
    LunchPrice = db.StringField(required=True)
    LunchList = ListField(db.StringField(), required=False)
    DinnerPrice = db.StringField(required=True)
    DinnerList = ListField(db.StringField(), required=False)


class Admin(db.Document):
    email = db.StringField(required=True)


class PaymentStatus(db.Document):
    email = db.StringField(required=True)
    status = db.StringField(required=True)

class InvoiceDetails(db.Document):
    email = db.StringField(required=True)
    billAmount = db.IntField(required=True)
    numberOfAttendences = db.IntField(required=True)


class Profile(db.Document):
    email = db.StringField(required=True)
    name = db.StringField(required=True)
    cnic = db.StringField(required=True)
    phone = db.StringField(required=True)
    gender = db.StringField(required=True)
    bio = db.StringField(required=True)
