from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import get_jwt,create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
from cerberus import Validator 
import bcrypt
from flask_cors import CORS
from flask_mysqldb import MySQL
from datetime import timedelta,datetime,timezone
from werkzeug.utils import secure_filename
import os 
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'kuma'
app.config['JWT_SECRET_KEY'] = '56b80543728020a3cd8d0ac0344b4b6d51c5af91ce8ee0d215983d0550a057be'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=10)
app.config['UPLOAD_FOLDER'] = '/home/shinslime/web-app/kuma/public/uploaded'

ALLOWED_EXTENSIONS = set(['webp', 'png', 'jpg', 'jpeg'])

CORS(app,supports_credentials=True)
mysql = MySQL(app)
jwt = JWTManager(app)

class MyValidator(Validator):
    def _validate_email(self, constraint, field, value):
        """ Test the oddity of a value.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        cursor = mysql.connection.cursor()
        cursor.execute(f'select * from users where email = "{value}"')
        if constraint is True and not cursor.fetchone() is None:
            cursor.close() 
            self._error(field, "The email has already been taken")

@app.route('/register', methods=['POST'])
def register():
    schema = {
        'name':{'required':True, 'type':'string','min':4},
        'email':{'required':True, 'type':'string','min':8, 'email':True},
        'password':{'required':True, 'type':'string'},
        'repassword':{'required':True, 'type':'string'}
    }
    v = MyValidator(schema)
    if v.validate(request.form):
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into users(name, email, password, roles) values("{name}", "{email}", "{hashed_password.decode("utf-8")}", 0)')
        mysql.connection.commit()
        user_id = cursor.lastrowid
        cursor.close() 
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        response = jsonify({'name':name,'email':email})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response, 201;
    else:
        response = make_response(
                jsonify({'error': v.errors}),
                422
            )
        response.headers["Content-Type"] = "application/json"
        return response
        

@app.route('/login', methods=['POST'])
def login():
    schema = {
        'email':{'required':True, 'type':'string','min':8},
        'password':{'required':True, 'type':'string'}
    }
    v = Validator(schema)
    if v.validate(request.form):
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == "" or password == "":
            v.errors['email'] = 'email or password cannot be empty'
            response = make_response(
                    jsonify({'error': v.errors}),
                    422)
            return response
        
        cursor = mysql.connection.cursor()
        cursor.execute(f'select * from users where email = "{email}"')
        user = cursor.fetchone()
        if not user is None:
            if bcrypt.checkpw(password.encode('utf-8'),user[3].encode('utf-8')):
                access_token = create_access_token(identity=user[0])
                refresh_token = create_refresh_token(identity=user[0])
                response = jsonify({'name':user[1],'email':user[2]})
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response, 200;
        else:
            v.errors['email'] = 'incorrect email address or password'
    response = make_response(
        jsonify({'error': v.errors}),
        422
    )
    
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/check', methods=['POST'])
@jwt_required()
def check():
    cursor = mysql.connection.cursor()
    cursor.execute(f'select * from users where id = "{get_jwt_identity()}"')
    user = cursor.fetchone()
    cursor.close()
    if user is not None:
        response = jsonify({'name':user[1],'email':user[2],'role':user[4]})
        return response, 200  
        
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    response = jsonify({'refreshed': True})
    set_access_cookies(response, new_token)
    return response, 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
  response = jsonify()
  unset_jwt_cookies(response)
  return response, 200  




























def image_validation(files):
    if 'image' not in files:
        return False 
    if files['image'].filename == '':
        return False
    return True

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/payment', methods=['POST','PUT','DELETE'])
@jwt_required()
def payment():
    if get_jwt_identity() != 1:
        return jsonify("not authorized", 401)
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        if image_validation(request.files):
            image = request.files['image']
            if image and allowed_file(image.filename):
                imagename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
                cursor.execute(f'insert into payments(name,image) values("{request.form.get("name")}","{imagename}")')
                mysql.connection.commit()
                cursor.close()   
                response = jsonify("Successfully created data")
                return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE payments set name="{request.form.get("name")}", image="{request.form.get("image")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully updated data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from payments where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200

@app.route('/payment_get', methods=['GET'])
def payment_select():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from payments')
    payments = []
    for payment in cursor.fetchall():
        payments.append({
            "id": payment[0],
            "name": payment[1],
            "image": payment[2]
        })
    cursor.close()   
    response = jsonify(payments)
    return response


@app.route('/category', methods=['POST','PUT','DELETE'])
@jwt_required()
def category():
    if get_jwt_identity() != 1:
        return jsonify("not authorized", 401)
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into categories(name) values("{request.form.get("name")}")')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully created data")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE categories set name="{request.form.get("name")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully updated data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from categories where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200
    
@app.route('/category_get', methods=['GET'])
def categorie_select():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from categories')
    categories = []
    for category in cursor.fetchall():
        categories.append({
            "id": category[0],
            "name": category[1]
        })
    cursor.close()   
    response = jsonify(categories)
    return response



@app.route('/banner', methods=['POST','PUT','DELETE'])
@jwt_required()
def banner():
    if get_jwt_identity() != 1:
        return jsonify("not authorized", 401)
    if request.method == 'POST':
        if image_validation(request.files):
            image = request.files['image']
            if image and allowed_file(image.filename):
                imagename = secure_filename(str(datetime.now())+image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
                cursor = mysql.connection.cursor()
                cursor.execute(f'insert into banners(banner,links) values("{imagename}","{request.form.get("link")}")')
                mysql.connection.commit()
                cursor.close()   
                response = jsonify("Successfully created data")
                return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE banners set banner="{request.form.get("banner")}", link="{request.form.get("link")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully updated data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'select banner from banners where id={request.form.get("id")}')
        
        os.remove('/home/shinslime/web-app/kuma/public/uploaded/'+cursor.fetchone()[0])
        cursor.execute(f'delete from banners where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200

@app.route('/banner_get', methods=['GET'])
def banner_select():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from banners')
    banners = []
    for banner in cursor.fetchall():
        banners.append({
            "id": banner[0],
            "banner": banner[1],
            "link": banner[2],
        })
    cursor.close()   
    response = jsonify(banners)
    return response


@app.route('/size', methods=['POST','PUT','DELETE'])
@jwt_required()
def size():
    if get_jwt_identity() != 1:
        return jsonify("not authorized",401) 
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into sizes(name) values("{request.form.get("name")}")')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully created data")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE sizes set name="{request.form.get("name")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully updated data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from sizes where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200

@app.route('/size_get', methods=['GET'])
def size_select():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from sizes')
    sizes = []
    for size in cursor.fetchall():
        sizes.append({
            "id": size[0],
            "name": size[1]
        })
    cursor.close()   
    response = jsonify(sizes)
    return response


@app.route('/gender', methods=['POST','PUT','DELETE'])
@jwt_required()
def gender():
    if get_jwt_identity() != 1:
        return jsonify("not authorized",401)
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into genders(name) values("{request.form.get("name")}")')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully created data")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE genders set name="{request.form.get("name")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully updated data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from genders where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200

@app.route('/gender_get', methods=['GET'])
def gender_select():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from genders')
    # genders = cursor.fetchall()
    genders = []
    for gender in cursor.fetchall():
        genders.append({
            "id": gender[0],
            "name": gender[1]
        })
    cursor.close()   
    response = jsonify(genders)
    return response


@app.route('/brand', methods=['POST','PUT','DELETE'])
@jwt_required()
def brand():
    if get_jwt_identity() != 1:
        return jsonify("not authorized", 401)
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into brands(name) values("{request.form.get("name")}")')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully created data")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE brands set name="{request.form.get("name")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully updated data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from brands where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200
    
@app.route('/brand_get', methods=['GET'])
def brand_select():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from brands')
    brands = []
    for brand in cursor.fetchall():
        brands.append({
            "id": brand[0],
            "name": brand[1]
        })
    cursor.close()   
    response = jsonify(brands)
    return response

@app.route('/shipping', methods=['POST','PUT','DELETE'])
@jwt_required()
def shipping():
    if get_jwt_identity() != 1:
        return jsonify("not authorized", 401)
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into shippings(name,cost) values("{request.form.get("name")}",{request.form.get("cost")})')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully created data")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE shippings set name="{request.form.get("name")}", cost={request.form.get("cost")} where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully updated data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from shippings where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200
    
@app.route('/shipping_get', methods=['GET'])
def shipping_select():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from shippings')
    # shippings = cursor.fetchall()
    shippings = []
    for shipping in cursor.fetchall():
        shippings.append({
            "id": shipping[0],
            "name": shipping[1],
            "price": shipping[2]
        })
    cursor.close()   
    response = jsonify(shippings)
    return response

@app.route('/product', methods=['POST','PUT','DELETE'])
@jwt_required()
def product():
    if get_jwt_identity() != 1:
        return jsonify("not authorized", 401)
    if request.method == 'POST':
        if image_validation(request.files):
            image = request.files['image']
            if image and allowed_file(image.filename):
                imagename = secure_filename(str(datetime.now())+image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
                cursor = mysql.connection.cursor()
                cursor.execute(f'insert into products(name, description, image, sku, color, price, sale, categories_id, brands_id, genders_id) values("{request.form.get("name")}","{request.form.get("description")}","{imagename}","{request.form.get("sku")}","{request.form.get("color")}",{request.form.get("price")},{request.form.get("sale")},"{request.form.get("categories_id")}","{request.form.get("brands_id")}","{request.form.get("genders_id")}")')
                mysql.connection.commit()
                cursor.close()   
                response = jsonify("Successfully created data")
                return response, 201
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE products set name="{request.form.get("name")}", description="{request.form.get("description")}", image="{request.form.get("image")}", sku="{request.form.get("sku")}", color="{request.form.get("color")}", stocks="{request.form.get("stocks")}", price={request.form.get("price")}, sale={request.form.get("sale")},categories_id="{request.form.get("categories_id")}",brands_id="{request.form.get("brands_id")}", sizes_id="{request.form.get("sizes_id")}", genders_id="{request.form.get("genders_id")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully updated data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from products where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200
    


@app.route('/product_get', methods=['GET'])
@jwt_required( optional=True )
def product_select():
    cursor = mysql.connection.cursor()
    if request.args.get('id') is None:
        cursor.execute('select p.* ,b.name as brand, c.name as category, g.name as gender from products p, brands b, categories c, genders g where b.id = p.brands_id and c.id = p.categories_id and g.id = p.genders_id order by p.id desc')
    else:
        cursor.execute(f'select p.* ,b.name as brand, c.name as category, g.name as gender from products p, brands b, categories c, genders g where b.id = p.brands_id and c.id = p.categories_id and g.id = p.genders_id and p.id={request.args.get("id")} order by p.id desc')
    products = []
    fetch = cursor.fetchall()
    for product in fetch:
        tempSize = []
        wishlist = []
        if get_jwt_identity() is not None:
            cursor.execute(f'select id from wishlists where products_id={product[0]} and users_id={get_jwt_identity()}')
            wishlist = cursor.fetchone()
            if wishlist is None:
                wishlist = []
        cursor.execute(f'select s.id, s.name, ps.stocks, ps.id from products_sizes ps, sizes s, products p where p.id=ps.products_id and ps.sizes_id=s.id and p.id={product[0]}')
        for size in cursor.fetchall():
            tempSize.append({
                "id":size[0],
                "name":size[1],
                "quantity":size[2],
                "products_sizes_id":[3]
            })
        products.append({
            "id": product[0],
            "name": product[1],
            "description": product[2],
            "image": product[3],
            "sku": product[4],
            "color": product[5],
            "price": product[6],
            "sale": product[7],
            "categories_id": product[8],
            "brands_id": product[9],
            "genders_id": product[10],
            "created_at": product[11],
            "brand": product[12],
            "category": product[13],
            "gender": product[14],
            "sizes": tempSize,
            "wishlist": wishlist 
        })
    cursor.close()   
    response = jsonify(products)
    return response

@app.route('/cart', methods=['POST','DELETE','PUT','GET'])
@jwt_required()
def cart():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'select id from carts where products_id={request.form.get("products_id")} and users_id={get_jwt_identity()} and sizes_id={request.form.get("sizes_id")}')
        cart = cursor.fetchone()
        if cart is None:
            cursor.execute(f'insert into carts(products_id,users_id,quantity,sizes_id) values({request.form.get("products_id")},{get_jwt_identity()},{request.form.get("quantity")},{request.form.get("sizes_id")})')
        else:
            cursor.execute(f'update carts set quantity=quantity+{request.form.get("quantity")} where id = {cart[0]} ')
        
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully created data")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'update carts set quantity={request.form.get("quantity")} where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()
        response = jsonify("Successfully updated data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from carts where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(f'select p.id, p.name, p.image, p.color, s.name, cat.name, p.price, p.sale, c.quantity, s.id, c.id, p.brands_id from carts c, sizes s, products p, categories cat where users_id={get_jwt_identity()} and c.products_id = p.id and p.categories_id = cat.id and c.sizes_id = s.id')
        carts = []
        for cart in cursor.fetchall():
            cursor.execute(f'select id from wishlists where products_id={cart[0]} and users_id={get_jwt_identity()}')
            wishlist = cursor.fetchone()
            carts.append({
                "id": cart[0],
                "name": cart[1],
                "image": cart[2],
                "color": cart[3],
                "size": cart[4],
                "category": cart[5],
                "price": cart[6],
                "sale": cart[7],
                "quantity": cart[8],
                "wishlist": wishlist,
                "sizes_id": cart[9],
                "cart_id": cart[10],
                "brands_id": cart[11]
            })
        cursor.close()   
        response = jsonify(carts)
        return response

@app.route('/address', methods=['POST','DELETE','PUT','GET'])
@jwt_required()
def address():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into addresses(users_id,name,province,city,subdistrict,postcode,phone,address) values({get_jwt_identity()},"{request.form.get("name")}","{request.form.get("province")}","{request.form.get("city")}","{request.form.get("subdistrict")}","{request.form.get("postcode")}","{request.form.get("phone")}","{request.form.get("address")}")')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully created address")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'update addresses set name="{request.form.get("name")}", province="{request.form.get("province")}", city="{request.form.get("city")}", subdistrict="{request.form.get("subdistrict")}", postcode="{request.form.get("postcode")}", phone="{request.form.get("phone")}",address="{request.form.get("address")}" where users_id={get_jwt_identity()}')
        mysql.connection.commit()
        cursor.close()
        response = jsonify("Successfully updated address")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from addresses where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted address")
        return response, 200
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(f'select id,name,province,city,subdistrict,postcode,phone,address from addresses where users_id={get_jwt_identity()}')
        addresses = []
        address = cursor.fetchone()
        if address is None:
            return jsonify("There is no address"),400
        addresses= {
            "id": address[0],
            "name": address[1],
            "province": address[2],
            "city": address[3],
            "subdistrict": address[4],
            "postcode": address[5],
            "phone": address[6],
            "address": address[7],
        }
        cursor.close()   
        response = jsonify(addresses)
        return response

@app.route('/wishlist', methods=['POST','DELETE'])
@jwt_required()
def wishlist():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into wishlists(products_id,users_id) values({request.form.get("products_id")},{get_jwt_identity()})')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully created data")
        return response, 201  
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from wishlists where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200
    
@app.route('/order', methods=['POST','PUT','DELETE','GET'])
@jwt_required()
def order():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into orders(users_id,status) values({get_jwt_identity()},"0")')
        orders_id = cursor.lastrowid
        for product in request.json.get('products'):
            cursor.execute(f'insert into products_orders(orders_id,products_id,quantity,sizes_id) values({orders_id},{product["products_id"]},{product["quantity"]},{product["sizes_id"]})')
            cursor.execute(f'update products_sizes set stocks = stocks-{product["quantity"]} where sizes_id={product["sizes_id"]} and products_id={product["products_id"]}')
        cursor.execute(f'delete from carts where users_id={get_jwt_identity()}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully created data")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'update addresses set name="{request.form.get("name")}", province="{request.form.get("province")}", city="{request.form.get("city")}", subdistrict="{request.form.get("subdistrict")}", postcode="{request.form.get("postcode")}", phone="{request.form.get("phone")}",address="{request.form.get("address")}" where users_id={get_jwt_identity()}')
        mysql.connection.commit()
        cursor.close()
        response = jsonify("Successfully deleted data")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from products_orders where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("Successfully deleted data")
        return response, 200
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(f'select o.id, o.created_at, p.image, p.sku, p.price, p.sale, b.name, po.quantity, o.status, p.name, s.name as size from orders o,  products_orders po, products p, brands b, sizes s where b.id = p.brands_id and o.users_id={get_jwt_identity()} and po.products_id = p.id and po.orders_id = o.id and po.sizes_id= s.id')
        orders = cursor.fetchall()
        cursor.close()
        if orders is None:
            return jsonify("There is no orders"),400
        products = []
        for product in orders:    
            products.append({
                    "order_id": product[0],
                    "date": product[1],
                    "image": product[2],
                    "sku": product[3],
                    "price": product[4],
                    "sale": product[5],
                    "brand": product[6],
                    "quantity": product[7],
                    "status": product[8],
                    "name": product[9],
                    "size": product[10]
                })
        
        response = jsonify(products)
        return response
    
@app.route('/user', methods=['PUT','DELETE','GET'])
@jwt_required()
def user():
    cursor = mysql.connection.cursor()
    user_id = get_jwt_identity()
    name = request.form.get('name')
    password = request.form.get('password')
    changeEmail = request.form.get('changeEmail')
    email = request.form.get('email')
    changePassword = request.form.get('changePassword')
    newPassword = request.form.get('newPassword')
    
    cursor.execute(f'select password from users where id = {user_id}')
    currentPassword = cursor.fetchone()[0]
    
    if not bcrypt.checkpw(password.encode('utf-8'), currentPassword.encode('utf-8')):
        return jsonify('Invalid Password'),422
    
    if changeEmail:
        cursor.execute(f'update users set email="{email}" where id = {user_id}')
    if changePassword:
        password = bcrypt.hashpw(newPassword.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
        cursor.execute(f'update users set password="{password}" where id = {user_id}')
        
    cursor.execute(f'update users set name="{name}" where id = {user_id}')
    mysql.connection.commit()
    return jsonify("Successfully updated user"),200

if __name__ == '__main__':
    app.run()
