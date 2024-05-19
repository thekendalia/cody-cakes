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


        
def foodlist():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT *
                FROM food
            ''')
            return cur.fetchall()

        
def insert_user(name, email, password):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO users (name, email, password, address_street, address_zip, country)
                VALUES (%s, %s, %s, '', 0, '');
            ''', (name, email, password))
            conn.commit()
            
def cake_create(name, description, price, quantity, images):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO cake (name, description, price, quantity, images)
                VALUES (%s, %s, %s, %s, %s);
            ''', (name, description, price, quantity, images))
            conn.commit()
            
def cake_delete(cake_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                DELETE FROM cake
                WHERE id = %s;
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
                id
                FROM users WHERE email = %s;
            ''', (email,))
            result = cur.fetchone()
            if result is None:
                return None, None, None, None, None, None
            else:
                return result[1], result[0], result[2], result[3], result[4], result[5]
            
def update_profile(name: str, email: str, zip: int, country: str, street: str, id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                UPDATE users
                SET name = %s, email = %s, address_zip = %s, country = %s, address_street = %s
                WHERE id = %s
                RETURNING *;
            ''', [name, email, zip, country, street, id])
            return cur.fetchone()
        
def update_stock(stock: bool, id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                UPDATE cake
                SET is_sold_out = %s
                WHERE id = %s
                RETURNING *;
            ''', [stock, id])
            return cur.fetchone()
            
def login(email, password):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
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
                return None, None, None, None
            else:
                return result['name'], result['email'], result['orders'], result['is_admin']
            
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