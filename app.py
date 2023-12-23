from flask import Flask, jsonify, request, make_response
import bcrypt
from flask_cors import CORS
from flask_mysqldb import MySQL
app = Flask(__name__)
# app.config.from_object(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1080'
app.config['MYSQL_DB'] = 'kuma'

CORS(app)
mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    error = {}
    name = request.form.get('name')
    if name is None or name=='':
        error['name']='name is required'
    elif len(name) < 3:
        error['name']='name is too short'
    email = request.form.get('email')
    if email is None:
        error['email']='email is required'
    elif len(email) < 3:
        error['email']='email is too short'
    else:
        cursor = mysql.connection.cursor()
        cursor.execute(f'select * from users where email = "{email}"')
        if not cursor.fetchone() is None:
            error['email']='The email has already been taken'
    repassword = request.form.get('repassword')
    if repassword is None:
        error['repassword']='repassword is required'
    password = request.form.get('password')
    if password is None:
        error['password']='password is required'
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        if len(password) < 3:
            error['password']='password is too short'
        elif not bcrypt.checkpw(repassword.encode('utf-8'),hashed_password):
            error['password']='password confirmation doesn\'t match' 
    if not error=={}:
        response = make_response(
                jsonify({'error': error}),
                422
            )
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        cursor.execute(f'insert into users(name, email, password, roles) values("{name}", "{email}", "{hashed_password.decode("utf-8")}", 0)')
        mysql.connection.commit()
        cursor.close()
        return "nice";

@app.route('/login', methods=['POST'])
def login():
    error = {}
    email = request.form.get('email')
    if email is None:
        error['email']='email is required'
    password = request.form.get('password')
    if password is None:
        error['password']='password is required'
    else:
        cursor = mysql.connection.cursor()
        cursor.execute(f'select * from users where email = "{email}"')
        user = []
        for row in cursor.fetchone():
            user.append(row)

        if bcrypt.checkpw(password.encode('utf-8'),user[3].encode('utf-8')):
            return 'you are logged in!'
        else:
            response = make_response(
                jsonify({'error': error}),
                422
            )
            response.headers["Content-Type"] = "application/json"
            return response
        


@app.route('/migrate', methods=['POST'])
def migration():
    cursor = mysql.connection.cursor()
    
    #users table
    cursor.execute('''
        create table if not exists users(
        id int primary key auto_increment, 
        name varchar(90) not null, 
        email varchar(125) not null, 
        password char(60) not null, 
        roles char(1) not null,
        unique(email))
        ''')
    
    #banners table
    cursor.execute('''
        create table if not exists banners(
        id int primary key auto_increment, 
        banner text not null, 
        links text not null)
        ''')
    
    #categories table
    cursor.execute('''
        create table if not exists categories(
        id int primary key auto_increment,
        name text not null)
        ''')
    
    #products table
    cursor.execute('''
        create table if not exists products(
        id int primary key auto_increment,
        name text not null,
        description text not null,
        image text not null,
        price int unsigned not null,
        sale smallint unsigned default 0,
        created_at datetime default now(),
        categories_id int,
        foreign key(categories_id) references categories(id))
        ''')
    
    #payments table
    cursor.execute('''
        create table if not exists payments(
        id int primary key auto_increment,
        name text not null, 
        image text not null)
        ''')
    
    #carts table
    cursor.execute('''
        create table if not exists carts(
        id int primary key auto_increment,
        products_id int not null,
        users_id int not null,
        quantity int not null,
        foreign key(products_id) references products(id),
        foreign key(users_id) references users(id))
        ''')
    
    #orders table
    cursor.execute('''
        create table if not exists orders(
        id int primary key auto_increment,
        users_id int not null,
        status char(1) not null,
        foreign key(users_id) references users(id))
        ''')
    
    #products to orders relation table
    cursor.execute('''
        create table if not exists products_orders(
        id int primary key auto_increment,
        orders_id int not null,
        products_id int not null,
        quantity int not null,
        foreign key(orders_id) references orders(id),
        foreign key(products_id) references products(id))
        ''')
    
    cursor.execute('''
        create table if not exists wishlists(
        id int primary key auto_increment,
        products_id int not null,
        users_id int not null,
        foreign key(products_id) references products(id),
        foreign key(users_id) references users(id))
        ''')
    
    
    cursor.execute('''
        create table if not exists addresses(
        id int primary key auto_increment,
        users_id int not null,
        name varchar(70) not null,
        province varchar(80) not null,
        city varchar(80) not null,
        subdistrict varchar(80) not null,
        postcode char(5) not null,
        phone varchar(15) not null,
        address text not null,
        unique(name),
        foreign key(users_id) references users(id))
        ''')
    
    
    cursor.execute(f'insert into users(name, email, password, roles) values("admin", "admin@gmail.com", "{bcrypt.hashpw("admin".encode("utf-8"),bcrypt.gensalt()).decode("utf-8")}", 1)')
    mysql.connection.commit()
    cursor.close()
    return "Migration ran successfully"

if __name__ == '__main__':
    app.run()