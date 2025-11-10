from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from flask import jsonify
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

load_dotenv("credentials.env")
# --- Database connection helper ---
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")       # Your MySQL database name
    )
    return conn

# --- Routes ---
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', customers=customers)

@app.route('/vendors')
def vendors_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendors")
    vendors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('vendors.html', vendors=vendors)

@app.route('/products')
def products_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/farmers')
def farmers_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM farmers")
    farmers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('farmers.html', farmers=farmers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        name = request.form.get('name')
        address = request.form.get('address')

        # ✅ Prevent duplicate ID
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        existing = cursor.fetchone()
        if existing:
            flash(f"❌ Customer ID {customer_id} already exists! Please use a unique ID.", "danger")
            conn.close()
            return redirect(url_for('add_customer'))

        try:
            cursor.execute(
                "INSERT INTO customers (customer_id, customer_name, customer_address) VALUES (%s, %s, %s)",
                (customer_id, name, address)
            )
            conn.commit()
            flash(f"✅ Customer '{name}' added successfully!", "success")
        except Exception as e:
            flash(f"⚠️ Error adding customer: {str(e)}", "danger")

        conn.close()
        return redirect(url_for('index'))

    return render_template('add_customer.html')




# ---------------- Universal Update / Search ---------------- #
@app.route('/update_search', methods=['GET', 'POST'])
def update_search():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    category = None
    search_results = []
    selected_record = None
    columns = []

    # Step 1: Category selection
    if request.method == 'POST':
        category = request.form.get('category')
        search_term = request.form.get('search')
        record_id = request.form.get('record_id')

        # Step 2: Handle search action
        if 'search' in request.form and category:
            table = category.lower() + 's'  # Convert "Customer" → "customers"
            id_col = category.lower() + '_id'
            name_col = category.lower() + '_name'

            query = f"SELECT * FROM {table} WHERE {id_col} = %s OR {name_col} LIKE %s"
            cursor.execute(query, (search_term, f"%{search_term}%"))
            search_results = cursor.fetchall()

        # Step 3: Handle edit submission
        elif 'update' in request.form and category and record_id:
            table = category.lower() + 's'
            id_col = category.lower() + '_id'

            # Build dynamic UPDATE query
            update_data = {k: v for k, v in request.form.items() if k not in ['update', 'category', 'record_id']}
            set_clause = ', '.join([f"{col} = %s" for col in update_data.keys()])
            values = list(update_data.values()) + [record_id]

            query = f"UPDATE {table} SET {set_clause} WHERE {id_col} = %s"
            cursor.execute(query, tuple(values))
            conn.commit()
            flash(f'{category} updated successfully!', 'success')

    cursor.close()
    conn.close()

    return render_template('update_search.html',
                           category=category,
                           search_results=search_results)
    
    
@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        cursor.execute("UPDATE customers SET customer_name=%s, customer_address=%s WHERE customer_id=%s",
                       (name, address, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM customers WHERE customer_id=%s", (id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_customer.html', customer=customer)


@app.route('/delete_customer/<int:id>')
def delete_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE customer_id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Customer deleted successfully!', 'danger')
    return redirect(url_for('index'))

# ---------------- Place Order ---------------- #
@app.route('/order_form', methods=['GET', 'POST'])
def order_form():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch customers and vendors for dropdowns
    cursor.execute("SELECT customer_id, customer_name FROM customers")
    customers = cursor.fetchall()

    cursor.execute("SELECT vendor_id, vendor_name FROM vendors")
    vendors = cursor.fetchall()

    cursor.execute("SELECT product_id, product_name, product_price FROM products")
    products = cursor.fetchall()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        vendor_id = request.form['vendor_id']
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])

        # Get product price
        cursor.execute("SELECT product_price FROM products WHERE product_id = %s", (product_id,))
        price = cursor.fetchone()['product_price']
        total_amount = price * quantity

        # Get product name for the order item field
        cursor.execute("SELECT product_name FROM products WHERE product_id = %s", (product_id,))
        product_name = cursor.fetchone()['product_name']

        # Insert order
        cursor.execute("""
            INSERT INTO orders (order_id, customer_id, order_date, order_item, vendor_id, order_amount)
            VALUES (NULL, %s, CURDATE(), %s, %s, %s)
        """, (customer_id, product_name, vendor_id, total_amount))
        conn.commit()

        flash('Order placed successfully!', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('order_form.html', customers=customers, vendors=vendors, products=products)

# ---------------- Make Payment ---------------- #
@app.route('/make_payment_form', methods=['GET', 'POST'])
def make_payment_form():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all orders to choose from
    cursor.execute("SELECT order_id, customer_id, order_amount FROM orders")
    orders = cursor.fetchall()

    if request.method == 'POST':
        order_id = request.form['order_id']
        payment_amount = request.form['payment_amount']

        cursor.execute("""
            INSERT INTO payment (payment_id, order_id, payment_amount, payment_date)
            VALUES (NULL, %s, %s, CURDATE())
        """, (order_id, payment_amount))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Payment recorded successfully!', 'success')
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('make_payment.html', orders=orders)

# ---------------- Supply / Restock ---------------- #
@app.route('/supply_form', methods=['GET', 'POST'])
def supply_form():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch farmer, vendor, and product data for dropdowns
    cursor.execute("SELECT farmer_id, farmer_name FROM farmers")
    farmers = cursor.fetchall()

    cursor.execute("SELECT vendor_id, vendor_name FROM vendors")
    vendors = cursor.fetchall()

    cursor.execute("SELECT product_id, product_name FROM products")
    products = cursor.fetchall()

    if request.method == 'POST':
        farmer_id = request.form['farmer_id']
        vendor_id = request.form['vendor_id']
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])

        # Insert into supply table
        cursor.execute("""
            INSERT INTO supply (farmer_id, vendor_id, supply_quantity, supply_date)
            VALUES (%s, %s, %s, CURDATE())
        """, (farmer_id, vendor_id, quantity))

        # Update inventory — add if exists, else insert
        cursor.execute("""
            INSERT INTO inventory (vendor_id, product_id, product_quantity, last_update)
            VALUES (%s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE 
                product_quantity = product_quantity + VALUES(product_quantity),
                last_update = NOW();
        """, (vendor_id, product_id, quantity))

        conn.commit()
        cursor.close()
        conn.close()
        flash('Supply recorded and inventory updated successfully!', 'success')
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('supply_form.html', farmers=farmers, vendors=vendors, products=products)

