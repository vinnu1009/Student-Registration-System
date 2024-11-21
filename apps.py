from flask import Flask,render_template,request,redirect,url_for,session,flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)


app.secret_key = 'your_secure_random_key_here'

#Mysql db connection configure
db_config={
    'host':'localhost',
    'user':'root',
    'password':'10vinnu-09R',
    'database':'student'

}

#helper function to get connect db
def get_db_connection():
    try:
        connection=mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print("Error while connecting to MySQL",e)
        return None 

#static routing

@app.route("/")
def dashboard():
    if 'username' in session:
        return render_template('home_page.html',username = session['username'])
    else:
        flash('please log in first','warning')
        return redirect(url_for('login'))

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        conn=get_db_connection()
        if conn:
            cursor=conn.cursor()
            cursor.execute("SELECT*FROM users WHERE username=%s",(username,))
            user=cursor.fetchone()
            conn.close()

            if user and check_password_hash(user[5],password):
                print('yes')
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                print("Invalid username or password")
    return render_template('login.html')

@app.route("/registration", methods=['GET','POST'])
def registration():
    if request.method == "POST":
        username=request.form['username']
        Address=request.form['address']
        student_id=request.form['student_id']
        Email = request.form['email']
        password = request.form['pass']
        print(username)
        print(Address)
        print(student_id)
        print(Email)
        print(password)
        hash_pass = generate_password_hash(password)
        #connect to db
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('insert into users(username,address,student_id,Email,password) values(%s,%s,%s,%s,%s)',(username,Address,student_id,Email,hash_pass))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
    return render_template('registration1.html')


# student registartion
@app.route("/std_reg", methods=['GET', 'POST'])
def student_register():
    if request.method == "POST":
        name = request.form['name']
        address=request.form['address']
        age=request.form['age']
        email=request.form['email']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students(name,address,age,email) VALUES (%s, %s, %s, %s)",(name,address,age,email))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Student registered successfully!","success")
            return redirect(url_for('login'))
    return render_template('student_registration.html')


@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_student(id):
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("select *from students\
     where id=%s",(id,))
    student=cursor.fetchone()
    print(student)
    if request.method=="POST":
        name=request.form['name']
        address=request.form['address']
        age=request.form['age']
        email=request.form['email']
        cursor.execute("UPDATE students SET name=%s,address=%s,age=%s\
        ,email=%s where id=%s",(name,address,age,email,id))
        conn.commit()
        conn.close()
        flash("Student details updated succesfully!","success")

    return render_template('student_update.html',student=student)


@app.route('/student_list')
def student_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('student_list.html', students=students)


@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete_student(id):
    if request.method=="POST":
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("Delete From students\
        WHERE id=%s",(id,))
        conn.commit()
        conn.close()
        flash("Student deleted sucessfully","success")
        return redirect(url_for('student_list'))
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT *FROM students where id=%s",(id,))
    student=cursor.fetchone()
    conn.close()
    return render_template('Delete_confirmation.html',student=student)


@app.route('/logout')
def logout():
    session.pop('username',None)
    flash("YOu've been logged out.",'info')
    return redirect(url_for('login'))

#dynamic routing

@app.route('/users/<string:username>/<int:userid>')
def user(username,userid):
    return 'hello '+username+'my id is '+ f'{userid}'

@app.route('/show_price/<float:price>')
def show_price(price):
    return f'{price}'

@app.route('/path/<path:subpath>')
def path(subpath):
    return subpath
@app.route('/uuid/<uuid:item_id>')
def show_uuid(item_id):
    return f"The uuid is {item_id}"

app.run()