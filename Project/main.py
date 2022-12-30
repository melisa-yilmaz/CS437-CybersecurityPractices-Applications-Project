from flask import Flask, jsonify, render_template

from flask_limiter.util import get_remote_address
from flask_limiter import Limiter

from flask_mail import Mail, Message

import json
import sqlite3


app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '97e041d5e367c7'
app.config['MAIL_PASSWORD'] = 'cfaf5b99f8bafb'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["3 per day"]
)


# Connect to database
def database_connection() -> sqlite3.Connection:
    connection = sqlite3.connect('database.db')
    return connection

# Get table names from the databse
def get_table_from_db() -> sqlite3.Connection:
    connection = database_connection()
    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor = connection.cursor()
    cursor.execute(sql_query)
    return connection


# Insert users to database
def insert_users_to_db() -> None:
    # Add users to the database
    #names = ["Araminta", "Arden", "Azalea", "Birdie", "Blythe", "Clover", "Lilac", "Lavender", "Posey", "Waverly","Birch", "Booker", "Dane", "Garrison", "Hale", "Kit", "Oberon", "Shaw", "Tobin", "Oliver","Charlie","Melisa","Sinan","Kalender","Sinali"]
    connection = database_connection()
    cursor = connection.cursor()
    for i in range(20,1000000):
        sqlite_insert_query = "INSERT INTO users (id, email, password) VALUES (" + str(i) + ", 'users" + str(i)  + "@gmail.com','123456')"
        cursor.execute(sqlite_insert_query)
    connection.commit()

# Send email to the user when rate limiting occurs
def send_email_to_user() -> str:
    msg = Message('Hello from the other side!', sender ='meliisayiilmaz2@mail.com', recipients = ['meliisayiilmaz@gmail.com'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    mail.send(msg)
    print("YEYY")
    return "Message sent!"


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/page/<int:page_count>/entries/<int:entry_count>')
def show_users(page_count,entry_count):

    connection = database_connection()
    sql_query_get_users = "SELECT * FROM users"
    get_users = connection.execute(sql_query_get_users)
    all_users_db = get_users.fetchall()


    start_index = (page_count-1) * entry_count
    all_users = []

    for i in range(start_index, start_index+entry_count):
        each_user = {"id": all_users_db[i][0], "email":all_users_db[i][1], "password": all_users_db[i][2]}
        all_users.append(each_user)

    return jsonify(all_users)


@app.errorhandler(429)
def ratelimit_handler(e):
  return "You have exceeded your daily rate-limit", 429


if __name__ == "__main__":
    app.run(port=4000,debug=True)


    


    




    





















"""""
app = Flask(__name__)
api = Api(app)

def retrieve_email(user_id):
    email = ""
    return email

@app.route("/")
def index():
    return "Welcome to the API"


@app.route('/email/<user_id>')
def get_email(user_id):
    email = retrieve_email(user_id)
    return jsonify({"email": email})


if __name__ == "__main__":
    app.run()



class MyApi(Resource):
    def get(self, name,test):
        return {"name": name, "test": test}

    def post(self):
        return {"data": "Posted"}


api.add_resource(MyApi, "/helloworld/<string:name>/<int:test>")

if __name__ == "__main__":
    app.run(debug=True)


###############

app = Flask(__name__)
api = Api(app)

limiter = Limiter(app, key_func=get_remote_address)
limiter.init_app(app)

api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url = '/docs' )

class MyApi(Resource):

    def get(self, zip):
        return {
            "Response": 200,
            "data":zip
        }

    
api.add_resource(MyApi, '/weather/<string:zip>')

if __name__ == "main":
    app.run(debug=True)
"""""