# ---------------- Customer Orders ---------------- #
@app.route('/customer_orders')
def customer_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            o.order_id,
            c.customer_name,
            v.vendor_name,
            o.order_date,
            o.order_item,
            o.order_amount
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN vendors v ON o.vendor_id = v.vendor_id
        ORDER BY o.order_date DESC
    """)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('customer_orders.html', orders=orders)

# ---------------- Vendor Inventory ---------------- #
@app.route('/vendor_inventory')
def vendor_inventory():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            v.vendor_name,
            p.product_name,
            i.product_quantity,
            i.last_update
        FROM inventory i
        JOIN vendors v ON i.vendor_id = v.vendor_id
        JOIN products p ON i.product_id = p.product_id
        ORDER BY v.vendor_name ASC, p.product_name ASC
    """)
    inventory = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group data by vendor for organized display
    grouped_inventory = {}
    for item in inventory:
        vendor = item["vendor_name"]
        if vendor not in grouped_inventory:
            grouped_inventory[vendor] = []
        grouped_inventory[vendor].append(item)

    return render_template("vendor_inventory.html", grouped_inventory=grouped_inventory)

# ---------------- Edit Product ---------------- #
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']

        cursor.execute("""
            UPDATE products
            SET product_name = %s, category = %s, product_quantity = %s, product_price = %s
            WHERE product_id = %s
        """, (name, category, quantity, price, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products_list'))

    # Fetch the product to edit
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_product.html', product=product)


# ---------------- Delete Product ---------------- #
@app.route('/delete_product/<int:id>')
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Product deleted successfully!', 'danger')
    return redirect(url_for('products_list'))

# ---------------- API: Get Products for Selected Vendor ---------------- #

@app.route('/get_vendor_products/<int:vendor_id>')
def get_vendor_products(vendor_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.product_id, p.product_name, p.product_price, i.product_quantity
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        WHERE i.vendor_id = %s AND i.product_quantity > 0
    """, (vendor_id,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

# ---------------- Universal Delete Page ---------------- #
@app.route('/delete_record', methods=['GET', 'POST'])
def delete_record():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    category = None
    results = []

    if request.method == 'POST':
        category = request.form.get('category')
        search_term = request.form.get('search')
        delete_id = request.form.get('delete_id')

        # Step 1: Handle Deletion
        if 'delete' in request.form and delete_id and category:
            table = category.lower() + 's'
            id_col = category.lower() + '_id'
            cursor.execute(f"DELETE FROM {table} WHERE {id_col} = %s", (delete_id,))
            conn.commit()
            flash(f"{category} with ID {delete_id} deleted successfully!", "danger")

        # Step 2: Search functionality
        elif 'search' in request.form and category:
            table = category.lower() + 's'
            id_col = category.lower() + '_id'
            name_col = category.lower() + '_name'
            query = f"SELECT * FROM {table} WHERE {id_col} = %s OR {name_col} LIKE %s"
            cursor.execute(query, (search_term, f"%{search_term}%"))
            results = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('delete_record.html', category=category, results=results)

@app.route('/search_orders')
def search_orders():
    query = request.args.get('query', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT o.order_id, o.order_date, o.order_item, o.order_amount,
               c.customer_name, v.vendor_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN vendors v ON o.vendor_id = v.vendor_id
        WHERE c.customer_id = %s OR c.customer_name LIKE %s
    """
    try:
        # Try to interpret query as ID
        id_val = int(query)
    except ValueError:
        id_val = -1  # will never match

    cursor.execute(sql, (id_val, f"%{query}%"))
    orders = cursor.fetchall()
    conn.close()

    return jsonify({"orders": orders})

@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        vendor_id = request.form.get('vendor_id')
        name = request.form.get('name')
        email = request.form.get('email')
        pancard = request.form.get('pancard')
        phone = request.form.get('phone_number')

        # ✅ Check for duplicate ID
        cursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (vendor_id,))
        existing = cursor.fetchone()
        if existing:
            flash(f"❌ Vendor ID {vendor_id} already exists! Please use a unique ID.", "danger")
            conn.close()
            return redirect(url_for('add_vendor'))

        try:
            cursor.execute(
                "INSERT INTO vendors (vendor_id, vendor_name, vendor_email, vendor_pancard, vendor_phone_number) VALUES (%s, %s, %s, %s, %s)",
                (vendor_id, name, email, pancard, phone)
            )
            conn.commit()
            flash(f"✅ Vendor '{name}' added successfully!", "success")
        except Exception as e:
            flash(f"⚠️ Error adding vendor: {str(e)}", "danger")

        conn.close()
        return redirect(url_for('vendors_list'))

    return render_template('add_vendor.html')


@app.route('/add_farmer', methods=['GET', 'POST'])
def add_farmer():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        farmer_id = request.form.get('farmer_id')
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')

        # validate presence
        if not (farmer_id and name and phone and address):
            flash("Please fill all fields.", "danger")
            conn.close()
            return redirect(url_for('add_farmer'))

        # duplicate check
        cursor.execute("SELECT 1 FROM farmers WHERE farmer_id = %s", (farmer_id,))
        if cursor.fetchone():
            flash(f"Farmer ID {farmer_id} already exists. Choose a unique ID.", "danger")
            conn.close()
            return redirect(url_for('add_farmer'))

        try:
            cursor.execute(
                "INSERT INTO farmers (farmer_id, farmer_name, farmer_phone_number, farmer_address) VALUES (%s, %s, %s, %s)",
                (farmer_id, name, phone, address)
            )
            conn.commit()
            flash(f"Farmer '{name}' added.", "success")
        except Exception as e:
            flash(f"Error adding farmer: {e}", "danger")
        finally:
            conn.close()

        return redirect(url_for('farmers_list'))

    return render_template('add_farmer.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        quantity = request.form.get('quantity')

        if not (product_id and name and category and price and quantity):
            flash("Please fill all fields.", "danger")
            conn.close()
            return redirect(url_for('add_product'))

        cursor.execute("SELECT 1 FROM products WHERE product_id = %s", (product_id,))
        if cursor.fetchone():
            flash(f"Product ID {product_id} already exists. Use a unique ID.", "danger")
            conn.close()
            return redirect(url_for('add_product'))

        try:
            cursor.execute(
                "INSERT INTO products (product_id, product_name, category, product_quantity, product_price) VALUES (%s, %s, %s, %s, %s)",
                (product_id, name, category, quantity, price)
            )
            conn.commit()
            flash(f"Product '{name}' added.", "success")
        except Exception as e:
            flash(f"Error adding product: {e}", "danger")
        finally:
            conn.close()

        return redirect(url_for('products_list'))

    return render_template('add_product.html')



if __name__ == '__main__':
    app.run(debug=True)