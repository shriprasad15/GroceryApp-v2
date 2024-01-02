from celery.result import AsyncResult
import os
import hashlib
import random
from flask import Flask, render_template,request, make_response, jsonify, send_file
from flask_security import SQLAlchemySessionUserDatastore, Security, login_user, logout_user
from flask_security import current_user, auth_required, login_required, roles_required, roles_accepted,hash_password,verify_password
from flask_cors import CORS
# from pyshortcuts import make_shortcut
from models import *
from apis import *
from config import Config
import time
from cachee import cache
from worker import celery_init_app
from tasks import  engagment
from mail_service import send_email as smail
from tasks import create_resource_csv, monthly_report
from admin_create import admin_create_user
# from tasks import create_resource_csv
# from worker import celery_init_app

app = Flask(__name__)
api.init_app(app)
app.config.from_object(Config)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./model.db"

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", 
                                          "hbivnfdisbvljobfgjoihfhrugubdfsbery89w34yt5898he")
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT",
                                                       "hbivnfdisbvljobfgjoihfhrugubdfsbery89w34yt5898he")

# authenticatin paramter for url
app.config["`SECURITY_TOKEN_AUTHENTICATION_KEY`"] = "auth_key" # Default: auth_token
# in postman add the key as auth_key and value as the token , this should be in the url
app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"] = "Authentication-Token" # Default: Authentication-Token"
# in postman add the key as Authentication-Token and value as the token
# app.config[]

db.init_app(app)

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role) # Not SQLAlchemyUserDatastore
app.security = Security(app, user_datastore)
with app.app_context():
    db.create_all()

    if(db.session.query(Role).count()==0):
        # app.security.datastore.create_role(name="admin")
        # app.security.datastore.create_role(name="user")
        # app.security.datastore.create_role(name="manager")
        db.session.commit()
        admin_create_user()


# @app.route('/monthly-report')
# def monthly_report():
#
#     user_id = 4  # Replace with the desired user ID
#
#
#     report_file = generate_monthly_report(user_id)
#     print(f"Report generated: {report_file}")
#     return {"message": "Report generated successfully!"}

@app.route('/')
def index():
    return "hello"



@app.route('/create-role/<string:role>')
def create_role(role):

    app.security.datastore.create_role(name=role)
    db.session.commit()

    return "Role Created Successfully"


# @app.post('/create-user')
# def create_user():
#     data=request.get_json()
#     # Create and save the user
#     fname = data['fname']
#     lname=data['lname']
#     role = data['roles']
#     mobile=data['mobile']
#     email=data['email']
#     password=data['password']
#     is_auth=data['is_auth']
#     encoded_password = password.encode('utf-8')
#     hashed_password = hashlib.sha256(encoded_password).hexdigest()
#
#     app.security.datastore.create_user(fname=fname, lname=lname, roles=role, mobile=mobile, email=email,
#                                        password=hashed_password, authenticated=is_auth)
#
#     db.session.commit()
#
#     return {"message":"Success"}


@app.post('/create-user')
def create_user():
    data=request.get_json()
    # Create and save the user
    fname = data['fname']
    lname=data['lname']
    role = data['roles']
    mobile=data['mobile']
    email=data['email']
    password=data['password']
    # is_auth=data['is_auth']
    if role[0]!='admin':
        print(role)
        if role[0]=='manager':
            is_auth=0
        else:
            is_auth = ''.join(str(random.randint(0, 9)) for _ in range(12))
    else:
        is_auth=1
    encoded_password = password.encode('utf-8')
    hashed_password = hashlib.sha256(encoded_password).hexdigest()

    app.security.datastore.create_user(fname=fname, lname=lname, roles=role, mobile=mobile, email=email,
                                       password=hashed_password, authenticated=is_auth)
    db.session.commit()
    if role[0]=='user':
        smail(email, "Verify Email- MrBean Grocery App", f'Please click on the link to verify your email http://127.0.0.1:5003/verify-email/{is_auth}')

    return {"message":"Success"}
def celery_func():
    # cache.init_app(app)
    from workers import ContextTask, celery
    celery1 = celery
    celery1.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"]
    )
    celery1.Task = ContextTask
    # Setting Flask Security Setup
    cache.init_app(app)
    app.app_context().push()

    return celery1


celery = celery_func()

celery_app = celery_init_app(app)
from flask import send_file
@app.route('/download_csv')
def download_csv():
    return send_file(f'./instance/name.csv', as_attachment=True)


@app.get("/cached-data")
@cache.cached(timeout=50)
def cached_data():
    time.sleep(10)
    print("printing cached data")
    return {"cached_data": "sds"}

