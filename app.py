from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import get_jwt,create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, jwt_required, JWTManager, get_jwt_identity
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
        
        # print(email)
        # print(password)
        
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
        

@app.after_request
def refresh(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        return response
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(hours=1))
        if target_timestamp > exp_timestamp:
            print("New Token!")
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        print("No Token :(")
        return response

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
                response = jsonify("successfuly created")
                return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE payments set name="{request.form.get("name")}", image="{request.form.get("image")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly updated")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from payments where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
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
        response = jsonify("successfuly created")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE categories set name="{request.form.get("name")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly updated")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from categories where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
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
                response = jsonify("successfuly created")
                return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE banners set banner="{request.form.get("banner")}", link="{request.form.get("link")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly updated")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'select banner from banners where id={request.form.get("id")}')
        
        os.remove('/home/shinslime/web-app/kuma/public/uploaded/'+cursor.fetchone()[0])
        cursor.execute(f'delete from banners where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
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
        response = jsonify("successfuly created")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE sizes set name="{request.form.get("name")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly updated")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from sizes where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
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
        response = jsonify("successfuly created")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE genders set name="{request.form.get("name")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly updated")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from genders where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
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
        response = jsonify("successfuly created")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE brands set name="{request.form.get("name")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly updated")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from brands where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
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
        response = jsonify("successfuly created")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE shippings set name="{request.form.get("name")}", cost={request.form.get("cost")} where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly updated")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from shippings where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
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
                response = jsonify("successfuly created")
                return response, 201
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE products set name="{request.form.get("name")}", description="{request.form.get("description")}", image="{request.form.get("image")}", sku="{request.form.get("sku")}", color="{request.form.get("color")}", stocks="{request.form.get("stocks")}", price={request.form.get("price")}, sale={request.form.get("sale")},categories_id="{request.form.get("categories_id")}",brands_id="{request.form.get("brands_id")}", sizes_id="{request.form.get("sizes_id")}", genders_id="{request.form.get("genders_id")}" where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly updated")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from products where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
        return response, 200
    

@app.route('/product_get', methods=['GET'])
@jwt_required(optional=True)
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
        cursor.execute(f'insert into carts(products_id,users_id,quantity,sizes_id) values({request.form.get("products_id")},{get_jwt_identity()},{request.form.get("quantity")},{request.form.get("sizes_id")})')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly created")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'update carts set quantity={request.form.get("quantity")} where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()
        response = jsonify("successfuly deleted")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from carts where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
        return response, 200
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(f'select p.id, p.name, p.image, p.color, s.name, cat.name, p.price, p.sale, c.quantity, s.id from carts c, sizes s, products p, categories cat where users_id={get_jwt_identity()} and c.products_id = p.id and p.categories_id = cat.id and c.sizes_id = s.id')
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
                "sizes_id": cart[9]
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
        response = jsonify("successfuly created")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'update addresses set name="{request.form.get("name")}", province="{request.form.get("province")}", city="{request.form.get("city")}", subdistrict="{request.form.get("subdistrict")}", postcode="{request.form.get("postcode")}", phone="{request.form.get("phone")}",address="{request.form.get("address")}" where users_id={get_jwt_identity()}')
        mysql.connection.commit()
        cursor.close()
        response = jsonify("successfuly deleted")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from addresses where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
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
        response = jsonify("successfuly created")
        return response, 201  
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from wishlists where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
        return response, 200
    
