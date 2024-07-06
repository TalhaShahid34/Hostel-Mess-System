from flask import Flask, jsonify, request, render_template, Response, session, redirect
from flask_restful import Api, Resource
from database import db, models
from database.models import User, Admin
from resources import routes
import stripe
import os
from werkzeug.utils import secure_filename
domain_url = "http://127.0.0.1:5000"

stripe.api_key = "sk_test_51MU9hXEf0VmxjSoD4YQ8vA6JccleWXGcWtdHO4IQIZuStqhwrzXwga4UjLIzgtqDjVQd4pvReJWplzJ4C3uhIkp2002cUXWDZG"

dbUrl='mongodb://localhost:27017/MessSystem'

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': dbUrl
}
app = Flask(__name__, template_folder='templates', static_folder='static')
api = Api(app)
db.initialize_db(app)
routes.initialize_routes(api)
app.secret_key = "Mess_Management"
UPLOAD_FOLDER = "C:\\Users\\HF\\Downloads\\Hostel_Mess-main\\Hostel_Mess-main\\static\\img"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/index')
def home():  # put application's code here
    if session and session["email"]:
        if session["is_admin"]:
            return render_template("/Admin/index.html")
        else:
            return render_template("/Student/index.html", email=session['email'])
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")


@app.route('/settings')
def settings():  # put application's code here
    if session and session["email"] and session["is_admin"]:
        return render_template("/Admin/settings.html")
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")


@app.route('/students')
def students():  # put application's code here
    if session and session["email"] and session["is_admin"]:
        return render_template("/Admin/students.html",email=session["email"])
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")


@app.route('/todayAttendees')
def todayAttendess():  # put application's code here
    if session and session["email"] and session["is_admin"]:
        return render_template("/Admin/todayAttendess.html",email=session['email'])
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")


@app.route('/userManage')
def userManage():  # put application's code here
    if session and session["email"] and session["is_admin"]:
        return render_template("/Admin/userManage.html",email=session["email"])
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")


@app.route('/addNew')
def addNew():  # put application's code here
    if session and session["email"] and session["is_admin"]:
        return render_template("/Admin/addNew.html")
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")

    # return render_template("/Admin/settings.html")


@app.route('/register')
def register():  # put application's code here
    return render_template("register.html")


@app.route('/forget-password')
def forget():  # put application's code here
    return render_template("forget.html")
# @app.route('/register')
# def register():  # put application's code here
#     return render_template("register.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["is_admin"] = False
        email = request.form["email"]
        password = request.form["password"]
        print(email)

        # val = request.form.get("cb1")
        # admin = "talhaadmin@gmail.com"
        if email=="Talhaadmin@gmail.com":
            print("here")
            session["is_admin"] = True
        user = User.objects(email=email).first()
        if not user:
            return render_template("login.html", error="User not found!")
        elif password == user["password"]:
            # if val== "on":
            session["email"] = email
            if session.get("is_admin"):
                return render_template("/Admin/index.html")
            else:
                print(session['email'])

                return render_template("/Student/index.html",email=session["email"])
        else:
            return render_template("login.html", error="Wrong Password!")

    else:

        return render_template("login.html")

@app.route('/dataTable-users')
def dataTableUsers():
    return render_template("/Admin/dataTabelUsers.html")

@app.route('/menu-update', methods=['POST', 'GET'])
def uploadPic():
    if request.method == "GET":
        return render_template("/Admin/menuUpdate.html")
    
    day = request.form['day']
    dinnerImg = request.files['inputFile1']
    lunchImg = request.files['inputFile2']
    dinner = request.form['dinner']
    lunch = request.form['lunch']
    lunchPrice = request.form['lunchPrice']
    dinnerPrice = request.form['dinnerPrice']
    dinnerfileName = secure_filename(dinnerImg.filename)
    lunchfileName = secure_filename(lunchImg.filename)
    
    if dinnerImg and lunchImg:
        dinnerImg.save(os.path.join(app.config['UPLOAD_FOLDER'], dinnerfileName))
        lunchImg.save(os.path.join(app.config['UPLOAD_FOLDER'], lunchfileName))
        
        # Check if menu for the day already exists
        existing_menu = models.Menu.objects(day=day).first()
        
        if existing_menu:
            # Update existing menu
            existing_menu.update(
                day=day,
                lunch=lunch,
                lunchPrice=lunchPrice,
                dinner=dinner,
                dinnerPrice=dinnerPrice,
                lunchPic=lunchImg.filename,
                dinnerPic=dinnerImg.filename
            )
        else:
            # Create new menu entry
            new_menu = models.Menu(
                day=day,
                lunch=lunch,
                lunchPrice=lunchPrice,
                dinner=dinner,
                dinnerPrice=dinnerPrice,
                lunchPic=lunchImg.filename,
                dinnerPic=dinnerImg.filename
            )
            new_menu.save()
        
        return render_template('/Admin/settings.html', success="Menu updated successfully!")

    return render_template('/Admin/settings.html', error="Failed to update menu.")

@app.route('/menu')
def admin_menu():  # put application's code here
    if session and session["email"]:
        if session["is_admin"]:
            return render_template("/Admin/menu.html")
        else:
            return render_template("/Student/menu.html")
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")


# @app.route('/student-menu')
# def student_menu():  # put application's code here
#     return render_template("/Student/menu.html")

@app.route('/menu', methods=['POST'])
def menu_update_post():  # put application's code here
    return render_template("/Admin/settings.html")


@app.route('/payment')
def payment():  # put application's code here
    if session and session["email"] and not session["is_admin"]:
        return render_template("/Student/payment.html")
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")


@app.route('/challan')
def seeInvoice():  # put application's code here
    if session and session["email"] and not session["is_admin"]:
        return render_template("/Student/challan.html",email=session["email"])
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")


@app.route('/analytics')
def analyticsStudent():  # put application's code here
    if session and session["email"] and not session["is_admin"]:
        return render_template("/Student/analytics.html",email=session["email"])
    else:
        return render_template("/login.html", error="Unauthorized access! please login first..")


@app.route('/base')
def homef():  # put application's code here
    print(session["email"])
    return render_template("/Student/base.html",email=session["email"])


@app.route('/pay')
def pay():
    email = session['email']
    try:
        print("here");
        checkout_session = stripe.checkout.Session.create(
           
            success_url=domain_url + "/success",
            cancel_url=domain_url + "/success",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {

                    "quantity": 1,
                    "price": "price_1MYvwuEf0VmxjSoDKuavN3Ov"
                }
            ]

        )
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return jsonify(str(e))


@app.route('/success')
def success():
    email = session['email']
    return render_template('/Student/succes.html', email=email)


@app.route('/profile', methods=['GET', 'POST'])
def homep():  # put application's code here
    email = session['email']
    return render_template("/Student/profile.html", email=email)

@app.route('/profile-admin/<email>')
def adminViewHomep(email):  # put application's code here
    
    return render_template("/Admin/adminSiteProfile.html", email=email)

@app.route('/add-newStudent')
def addNewStudent():
    email = session['email']
    return render_template('/Admin/addNew.html', email=email)


@app.route('/logout')
def logout():  # put application's code here
    print(session)
    session.clear()
    return render_template("/login.html")

@app.route('/poll')
def poll(): 
    return render_template("poll.html")

@app.route('/createPoll')
def createPoll(): 
    return render_template("/Admin/createPoll.html")
   
if __name__ == '__main__':
    app.run(debug=True,port=5000)
