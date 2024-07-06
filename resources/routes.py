from .resources import *


def initialize_routes(api):
    api.add_resource(DisplayMenu, "/api/menu/")
    api.add_resource(menuUpdateApi, "/api/updateMenu/<day>")
    api.add_resource(AttendenceReservation, "/api/attendence/<date>/<type>")
    api.add_resource(AttendenceRes, "/api/attendenced")
    api.add_resource(BillDetails, "/api/bill")
    api.add_resource(UpdateInvoiceDetails, "/api/updateBill/<email>")
    api.add_resource(UserApi,"/api/User")
    api.add_resource(UserApiByEmail,"/api/User/<email>")
    api.add_resource(UserApiPayment,"/api/Users/<email>")
    api.add_resource(adminApi,"/api/admin")
    api.add_resource(LoginApi, '/api/Login')
    api.add_resource(paymentStatusApi, "/api/status/")
    api.add_resource(MypaymentStatus, "/api/payStatus/<email>")
    api.add_resource(ProfileData, "/api/profile/<email>")
    api.add_resource(PostProfile, "/api/postProfile/")
    api.add_resource(PollData, "/api/pollData/")
    api.add_resource(PollDataGetInfo, "/api/pollDataInfo/<food>")
    