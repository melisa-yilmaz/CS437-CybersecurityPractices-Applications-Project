import local_settings
from flask import Flask, jsonify, render_template, redirect, request
from flask_limiter import Limiter
from flask_mail import Mail, Message
from flask_login import login_user, login_required, current_user, logout_user, LoginManager,  UserMixin
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = local_settings.DB_URI
app.config['SECRET_KEY'] = local_settings.DB_SECRET_KEY

db.init_app(app)

class Users(UserMixin):
    def __init__(self, email, uid, password):
        self.uid = uid
        self.email = email
        self.password = password
        self.authenticated = False

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return True
    
    def get_id(self):
        return self.uid


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = local_settings.MAIL_ADDRESS
app.config['MAIL_PASSWORD'] = local_settings.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    conn = database_connection()
    curs = conn.cursor()
    curs.execute("SELECT * from users where id = " + str(user_id))
    lu = curs.fetchone()
    if lu is None:
        return None

    return Users(lu[1], int(lu[0]), lu[2])
        

# Get the email of the from the logged-in user's session
@login_required
def get_current_user_email():
    user_email = current_user.email
    #print("Current user email", user_email)
    if user_email:
        print("Current user email", user_email)
        return str(user_email)
    return None


limiter = Limiter(
    app=app,
    key_func=get_current_user_email,
    default_limits=["20 per day"]
    )


# Send email to the user when rate limiting occurs
def send_email_to_user() -> str:
    msg = Message('Rate Limiting Applied', sender ='437testmail@gmail.com', recipients = [get_current_user_email()])
    msg.body = "Hello, this message is sent to let you know there have been large number of requests sent from your account."
    mail.send(msg)
    print("E-mail sent.")
    return "Message sent!"


# Connect to database
def database_connection() -> sqlite3.Connection:
    connection = sqlite3.connect('database.db')
    #connection = sqlite3.connect('C:\Belgelerim\GitHub\CS437-CybersecurityPractices-Applications-Project\Project\database.db')
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
    #names = ["Araminta", "Arden", "Azalea", "Birdie", "Blythe", "Clover", "Lilac", "Lavender", "Posey", "Waverly","Birch", "Booker", 
    # "Dane", "Garrison", "Hale", "Kit", "Oberon", "Shaw", "Tobin", "Oliver","Charlie","Melisa","Sinan","Kalender","Sinali"]
    connection = database_connection()
    cursor = connection.cursor()
    test_mail_insert = "INSERT INTO users (id, email, password) VALUES (5336641108, 'sinan_cetingoz1998@hotmail.com', '123456')"
    cursor.execute(test_mail_insert)
    for i in range(20,1000000):
        sqlite_insert_query = "INSERT INTO users (id, email, password) VALUES (" + str(i) + ", 'users" + str(i)  + "@gmail.com','123456')"
        cursor.execute(sqlite_insert_query)
    connection.commit()

# Show users based on page and entry count
def get_users(page_count, entry_count) -> list:

    if entry_count > 20:
        entry_count = 20

    start_index = (page_count-1) * entry_count
    all_users = []
    
    connection = database_connection()
    sql_query_get_users = "SELECT * FROM users LIMIT " + str(start_index + entry_count)
    get_users = connection.execute(sql_query_get_users)
    all_users_db = get_users.fetchall()

    print(all_users_db)

    for i in range(start_index, start_index+entry_count):
        each_user = {"id": all_users_db[i][0], "email":all_users_db[i][1], "password": all_users_db[i][2]}
        all_users.append(each_user)

    return all_users

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/page/<int:page_count>/entries/<int:entry_count>')
@login_required
@limiter.limit("20 per day")
def show_users(page_count,entry_count):
    print(current_user.email)
    all_users = get_users(page_count, entry_count)
    return jsonify(all_users)


@app.errorhandler(429)
def ratelimit_handler():
    send_email_to_user()
    return "You have exceeded your daily rate-limit", 429

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = database_connection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM users WHERE email = \'" + str(email) + "\'")
    user = curs.fetchall()

    if not len(user) > 0:
        return redirect('/login')

    Us = load_user(user[0][0])
    if email == Us.email and password == Us.password:
        login_user(Us, remember=False)
        return redirect('/page/1/entries/20')

    return redirect('/login')
        

@app.route('/logout')
def logout_post():
    logout_user()
    return redirect('/login')


if __name__ == "__main__":
    app.run(port=4000)



    


    




    





















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
