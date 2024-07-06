from flask import request, Response, jsonify
from flask_restful import Resource
from database.models import *
from database.models import Menu, User, Admin, PaymentStatus, Profile , InvoiceDetails
from mongoengine.queryset.visitor import Q
import json

class PollDataGetInfo(Resource):
    def get(self, food):
        product = Menu.objects.get(food=food).to_json()
        return Response(product, mimetype="application/json", status=200)

    def put(self, food):
        print(food)
        body = request.get_json()
        Poll.objects.get(food1=food).update(**body)
        return {'id': str(food)}, 300
class PollData(Resource):
    def get(self):
        product = Poll.objects().to_json()
        # print(product)
        return Response(product, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        attend = Poll(food1=body["food1"], food2=body["food2"],count1=body["count1"], count2=body["count2"]
                           ).save()
        return {'id':str(attend.id)}, 200

    def put(self):
        body = request.get_json()
        Poll.objects().update(**body)
        return {'id':"Successfull"}, 200


class DisplayMenu(Resource):
    def get(self):
        menu = Menu.objects().to_json()
        print(menu)
        return Response(menu, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        menu = Menu(
            day=body["day"], lunch=body["lunch"], lunchPrice=body["lunchPrice"], dinner=body["dinner"], dinnerPrice=body["dinnerPrice"],dinnerPic=body["dinnerPic"],lunchPic=["dinnerPic"]).save()
        id = menu.id

        return {'id': str(id)}, 200

    def put(self):
        body = request.get_json()
        menu = Menu(
            day=body["day"], lunch=body["lunch"], lunchPrice=body["lunchPrice"], dinner=body["dinner"], dinnerPrice=body["dinnerPrice"]).save()
        id = menu.id

        return {'id': str(id)}, 200


class menuUpdateApi(Resource):
    def get(self, day):
        product = Menu.objects.get(day=day).to_json()
        return Response(product, mimetype="application/json", status=200)

    def put(self, day):
        try:
            body = request.get_json()
            print(body)
            print(body["lunchPic"])
            Menu.objects.get(day=day).update(**body)
            print(body)
            return {'id': str(day)}, 200
        except:
            return jsonify("Error updating menu")


class AttendenceRes(Resource):
    def get(self):
            menu = Attendence.objects().to_json()
            print(menu)
            return Response(menu, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        print("I am in Post request Please")
        attend = Attendence(Date=body["Date"], LunchPrice=body["LunchPrice"], DinnerPrice=body["DinnerPrice"],
                            DinnerList=body["DinnerList"], LunchList=body["LunchList"]).save()
        return {'id':str(attend.id)}, 200



class AttendenceReservation(Resource):
    def get(self, date, type):
        reservation = list(Attendence.objects.get(Date=date).to_json())
        # print(reservation)
        return Response(reservation, mimetype="application/json", status=200)

    def put(self, date, type):
        body = request.get_json()
        # print(body)
        # print(date)
        shouldPost=True
        try:
            # print("bila");
            res = Attendence.objects.get(Date=date)
            # print("bila");
            if res:
                shouldPost=False
                reservation = Attendence.objects.get(Date=date).to_json()
                reservation = json.loads(reservation)
                # print(type)
                if type == "lunch":
                    resCount=reservation["LunchList"].count((body["LunchList"])[0])
                    if resCount<2:
                        reservation["LunchList"].append((body["LunchList"])[0])
                        response = {"Date": body["Date"], "LunchPrice": body["LunchPrice"],
                        "DinnerPrice": body["DinnerPrice"], "LunchList": reservation["LunchList"],
                        "DinnerList": reservation["DinnerList"]}
                        # print(reservation["LunchList"])
                        jsonify(response)
                        att=Attendence.objects.get(Date=date).update(**response)
                        # UpdateInvoiceDetails.put(self, (body["LunchList"])[0])
                        # print(response)
                    else:
                        return {"error":"Maximum reservation reached!"},399

                else:
                    resCount=reservation["DinnerList"].count((body["DinnerList"])[0])
                    if resCount<2:
                        reservation["DinnerList"].append((body["DinnerList"])[0])
                        response = {"Date": body["Date"], "LunchPrice": body["LunchPrice"],
                        "DinnerPrice": body["DinnerPrice"], "LunchList": reservation["LunchList"],
                         "DinnerList": reservation["DinnerList"]}
                        # print(reservation["DinnerList"])
                        jsonify(response)
                        att=Attendence.objects.get(Date=date).update(**response)
                    else:
                        return {"error":"Maximum reservation reached!"},400

            # id = att.id
        except:
            if shouldPost:
                AttendenceRes.post(self);
            else:
                print("attendence not reserved!exception!")
                return {'error': "attendence not reserved!exception!"}, 400


class UserApiByEmail(Resource):
    def delete(self, email):
        User.objects.get(email=email).delete()
    
    def get(self, email):
        try:
            usr =  User.objects.get(email=email).to_json()
            return Response(usr, mimetype="application/json", status=200)
        except Exception as e:
            print("here")
            message = {
                "status code": 404,
                "message": str(e)
            }

            resp = jsonify(message)
            resp.status_code = 404
            return resp
    def put(self, email):
        body = request.get_json()
        try:
            res = User.objects.get(email=email).update(**body)
            return jsonify("Successfully Updated")
        except User.DoesNotExist:
            return jsonify("Error")


class adminApi(Resource):
    def get(self):
        try:
            usr = Admin.objects().to_json()
            return Response(usr, mimetype="application/json", status=200)
        except:
            return {"error": "admin doesn't exists"}, 404

    def post(self):
        body = request.get_json()
        try:
            res = Admin.objects.get(email=body["email"]).to_json()
            if res:
                return {"error": "admin already exists"}, 404
        except Admin.DoesNotExist:
            user1 = Admin(email=body["email"]).save()
            id = user1.id
            return {'id': str(id)}, 200


class UserApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            res = User.objects.get(email=body["email"]).to_json()
            if res:
                return {"error": "User already exists"}, 404
        except User.DoesNotExist:
            user1 = User(fullName=body["fullName"], email=body["email"],
                         password=body["password"], phone=body["phone"], cnic=body["cnic"], paymentStatus=body['paymentStatus'], gender=body['gender'], bio=body['bio']).save()
            id = user1.id
            return {'id': str(id)}, 200

    def get(self):
        usr = User.objects().to_json()
        return Response(usr, mimetype="application/json", status=200)


class UserApiPayment(Resource):
    def put(self, email):
        try:
            body = request.get_json()
            User.objects.get(email=email).update(**body)
            print(body)
            return {'id': str(body)}, 200
        except Exception as e:
            message = {
                "status code": 404,
                "message": str(e)
            }

            resp = jsonify(message)
            resp.status_code = 404
            return resp


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            usr = User.objects.get(email=body.get(
                'email'), password=body.get('password')).to_json()
            return Response(usr, mimetype="application/json", status=200)
        except User.DoesNotExist:
            return {"error": "User dont exists"}, 400


class paymentStatusApi(Resource):
    def get(self):
        usr = PaymentStatus.objects().to_json()
        return Response(usr, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        menu = PaymentStatus(
            email=body["email"], status=body["status"]).save()

        id = menu.id

        return {'id': str(id)}, 200

class BillDetails(Resource):
    def get(self):
        pass

    def post(self):
        body = request.get_json()
        print("I am in Post request Please")
        attend = InvoiceDetails(email=body["email"], billAmount=int(body["billAmount"]), numberOfAttendences=int(body["numberOfAttendences"])).save()
        # print(attend.id)
        return {'id': str(attend.id)}, 200
class UpdateInvoiceDetails(Resource):
    def get(self,email):
        details= InvoiceDetails.objects.get(email=email).to_json()
        # print(reservation)
        return Response(details, mimetype="application/json", status=200)


    def put(self,email):
        body = request.get_json()
        print(body)
        shouldPost=True
        try:
            res = InvoiceDetails.objects.get(email=body["email"])
            if res:
                # print(res)
                shouldPost=False;
                reservation = InvoiceDetails.objects.get(email=email).to_json()
                reservation = json.loads(reservation)
                # print(reservation)
                lastBill=int(reservation["billAmount"])
                lastAttend=int(reservation["numberOfAttendences"])
                lastBill+=int(body["billAmount"])
                # print(body["numOfAttendences"])
                lastAttend+=int(body["numberOfAttendences"])
                print("here")
                response = {"email": email, "billAmount": lastBill,"numberOfAttendences": lastAttend}
                # print(lastAttend)
                # print(lastBill)
                # print(response)
                # print(reservation["LunchList"])
                jsonify(response)
                att=InvoiceDetails.objects.get(email=email).update(**response)
                # else:
                #     return {"error":"Maximum reservation reached!"},399

            # id = att.id
            return {'msg': "success"}, 200
        except:
            # print("getting!")
            if shouldPost:
                BillDetails.post(self);
            else :
                return {'error': "attendence not reserved!exception!"}, 400



class MypaymentStatus(Resource):
    def get(self, email):
        try:
            profile = PaymentStatus.objects(Q(email__icontains=email))
            if not profile or profile == []:
                message = {
                    "status code": 404,
                    "message": "not found"
                }

                resp = jsonify(message)
                resp.status_code = 404
                return resp

            else:
                return jsonify(profile)
                # return Response(profile, mimetype="application/json", status=200)

        except Exception as e:
            message = {
                "status code": 404,
                "message": str(e)
            }

            resp = jsonify(message)
            resp.status_code = 404
            return resp


class ProfileData(Resource):
    def get(self, email):
        try:
            profile = Profile.objects.get(email=email).to_json()

            return Response(profile, mimetype="application/json", status=200)

        except Exception as e:
            message = {
                "status code": 404,
                "message": str(e)
            }

            resp = jsonify(message)
            resp.status_code = 404
            return resp

    def put(self, email):
        try:
            body = request.get_json()
            Profile.objects.get(email=email).update(**body)
            print(body)
            return {'id': str(body)}, 200
        except Exception as e:
            message = {
                "status code": 404,
                "message": str(e)
            }

            resp = jsonify(message)
            resp.status_code = 404
            return resp


class PostProfile(Resource):
    def post(self):
        body = request.get_json()
        # profile = Profile(
        #     email=body["email"], name=body["name"], cnic=body["cnic"], phone=body['phone'], bio=body['bio'], gender=body['gender']).save()
        profile = Profile(
            email=body["email"], name=body["name"], cnic=body["cnic"], phone=body['phone'], bio=body['bio'], gender=body['gender']).save(),

        return {'id': str("Success")}, 200