@app.route("/get-roles")
@cache.cached(timeout=50)
def get_roles():
    return [x.name for x in db.session.query(Role).all()]


@app.post('/signin')
def signin():
    data = request.get_json()
    email = data['email']
    print(email)
    user = db.session.query(User).filter_by(email=email).first()
    print(user)
    if user is None:
        return make_response({"message":"Invalid user!"}, 404)
    else:
        password = data['password']
        is_auth= user.authenticated
        print(email, password, is_auth)
        if is_auth ==1 :
            encoded_password = password.encode('utf-8')
            hashed_password = hashlib.sha256(encoded_password).hexdigest()
            if not verify_password(hashed_password, user.password):
                print("true")
                return make_response({"message":"Wrong Password!"}, 404)
        else:
            return make_response({"message":"User not authenticated!"}, 404)


    result = login_user(user)  # return True if able to signin the user else False
    return make_response({"role":[role.name for role in current_user.roles], "email": user.email,"mobile":user.mobile,"fname":user.fname,"lname":user.lname, "token": user.get_auth_token(),"message": "User Signed In Successfully!"},200) if result else make_response({"message":"Failed to signin!"}, 404)

@app.get('/verify-email/<string:token>')
def verify_email(token):
    from database import verify_authenticated_email
    users= verify_authenticated_email()
    print(users)
    flag=0
    for user in users:
        print(user)
        print(user.authenticated)
        if int(user.authenticated)==int(token):
            flag=1
            user.authenticated = 1
            db.session.commit()
            return  "<h3>User Authenticated Successfully!. You can close this tab<h3>", 200
            # return make_response({"message": "User Authenticated Successfully!. You can close this tab"}, 200)
        else:
            print("failed")
            continue
    if flag==0:
        return "<h3>Invalid Token or Token Expired<h3>", 404
        # return make_response({"message":"Invalid Token! or Token expired"}, 404)



@app.get("/signout")
# @login_required
def logout():
    logout_user()
    return make_response({"message":"User Logged Out Successfully!"},200)



@app.route("/get-user")
@auth_required('token')
@cache.cached(timeout=50)
def get_user():
    return {"email": current_user.email,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles]}

@app.route("/get-users")
@auth_required('token')
@roles_required('admin')
@cache.cached(timeout=50)
def get_users():
    return [{"email": user.email,
             "id": user.id,
             "role": [role.name for role in user.roles]} for user in db.session.query(User).all()]

# @app.get('/ds')
# def ds():
#     from models import Cart
#     item = db.session.query(Cart).first()
#     print(item.__dict__)
#     print(item.cart_product.__dict__)
#
#     return "hello"


@app.route('/get-user-details')
# @login_required #Only after the route otherwise wont work
def get_user_details():
    return {"username": current_user.username,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles]}


@app.route('/get-authenticated-data')
@auth_required('token')
# to allow admin and user to access the route
@roles_required('manager')
def get_authenticated_data():
    return {"username": current_user.username,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles],
             "message": "Only can access if you pass token"}



@app.route('/multiple-roles')
@roles_accepted('admin', 'manager')

def multiple_roles():
    return {"username": current_user.username,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles],
             "message": "Only can access if you are a manager or admin"}

@app.route('/get-user-token')
def get_user_token():
    return {"token": current_user.get_auth_token()}


@app.route('/user-role-data')
@roles_required('user')
def user_role_date():
    return {"username": current_user.username,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles],
             "message": "Only can access if you are a user"}




@app.route('/gen_csv')
def gen_csv():
    from tasks import bla
    task=bla.delay()
    return jsonify({"task-id": task.id})

@app.route('/task')
def taskgy():

    task=monthly_report.delay()
    return jsonify({"task-id": task.id})

@app.get('/get_csv/<task_id>')
def get_csv(task_id):
    res = AsyncResult(task_id)
    print(res)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": "Task Pending"}), 404
 

from celery.schedules import crontab
@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=55, day_of_month=20),
        engagment.s(),
    )

@app.post('/add-to-desktop')
def add_to_desktop():
    data=request.get_json()
    app_name = data['name']
    icon_path = data['icon']
    app_route = data['url']

    shortcut_path= f'/Users/shriprasad/Desktop/{app_name}'
    # Creating the desktop shortcut
    make_shortcut(app_name,shortcut_path,icon=icon_path, terminal=False)

    return {"Message":"Shortcut Created Successfully!"}

if __name__ == "__main__":
    app.run(debug=True,port=5003)