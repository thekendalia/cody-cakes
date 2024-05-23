from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from werkzeug.utils import secure_filename
from repositories import db_repo
import os
from flask_mailman import Mail, EmailMessage

mail = Mail()
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('PASS')

mail.init_app(app)



app.secret_key = 'your_secret_key_here'

UPLOAD_FOLDER = 'static/cake_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/add_cake', methods=['GET', 'POST'])
def add_cake():
    if request.method == 'POST':
        # Get form data
        cake_name = request.form['name']
        cake_description = request.form['description']
        #cake_price = request.form['price']
        cake_price = 15
        cake_quantity = 100
        print(cake_name)
        print(cake_description)
        print(cake_price)
        print(cake_quantity)

        # Get uploaded files
        files = request.files.getlist('images')
        saved_filenames = []

        # Save each file
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                saved_filenames.append(filename)
                images=",".join(saved_filenames)
        db_repo.cake_create(cake_name, cake_description, cake_price, cake_quantity, images)
        return redirect(url_for('cake'))

    return render_template('add_cake.html')

@app.route('/success')
def success():
    return "Cake added successfully!"

@app.route('/')
def index():
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    return render_template('index.html', cart_item_count=cart_item_count)

@app.route('/productpage')
def productpage():
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    id = request.args.get('cakeid')  # Use request.args.get for GET request parameters
    if id:
        print(id)
        details = db_repo.cake_details(id)
        print(details)
        return render_template('productpage.html', details=details, cart_item_count=cart_item_count)
    else:
        return "No cake ID provided", 400
    
@app.route('/cart')
def checkout():
    message = request.args.get('message', '')
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    cart = db_repo.get_cart(id)
    cost = db_repo.get_cart_cost(id)
    quantity = db_repo.get_cart_count(id)
    email = dict(session).get('email', None)
    zipc, street, country, name, user_email, id, phone = db_repo.user_info(email)
    if phone == "":
        num = ""
    else:
        num = phone
    
    details = []
    details.append(db_repo.cart_details(id))
    
    flattened_details = [item for sublist in details for item in sublist]
    print(cart)
    print("brr")
    print(details)

# Calculate the total cost for each item
    total_costs = []
    for item in flattened_details:
        total = item['price'] * item['quantity']
        total_costs.append(total)
    grandtotal = sum(total_costs)
     
    flattened_data = [item for sublist in details for item in sublist]
    
    return render_template('checkout.html', cart=cart, quantity=quantity, cost=cost, cart_item_count=cart_item_count, details=flattened_data, grandtotal=grandtotal, num=num, message=message)



@app.route('/dashboard')
def dashboard():
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    orders = db_repo.open_orders()
    print(orders)
    rev = db_repo.getrevenue()
    if rev is None:
        total = 0
    else:
        total = rev
        
    openorder = db_repo.numopen()
    closed = db_repo.numcompleted()
    totalusers = db_repo.totalnumusers()
    if session['is_admin'] == True:
        return render_template('dashboard.html', cart_item_count=cart_item_count, orders=orders, total=total, openorder=openorder, closed=closed, totalusers=totalusers)
    else: 
        return redirect(url_for('index'))
    
@app.route('/cakes')
def cake():
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    cake = db_repo.get_all_cakes()
    for entries in cake:
        print(entries)
    return render_template('product.html', cake=cake, cart_item_count=cart_item_count)

@app.get('/orders')
def orders():
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    orders = db_repo.user_orders(id)
    return render_template('orders.html', cart_item_count=cart_item_count, orders=orders)

@app.get('/contact')
def contact():
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    orders = db_repo.user_orders(id)
    return render_template('contact.html', cart_item_count=cart_item_count, orders=orders)

@app.post('/email')
def email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    print(name)
    print(email)
    print(message)
    msg = EmailMessage(
        "MAC's Tipsey Creations customer",
        f"{message}\n\nFrom, {name}",
        f"{email}",
        ["ktart2@uncc.edu"]
    )
    msg.send()
    return redirect(url_for('contact'))

