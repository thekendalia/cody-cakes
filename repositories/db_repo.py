from repositories.db import get_pool
from psycopg.rows import dict_row
from werkzeug.security import generate_password_hash, check_password_hash

def get_all_users():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    *
                FROM users;
            ''')
            return cur.fetchall()
        
def cart_revenue_details(id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    price, quantity
                FROM shopping_cart
                WHERE cart_id = %s;
            ''', (id,))
            result = cur.fetchone()
            return result
        
def getrevenue():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    revenue
                FROM users
                WHERE id = 1;
            ''')
            result = cur.fetchone()
            return result['revenue']
        
def count_cart(id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    SUM(quantity) AS total
                FROM shopping_cart WHERE user_id = %s and is_bought = FALSE;
            ''', (id,))
            result = cur.fetchone()
            # Check if result is not None and return the sum, otherwise return 0
            return result['total'] if result['total'] is not None else 0
        
def food():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT food
FROM food
ORDER BY RANDOM()
LIMIT 1;
            ''',)
            result = cur.fetchone()
            return result['food']
        
def insert_food(new_food):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO food (food)
                VALUES (%s);
            ''', (new_food,))
            conn.commit()
            return {'status': 'success', 'message': f'Inserted {new_food} into the food table.'}
        
def delete_food(food_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                DELETE FROM food
                WHERE id = %s;
            ''', (food_id,))
            conn.commit()
            return {'status': 'success', 'message': f'Deleted food item with id {food_id} from the food table.'}


        
def cake_details(id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT *
                FROM cake WHERE id_cake = %s;
            ''', (id, ))
            return cur.fetchall()
        
def numcompleted():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT COUNT(*) FROM shopping_cart WHERE is_bought = TRUE and id_delivered = true;
            ''')
            result = cur.fetchone()
            return result['count']
        
def totalnumusers():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT COUNT(*) FROM users WHERE is_admin = false;
            ''')
            result = cur.fetchone()
            return result['count']
        
def numopen():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT COUNT(*) FROM shopping_cart WHERE is_bought = TRUE and id_delivered = false;
            ''')
            result = cur.fetchone()
            return result['count']
        
def update_country(user_id, new_country):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE users
                SET country = %s
                WHERE id = %s;
            ''', (new_country, user_id))
            conn.commit()
            
def update_phone(user_id, phone):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE users
                SET phone = %s
                WHERE id = %s;
            ''', (phone, user_id))
            conn.commit()
            
def addrevenue(revenue):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE users
                SET revenue = revenue + %s
                WHERE id = 1;
            ''', (revenue, ))
            conn.commit()
            
def subrevenue(revenue):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE users
                SET revenue = revenue - %s
                WHERE id = 1;
            ''', (revenue, ))
            conn.commit()
            
def update_zip(user_id, zip):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE users
                SET address_zip = %s
                WHERE id = %s;
            ''', (zip, user_id))
            conn.commit()
            
def update_notes(note, id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE shopping_cart
                SET extra_note = %s
                WHERE cart_id = %s;
            ''', (note, id))
            conn.commit()
            
def update_pickup_date(note, id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE shopping_cart
                SET needed_date = %s
                WHERE cart_id = %s;
            ''', (note, id))
            conn.commit()
            
def update_delivered(cart_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE shopping_cart
                SET id_delivered = TRUE
                WHERE cart_id = %s;
            ''', (cart_id,))
            conn.commit()
            
def update_not_delivered(cart_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE shopping_cart
                SET id_delivered = FALSE
                WHERE cart_id = %s;
            ''', (cart_id,))
            conn.commit()
            
def update_address(user_id, address):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE users
                SET address_street = %s
                WHERE id = %s;
            ''', (address, user_id))
            conn.commit()
        
def cart_details(user_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT 
    cake.*,
    shopping_cart.*,
    users.*
FROM 
    cake
JOIN 
    shopping_cart ON cake.id_cake = shopping_cart.cake_id
JOIN
    users ON shopping_cart.user_id = users.id
WHERE 
    shopping_cart.user_id = %s and shopping_cart.is_bought = FALSE;
            ''', (user_id,))
            return cur.fetchall()
        
def open_orders():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
    cake.*,
    shopping_cart.*,
    users.*
FROM
    cake
JOIN
    shopping_cart ON cake.id_cake = shopping_cart.cake_id
JOIN
    users ON shopping_cart.user_id = users.id
WHERE
    shopping_cart.is_bought = TRUE;
            ''')
            return cur.fetchall()
        
def user_orders(id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
    cake.*,
    shopping_cart.*,
    users.*
FROM
    cake
JOIN
    shopping_cart ON cake.id_cake = shopping_cart.cake_id
JOIN
    users ON shopping_cart.user_id = users.id
WHERE
    shopping_cart.is_bought = TRUE AND shopping_cart.user_id = %s;
            ''', (id,))
            return cur.fetchall()
        