@app.route('/order', methods=['POST','PUT','DELETE','GET'])
@jwt_required()
def order():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(f'insert into orders(users_id,status) values({get_jwt_identity()},"0")')
        orders_id = cursor.lastrowid
        for product in request.json.get('products'):
            cursor.execute(f'insert into products_orders(orders_id,products_id,quantity) values({orders_id},{product["products_id"]},{product["quantity"]})')
            cursor.execute(f'update products_sizes set stocks = stocks-{product["quantity"]} where sizes_id={product["sizes_id"]} and products_id={product["products_id"]}')
        cursor.execute(f'delete from carts where users_id={get_jwt_identity()}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly created")
        return response, 201  
    if request.method == 'PUT':
        cursor = mysql.connection.cursor()
        cursor.execute(f'update addresses set name="{request.form.get("name")}", province="{request.form.get("province")}", city="{request.form.get("city")}", subdistrict="{request.form.get("subdistrict")}", postcode="{request.form.get("postcode")}", phone="{request.form.get("phone")}",address="{request.form.get("address")}" where users_id={get_jwt_identity()}')
        mysql.connection.commit()
        cursor.close()
        response = jsonify("successfuly deleted")
        return response, 200
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute(f'delete from products_orders where id={request.form.get("id")}')
        mysql.connection.commit()
        cursor.close()   
        response = jsonify("successfuly deleted")
        return response, 200
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        # cursor.execute(f'select * from orders where users_id={get_jwt_identity()}')
        
        cursor.execute(f'select o.id, o.created_at, p.image, p.sku, p.price, p.sale, b.name, po.quantity from orders o, products_orders po, products p, brands b where b.id = p.brands_id and o.users_id={get_jwt_identity()} and po.products_id = p.id')
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
                })
        
        response = jsonify(products)
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
    
    #shipppping table
    cursor.execute('''
        create table if not exists shippings(
        id int primary key auto_increment,
        name text not null,
        cost int unsigned not null)
        ''')
    
    
    #brands table
    cursor.execute('''
        create table if not exists brands(
        id int primary key auto_increment,
        name text not null)
        ''')
    
    #sizes table
    cursor.execute('''
        create table if not exists sizes(
        id int primary key auto_increment,
        name text not null)
        ''')
    
    #gender table
    cursor.execute('''
        create table if not exists genders(
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
        sku varchar(12) not null,
        color varchar(24) not null,
        price int unsigned not null,
        sale smallint unsigned default 0,
        categories_id int not null,
        brands_id int not null,
        genders_id int not null,
        created_at datetime default now(),
        foreign key(categories_id) references categories(id),
        foreign key(brands_id) references brands(id),
        foreign key(genders_id) references genders(id))
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
        sizes_id int not null,
        quantity int not null,
        foreign key(products_id) references products(id),
        foreign key(users_id) references users(id),
        foreign key(sizes_id) references sizes(id))
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
        create table if not exists products_sizes(
        id int primary key auto_increment,
        products_id int not null,
        sizes_id int not null,
        stocks int not null,
        foreign key(sizes_id) references sizes(id),
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
    
    cursor.execute("INSERT INTO `brands` VALUES (1,'Adidas'), (2,'Nike'), (3,'Puma'), (4,'Vans'), (5,'Asics')")
    cursor.execute("INSERT INTO `categories` VALUES (1,'Footwear'), (2,'Apparel'), (3,'Accessories'), (4,'Equipment')")
    cursor.execute("INSERT INTO `genders` VALUES (1,'Men'), (2,'Women'), (3,'Unisex'), (4,'Kids')")
    cursor.execute("INSERT INTO `payments` VALUES (1,'OVO','cara-isi-ulang-saldo-ovo.jpg'), (2,'BCA','836405_720.jpg'), (3,'Shopee pay','shopeepay.png'), (4,'DANA','dana.jpg')")
    cursor.execute("INSERT INTO `sizes` VALUES (1,'XS'), (2,'S'), (3,'M'), (4,'L'), (5,'XL'), (6,'XXL'), (7,'35'), (8,'36'), (9,'37'), (10,'38'), (11,'39'), (12,'40'), (13,'41'), (14,'42'), (15,'43'), (16,'44'), (17,'45'), (18,'46'), (19,'47'), (20,'48')")

    
    cursor.execute(f'insert into users(name, email, password, roles) values("admin", "admin@gmail.com", "{bcrypt.hashpw("admin".encode("utf-8"),bcrypt.gensalt()).decode("utf-8")}", 1)')
    mysql.connection.commit()
    cursor.close()
    return "Migration ran successfully"




























if __name__ == '__main__':
    app.run()