@app.post('/checkout/<int:cart_id>')
def purchase(cart_id):
    print("cart id")
    print(cart_id)
    id = session['id'] if 'id' in session else None
    phone = request.form.get('phone')
    street = request.form.get('street')
    country = request.form.get('country')
    zipc = request.form.get('zip')
    comments = request.form.get('comments')
    pickup = request.form.get('pickup')
    print(pickup)

    # Debugging: Print received values
    print(f"Phone: {phone}, Country: {country}, Street: {street}, Zip: {zipc}")

    # Check if user is logged in
    id = session['id'] if 'id' in session else None
    
    if not id:
        # Handle case where user is not logged in, e.g., redirect to login
        return redirect(url_for('login'))
    
    # Ensure required fields are provided
    if phone == "" or country == "" or street == "" or zipc == "" or pickup == "0001-01-01" or pickup == "":
        # Handle the error, e.g., flash a message to the user and redirect back to the form
        return redirect(url_for('checkout', message="Phone, date, or address is empty"))
    
    if phone == "None" or country == "None" or street == "None" or zipc == "None" or pickup == "None":
        # Handle the error, e.g., flash a message to the user and redirect back to the form
        return redirect(url_for('checkout', message="Phone, date, or address is empty"))
    
    # Assuming your db_repo has appropriate methods to handle these operations
    cart = db_repo.cart_details(id)
    cart_item = cart[0]
    print(cart_item)
    if cart_item['phone'] != phone:
        db_repo.update_phone(id, phone)
    if cart_item['address_street'] != street:
        db_repo.update_address(id, street)
    if cart_item['country'] != country:
        db_repo.update_country(id, country)
    if cart_item['address_zip'] != zipc:
        db_repo.update_zip(id, zipc)
        
        
        
    db_repo.update_notes(comments, cart_id) 
    db_repo.update_pickup_date(pickup, cart_id) 
    db_repo.mark_items_as_bought(id)

    # Redirect to a success page or home page
    return redirect(url_for('index'))

@app.post('/add_to_cart')
def add_to_cart():
    user_id = session['id']
    cake_id = request.form['cake_id']
    quantity = request.form['quantity']
    size = request.form['size']
    price = request.form['price']
    print(user_id)
    print(cake_id)
    print(quantity)
    print(size)
    print(price)
    db_repo.insert_shopping_cart(user_id, cake_id, quantity, size, price)
    quantity = db_repo.get_cart_count(user_id)
    session['cart'] = quantity
    return redirect(url_for('index'))
    

@app.get('/addcake')
def addcake():
    if session['is_admin'] == False:
        return redirect(url_for('index'))
    else:
        return render_template('addcake.html')
    
@app.route('/status/<int:cake_id>', methods=['POST'])
def status(cake_id):
    cake_status = request.form.get('status')
    print(cake_status)
    print(cake_id)
    if cake_status == "in_stock":
        status = False
        db_repo.update_stock(status, cake_id)
    elif cake_status == "sold_out":
        status = True
        db_repo.update_stock(status, cake_id)
    return redirect(url_for('cake'))

@app.route('/delivered/<int:id>', methods=['POST'])
def delivered(id):
    print(id)
    details = db_repo.cart_revenue_details(id)
    print(details)
    revenue = details['price'] * details['quantity']
    db_repo.addrevenue(revenue)
    db_repo.update_delivered(id)
    rev = db_repo.getrevenue()
    return redirect(url_for('dashboard', rev=rev))
    
@app.route('/notdelivered/<int:id>', methods=['POST'])
def notdelivered(id):
    print(id)
    details = db_repo.cart_revenue_details(id)
    print(details)
    revenue = details['price'] * details['quantity']
    db_repo.subrevenue(revenue)
    db_repo.update_not_delivered(id)
    rev = db_repo.getrevenue()
    return redirect(url_for('dashboard', rev=rev))
    
    
