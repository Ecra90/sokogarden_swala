from flask import *
import pymysql
app = Flask(__name__)
@app.route('/api/signup',methods=['POST'])
def Signup():
    #extract values posted in the request, and we store them in a variable
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    #connection to database
    connection = pymysql.connect(host='localhost',user='root',password='',database='dailyyoghurts_swala')
    #cursor object creation-to help us in the manipulaltion of our backend to execute any functionality needed.
    cursor = connection.cursor()
    # sql query to insert
    sql = 'INSERT INTO users(username,email,password,phone)VALUES(%s,%s,%s,%s)'
    #prepare data to replace the palce holders
    data = (username,email,password,phone)
    #we use the cursor to execute the sql and the data
    cursor.execute(sql,data)
    #save the changes
    connection.commit()
    return jsonify({'message':'sign up successful'})

if __name__ == '__main__':
    app.run(debug=True)