def mark_items_as_bought(user_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE shopping_cart
                SET is_bought = TRUE
                WHERE user_id = %s
            ''', (user_id,))
            conn.commit()
        
def get_cart(id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT * FROM shopping_cart WHERE user_id = %s;
            ''', (id, ))
            return cur.fetchall()
        
        
def get_cart_count(id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT SUM(quantity) AS total_quantity 
                FROM shopping_cart 
                WHERE user_id = %s;
            ''', (id, ))
            result = cur.fetchone()
            total_quantity = result['total_quantity']
            return total_quantity
        
def cake_to_be_sub(id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT SUM(quantity) AS total_quantity 
                FROM shopping_cart 
                WHERE cake_id = %s;
            ''', (id, ))
            result = cur.fetchone()
            total_quantity = result['total_quantity']
            return total_quantity
        
def get_cart_cost(id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT SUM(price) AS total_price 
                FROM shopping_cart 
                WHERE user_id = %s;
            ''', (id, ))
            result = cur.fetchone()
            total_price = result['total_price']
            return total_price

        
def insert_user(name, email, password):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO users (name, email, password, address_street, address_zip, country)
                VALUES (%s, %s, %s, '', 0, '');
            ''', (name, email, password))
            conn.commit()
            
def insert_shopping_cart(user_id, cake_id, quantity, size, price):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO shopping_cart (user_id, cake_id, quantity, size, price, extra_note, needed_date)
                VALUES (%s, %s, %s, %s, %s, '', '0001-01-01');
            ''', (user_id, cake_id, quantity, size, price))
            conn.commit()
            
def cake_create(name, description, price, quantity, images):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO cake (cake_name, description, price, quantity, images)
                VALUES (%s, %s, %s, %s, %s);
            ''', (name, description, price, quantity, images))
            conn.commit()
            
def cake_delete(cake_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                DELETE FROM cake
                WHERE id_cake = %s;
            ''', (cake_id,))
            conn.commit()
            
def delete_from_cart(cake_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                DELETE FROM shopping_cart
                WHERE cart_id = %s;
            ''', (cake_id,))
            conn.commit()
            
def get_all_cakes():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM cake;')
            cakes = cur.fetchall()
        return cakes

            
def user_exists(email):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT * FROM users WHERE email = %s;
            ''', (email,))
            user = cur.fetchone()
            return user is not None
        
def user_info(email):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT address_street,
                address_zip,
                country,
                name,
                email,
                id,
                phone
                FROM users WHERE email = %s;
            ''', (email,))
            result = cur.fetchone()
            if result is None:
                return None, None, None, None, None, None, None
            else:
                return result[1], result[0], result[2], result[3], result[4], result[5], result[6]
            
def update_profile(name: str, email: str, zip: int, country: str, street: str, id: int, phone: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                UPDATE users
                SET name = %s, email = %s, address_zip = %s, country = %s, address_street = %s, phone = %s
                WHERE id = %s
                RETURNING *;
            ''', [name, email, zip, country, street, phone, id])
            return cur.fetchone()
        
def update_stock(stock: bool, id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                UPDATE cake
                SET is_sold_out = %s
                WHERE id_cake = %s
                RETURNING *;
            ''', [stock, id])
            return cur.fetchone()
            
def login(email, password):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    id,
                    name,
                    email,
                    password,
                    orders,
                    is_admin
                FROM users
                WHERE email = %s AND users.password = %s;
            ''', (email, password))
            result = cur.fetchone()
            if result == None:
                return None, None, None, None, None
            else:
                return result['name'], result['email'], result['orders'], result['is_admin'], result['id']
            
def notes(note):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE notes
                SET notes = %s
                WHERE id = 1;
            ''', (note,))
            conn.commit()  # Ensure the transaction is committed
            return {'status': 'success', 'rowcount': cur.rowcount}
def get_note_by_id():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT notes FROM notes WHERE id = 1;')
            return cur.fetchone()

        
def fun(id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    position,
                    description,
                    img
                FROM positions
                WHERE id = %s;
            ''', (id,))
            return cur.fetchone()
        
def fun_length():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    COUNT(*) AS length
                FROM positions;
            ''')
            result = cur.fetchone()
            return result['length']
        
def fun_oral():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT position, description, img
FROM positions
WHERE is_oral = TRUE
ORDER BY RANDOM()
LIMIT 1;
            ''',)
            result = cur.fetchone()
            return result['position'], result['description'], result['img']
        
def fun_penetrate():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT position, description, img
FROM positions
WHERE is_oral = FALSE OR can_combine = TRUE
ORDER BY RANDOM()
LIMIT 1;
            ''',)
            result = cur.fetchone()
            return result['position'], result['description'], result['img']