@app.route('/deletecake/<int:id>', methods=['POST'])
def delete_cake(id):
    try:
        print(id)
        db_repo.delete_from_cart(id)
        count = db_repo.cake_to_be_sub(id)
        if count is None:
            session['cart'] = 0
        else: 
            session['cart'] = session['cart'] - count
        return redirect(url_for('checkout'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/delete_cake/<int:cake_id>', methods=['POST'])
def delete_cart(cake_id):
    try:
        db_repo.cake_delete(cake_id)
        return redirect(url_for('cake'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get('/profile')
def profile():
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    email = dict(session).get('email', None)
    print(email)
    zipc, street, country, name, user_email, id, phone = db_repo.user_info(email)
    print(zipc)
    print(street)
    session['id'] = id
    if phone == "":
        phonenum = "Not Set"
    else:
        phonenum = phone
    if zipc == 0 or street is None or country is None:
        status = "Not Set"
    else:
        status = f"{street}, {country} {zipc}"
        
    return render_template('profile.html', status=status, name=name, user_email=user_email, street=street, zipc=zipc, country=country, cart_item_count=cart_item_count, phonenum=phonenum)

@app.get('/edit_profile')
def editprofile():
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    email = dict(session).get('email', None)
    zipc, street, country, name, user_email, id, phone = db_repo.user_info(email)

    if zipc == 0 or street is None or country is None or phone is None:
        status = ""
        zipc = ""
        street = ""
        country = ""
        phone = ""
        
    return render_template('editprofile.html', zipc=zipc, street=street, country=country, name=name, user_email=user_email, cart_item_count=cart_item_count, phone=phone)

@app.route('/update_profile', methods=['GET', 'POST'])
def updateprofile():
    id = session['id'] if 'id' in session else None
    cart_item_count = db_repo.count_cart(id)
    message = request.args.get('message', '')
    if request.method == 'POST':
        id = session['id']
        name = request.form['name']
        email = session['email']
        zipc = request.form['zip']
        country = request.form['country']
        street = request.form['address']
        phone = request.form['phone']
        if email == "":
            return redirect(url_for('updateprofile', message="Email cannot be empty"))
        if name == "":
            return redirect(url_for('updateprofile', message="Name cannot be empty"))
        if zipc is "":
            zipc = 0
            update = db_repo.update_profile(name, email, zipc, country, street, id, phone)
        else:
            update = db_repo.update_profile(name, email, zipc, country, street, id, phone)
        session['name'] = name
        session['email'] = email
    
        return redirect(url_for('profile'))
    email = dict(session).get('email', None)
    zipc, street, country, name, user_email, id, phone = db_repo.user_info(email)
    if zipc == 0 or street is None or country is None or phone is None:
        status = ""
        zipc = ""
        street = ""
        country = ""
        phone = ""
    return render_template('editprofile.html', message=message, zipc=zipc, street=street, country=country, name=name, user_email=user_email, cart_item_count=cart_item_count, phone=phone)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = request.args.get('message', '')
    if request.method == 'POST':
        email = request.form['email']  # Use 'email' instead of 'Email'
        password = request.form['password']
        loginemail = email.lower()
        check, email, orders,  admin, id = db_repo.login(loginemail, password)
        if check is not None and admin is not None:  # Check for None using 'is not None'
            session['name'] = check
            session['is_admin'] = admin
            session['email'] = email
            session['orders'] = orders
            session['id'] = id
            print(admin)
            return redirect(url_for('index'))
            
        else:
            return redirect(url_for('login', message="Incorrect Password or Email"))
    return render_template('login.html', message=message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add():
    message = request.args.get('message', '')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        print(name)
        loginemail = email.lower()
        if db_repo.user_exists(loginemail):
            return redirect(url_for('add', message="User already exists!"))
        else:
            db_repo.insert_user(name, loginemail, password)
            return render_template('login.html')
    print("GoodNo")
    return render_template('signup.html', message=message)

@app.post('/logout')
def logout():
    lower = session['name'].lower()
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('index'))