from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from werkzeug.utils import secure_filename
from repositories import db_repo
import os
app = Flask(__name__)
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
        cake_price = request.form['price']
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
    return render_template('index.html')

@app.route('/cakes')
def cake():
    cake = db_repo.get_all_cakes()
    for entries in cake:
        print(entries)
    return render_template('product.html', cake=cake)

@app.get('/addcake')
def addcake():
    if session['is_admin'] == False:
        return render_template('index.html')
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
    
    
@app.route('/delete_cake/<int:cake_id>', methods=['POST'])
def delete_cake(cake_id):
    try:
        db_repo.cake_delete(cake_id)
        return redirect(url_for('cake'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get('/profile')
def profile():
    email = dict(session).get('email', None)
    print(email)
    zipc, street, country, name, user_email, id = db_repo.user_info(email)
    print(zipc)
    print(street)
    session['id'] = id

    if zipc == 0 or street is None or country is None:
        status = "Not Set"
    else:
        status = f"{street}, {country} {zipc}"
        
    return render_template('profile.html', status=status, name=name, user_email=user_email, street=street, zipc=zipc, country=country)

@app.get('/edit_profile')
def editprofile():
    email = dict(session).get('email', None)
    zipc, street, country, name, user_email, id = db_repo.user_info(email)

    if zipc == 0 or street is None or country is None:
        status = ""
        zipc = ""
        street = ""
        country = ""
        
    return render_template('editprofile.html', zipc=zipc, street=street, country=country, name=name, user_email=user_email)

@app.route('/update_profile', methods=['GET', 'POST'])
def updateprofile():
    message = request.args.get('message', '')
    if request.method == 'POST':
        id = session['id']
        name = request.form['name']
        email = session['email']
        zipc = request.form['zip']
        country = request.form['country']
        street = request.form['address']
        if email == "":
            return redirect(url_for('updateprofile', message="Email cannot be empty"))
        if name == "":
            return redirect(url_for('updateprofile', message="Name cannot be empty"))
        if zipc is "":
            zipc = 0
            update = db_repo.update_profile(name, email, zipc, country, street, id)
        else:
            update = db_repo.update_profile(name, email, zipc, country, street, id)
        session['name'] = name
        session['email'] = email
    
        return redirect(url_for('profile'))
    email = dict(session).get('email', None)
    zipc, street, country, name, user_email, id = db_repo.user_info(email)
    if zipc == 0 or street is None or country is None:
        status = ""
        zipc = ""
        street = ""
        country = ""
    return render_template('editprofile.html', message=message, zipc=zipc, street=street, country=country, name=name, user_email=user_email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = request.args.get('message', '')
    if request.method == 'POST':
        email = request.form['email']  # Use 'email' instead of 'Email'
        password = request.form['password']
        check, email, orders,  admin = db_repo.login(email, password)
        if check is not None and admin is not None:  # Check for None using 'is not None'
            session['name'] = check
            session['is_admin'] = admin
            session['email'] = email
            session['orders'] = orders
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
        if db_repo.user_exists(email):
            return redirect(url_for('add', message="User already exists!"))
        else:
            db_repo.insert_user(name, email, password)
            return render_template('login.html')
    print("GoodNo")
    return render_template('signup.html', message=message)

@app.post('/logout')
def logout():
    lower = session['name'].lower()
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('index'))