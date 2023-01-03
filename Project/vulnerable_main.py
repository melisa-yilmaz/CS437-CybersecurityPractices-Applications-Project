from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Connect to database
def database_connection() -> sqlite3.Connection:
    connection = sqlite3.connect('database.db')
    #connection = sqlite3.connect('C:\Belgelerim\GitHub\CS437-CybersecurityPractices-Applications-Project\Project\database.db')
    return connection

# Show users based on page and entry count
def get_users(page_count, entry_count) -> list:
    start_index = (page_count-1) * entry_count
    all_users = []
    
    connection = database_connection()
    sql_query_get_users = "SELECT * FROM users LIMIT " + str(start_index + entry_count)
    get_users = connection.execute(sql_query_get_users)
    all_users_db = get_users.fetchall()

    for i in range(start_index, start_index+entry_count):
        each_user = {"id": all_users_db[i][0], "email":all_users_db[i][1], "password": all_users_db[i][2]}
        all_users.append(each_user)

    return all_users


@app.route('/page/<int:page_count>/entries/<int:entry_count>')
def show_users(page_count,entry_count):
    all_users = get_users(page_count, entry_count)
    return jsonify(all_users)


if __name__ == "__main__":
    app.run(port=4000)