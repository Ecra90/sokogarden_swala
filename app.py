from flask import *
import pymysql
import pymysql.cursors
from flask_cors import CORS
import os #it allows python code to talk/comminicate with the operating system(linux,windows,macos)
app = Flask(__name__)
CORS(app)# allows requests from external origins 
#configure our upload folder
app.config['UPLOAD_FOLDER'] = 'static/images'
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
    #signin route
@app.route('/api/signin')
def signin():
     username = request.form['username']
     password = request.form['password']
     #connect to database
     connection = pymysql.connect(host='localhost',user='root',password='',database='dailyyoghurts_swala')
     cursor = connection.cursor(pymysql.cursors.DictCursor)
     sql = 'select *from users where username = %s and password = %s'
     data = (username,password)
     cursor.execute(sql,data)
     #check if there were rows found
     count = cursor.rowcount
     if count == 0:#if rows is zero == invalid credantials
         return jsonify({'message':'signin failed'})
     else:
         #if the cursor has returned a valid user or atleast a row
         user = cursor.fetchone()
         #removethe password key
         user.pop('password', None)
         return jsonify({'message':'signin successful','user':user})
@app.route('/api/add_products',methods =['POST'])
def add_products():
    #Extracting data from the post data request
    product_name=request.form['product_name']
    product_description=request.form['product_description']
    product_cost=request.form['product_cost']
    product_photo= request.files['product_photo']
    #Extract file name
    filename = product_photo.filename
    #specify the computer path where the image will be saved(static/images)
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    product_photo.save(photo_path)
    #connection to database
    connection = pymysql.connect(host='localhost',user='root',password='',database='dailyyoghurts_swala')
    #using a cursor object for the manipulation of the backend
    cursor=connection.cursor()
    #connection python and the database
    sql= 'insert into product_details(product_name,product_description,product_cost,product_photo)values(%s,%s,%s,%s)'
    data=(product_name,product_description,product_cost,filename,)
    #using the cursor to executete sql andthe data
    cursor.execute(sql,data)
    #saving changes
    connection.commit()
    return jsonify ({'message':'product added successfully'})
@app.route('/api/get_products')
def get_products():
    #connection to database
    connection=pymysql.connect(host='localhost',user='root',password='',database='dailyyoghurts_swala')
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    sql='select * from product_details'
    #using the cursor to execute the sql query
    cursor.execute(sql)
    #fetch all the products_details from the database and store them in a variable
    products_details=cursor.fetchall()
    return jsonify({'products':products_details})
if __name__ == '__main__':
    app.run(debug=True)