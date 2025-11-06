import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash

# --- 1. SET UP THE FLASK APPLICATION ---
app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Needed for flash messages

# --- 2. CONFIGURE YOUR DATABASE CONNECTION ---
DB_CONFIG = {
    'host': 'localhost',        # Or your MySQL server's IP address
    'user': 'root',             # Your MySQL username
    'password': 'Vinod123@',    # Your MySQL password
    'database': 'Market'     # The name of your database (confirmed from your screenshot)
}

# --- 3. DATABASE CONNECTION FUNCTION ---
def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# --- 4. VIEW ALL DATA PAGES (GET REQUESTS) ---

@app.route('/')
def index():
    """Homepage: Shows a list of all customers."""
    conn = get_db_connection()
    if not conn:
        return "<h1>Error: Could not connect to the database.</h1>", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers ORDER BY customer_name")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', customers=customers)

@app.route('/vendors')
def vendors_list():
    """Shows a list of all vendors."""
    conn = get_db_connection()
    if not conn:
        return "<h1>Error: Could not connect to the database.</h1>", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendors ORDER BY vendor_name")
    vendors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('vendors.html', vendors=vendors)

@app.route('/products')
def products_list():
    """Shows a list of all products and their total market quantity."""
    conn = get_db_connection()
    if not conn:
        return "<h1>Error: Could not connect to the database.</h1>", 500
    
    cursor = conn.cursor(dictionary=True)
    # Use the function to get total stock
    query = """
        SELECT 
            p.product_id, 
            p.product_name, 
            p.category, 
            p.product_price,
            (SELECT SUM(i.product_quantity) FROM inventory i WHERE i.product_id = p.product_id) AS total_stock
        FROM products p
        ORDER BY p.product_name;
    """
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/farmers')
def farmers_list():
    """Shows a list of all farmers."""
    conn = get_db_connection()
    if not conn:
        return "<h1>Error: Could not connect to the database.</h1>", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM farmers ORDER BY farmer_name")
    farmers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('farmers.html', farmers=farmers)

@app.route('/customer_orders', methods=['GET', 'POST'])
def customer_orders():
    """Search page for a customer's order history."""
    customer = None
    orders = []
    total_spent = 0

    if request.method == 'POST':
        # This name must match the 'name' attribute in the customer_orders.html form
        search_term = request.form['search_term'] 
        conn = get_db_connection()
        if not conn:
            return "<h1>Error: Could not connect to the database.</h1>", 500
        
        cursor = conn.cursor(dictionary=True)
        
        # Find the customer
        query_customer = "SELECT * FROM customers WHERE customer_id = %s OR customer_name LIKE %s"
        try:
            # Try to convert search_term to int for ID search
            customer_id_search = int(search_term)
        except ValueError:
            # If not an int, set ID search to a value that won't match (like -1)
            customer_id_search = -1

        cursor.execute(query_customer, (customer_id_search, f"%{search_term}%"))
        customer = cursor.fetchone()
        
        if customer:
            # If customer found, get their orders
            query_orders = """
                SELECT o.order_id, o.order_date, o.order_item, o.order_amount, v.vendor_name
                FROM orders o
                JOIN vendors v ON o.vendor_id = v.vendor_id
                WHERE o.customer_id = %s
                ORDER BY o.order_date DESC
            """
            cursor.execute(query_orders, (customer['customer_id'],))
            orders = cursor.fetchall()
            
            # Calculate total spent
            total_spent = sum(order['order_amount'] for order in orders)

        cursor.close()
        conn.close()

    return render_template('customer_orders.html', customer=customer, orders=orders, total_spent=total_spent)

@app.route('/inventory')
def vendor_inventory():
    """Shows a detailed list of inventory by vendor and product."""
    conn = get_db_connection()
    if not conn:
        return "<h1>Error: Could not connect to the database.</h1>", 500
    
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            v.vendor_name,
            p.product_name,
            i.product_quantity,
            i.last_update
        FROM inventory i
        JOIN vendors v ON i.vendor_id = v.vendor_id
        JOIN products p ON i.product_id = p.product_id
        ORDER BY v.vendor_name, p.product_name;
    """
    cursor.execute(query)
    inventory_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('inventory.html', items=inventory_items)


# --- 5. FUNCTIONAL FORMS (ORDER & SUPPLY) ---

@app.route('/order')
def order_form():
    """Shows the form to place a new order."""
    return render_template('order_form.html')

@app.route('/submit-order', methods=['POST'])
def submit_order_form():
    """Processes the new order form submission by calling a stored procedure."""
    # Get data from form
    order_id = request.form['order_id']
    customer_id = request.form['customer_id']
    vendor_id = request.form['vendor_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']

    conn = get_db_connection()
    if not conn:
        return "<h1>Error: Could not connect to the database.</h1>", 500

    try:
        cursor = conn.cursor()
        # Call the stored procedure
        args = (order_id, customer_id, vendor_id, product_id, quantity)
        cursor.callproc('PlaceNewOrder', args)
        conn.commit()
        flash('Order placed successfully!', 'success')
    except mysql.connector.Error as err:
        conn.rollback()
        flash(f'Error placing order: {err.msg}', 'danger')
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('order_form'))


@app.route('/supply')
def supply_form():
    """Shows the form to restock inventory."""
    return render_template('supply_form.html')

@app.route('/submit-supply', methods=['POST'])
def submit_supply_form():
    """Processes the restock form submission by calling a stored procedure."""
    # Get data from form
    farmer_id = request.form['farmer_id']
    vendor_id = request.form['vendor_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']

    conn = get_db_connection()
    if not conn:
        return "<h1>Error: Could not connect to the database.</h1>", 500

    try:
        cursor = conn.cursor()
        # Call the stored procedure
        args = (farmer_id, vendor_id, product_id, quantity)
        cursor.callproc('ProcessSupplyDelivery', args)
        conn.commit()
        flash('Inventory restocked successfully!', 'success')
    except mysql.connector.Error as err:
        conn.rollback()
        flash(f'Error processing supply: {err.msg}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('supply_form'))


# --- 6. "ADD NEW..." FORMS (CREATE DATA) ---

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    """Shows form to add a new customer and handles submission."""
    if request.method == 'POST':
        # Get data from form
        cust_id = request.form['customer_id']
        name = request.form['customer_name']
        address = request.form['customer_address']
        
        conn = get_db_connection()
        if not conn:
            return "<h1>Error: Could not connect to the database.</h1>", 500
        
        try:
            cursor = conn.cursor()
            query = "INSERT INTO customers (customer_id, customer_name, customer_address) VALUES (%s, %s, %s)"
            cursor.execute(query, (cust_id, name, address))
            conn.commit()
            flash('Customer added successfully!', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error adding customer: {err.msg}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('add_customer'))

    # If GET request, just show the form
    return render_template('add_customer.html')

@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    """Shows form to add a new vendor and handles submission."""
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            return "<h1>Error: Could not connect to the database.</h1>", 500
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO vendors (vendor_id, vendor_name, vendor_email, vendor_pancard, vendor_phone_number)
                VALUES (%s, %s, %s, %s, %s)
            """
            args = (
                request.form['vendor_id'],
                request.form['vendor_name'],
                request.form['vendor_email'],
                request.form['vendor_pancard'],
                request.form['vendor_phone']
            )
            cursor.execute(query, args)
            conn.commit()
            flash('Vendor added successfully!', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error adding vendor: {err.msg}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('add_vendor'))
        
    return render_template('add_vendor.html')

@app.route('/add_farmer', methods=['GET', 'POST'])
def add_farmer():
    """Shows form to add a new farmer and handles submission."""
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            return "<h1>Error: Could not connect to the database.</h1>", 500
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO farmers (farmer_id, farmer_name, farmer_phone_number, farmer_address)
                VALUES (%s, %s, %s, %s)
            """
            args = (
                request.form['farmer_id'],
                request.form['farmer_name'],
                request.form['farmer_phone'],
                request.form['farmer_address']
            )
            cursor.execute(query, args)
            conn.commit()
            flash('Farmer added successfully!', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error adding farmer: {err.msg}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('add_farmer'))
    
    return render_template('add_farmer.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """Shows form to add a new product and handles submission."""
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            return "<h1>Error: Could not connect to the database.</h1>", 500
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO products (product_id, product_name, category, product_quantity, product_price)
                VALUES (%s, %s, %s, %s, %s)
            """
            args = (
                request.form['product_id'],
                request.form['product_name'],
                request.form['category'],
                request.form['quantity'],
                request.form['price']
            )
            cursor.execute(query, args)
            conn.commit()
            flash('Product added successfully!', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error adding product: {err.msg}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('add_product'))

    return render_template('add_product.html')


# --- 7. "UPDATE" WORKFLOW (This is the new section) ---

@app.route('/update', methods=['GET', 'POST'])
def update_search():
    """
    This is the new search page you requested.
    It takes a type (e.g., 'customer') and an ID, then redirects 
    to the correct edit form for that item.
    """
    if request.method == 'POST':
        item_type = request.form.get('item_type')
        item_id = request.form.get('item_id')

        if not item_id:
            flash('Please enter an ID.', 'warning')
            return redirect(url_for('update_search'))

        # Based on the dropdown, redirect to the correct edit function
        if item_type == 'customer':
            return redirect(url_for('edit_customer_form', id=item_id))
        elif item_type == 'vendor':
            return redirect(url_for('edit_vendor_form', id=item_id))
        elif item_type == 'farmer':
            return redirect(url_for('edit_farmer_form', id=item_id))
        elif item_type == 'product':
            return redirect(url_for('edit_product_form', id=item_id))
        else:
            flash('Invalid item type selected.', 'danger')
            return redirect(url_for('update_search'))

    # If GET request, just show the search page
    return render_template('update_search.html')


# --- 7a. Edit and Update Customer ---
@app.route('/customer/edit/<int:id>', methods=['GET'])
def edit_customer_form(id):
    """Shows the form to edit an existing customer, pre-filled with their data."""
    conn = get_db_connection()
    if not conn:
        return "<h1>Error: Could not connect to the database.</h1>", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not customer:
        flash(f'Customer with ID {id} not found!', 'danger')
        return redirect(url_for('update_search'))
        
    return render_template('edit_customer.html', customer=customer)

@app.route('/customer/update/<int:id>', methods=['POST'])
def update_customer(id):
    """Processes the submission from the edit customer form."""
    if request.method == 'POST':
        # Get data from form
        name = request.form['customer_name']
        address = request.form['customer_address']
        
        conn = get_db_connection()
        if not conn:
            return "<h1>Error: Could not connect to the database.</h1>", 500
        
        try:
            cursor = conn.cursor()
            query = "UPDATE customers SET customer_name = %s, customer_address = %s WHERE customer_id = %s"
            cursor.execute(query, (name, address, id))
            conn.commit()
            flash('Customer updated successfully!', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error updating customer: {err.msg}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        # Redirect back to the main customers list
        return redirect(url_for('index'))


# --- 7b. Edit and Update Vendor ---
@app.route('/vendor/edit/<int:id>', methods=['GET'])
def edit_vendor_form(id):
    """Shows the form to edit an existing vendor."""
    conn = get_db_connection()
    if not conn: return "<h1>Error: Could not connect to the database.</h1>", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (id,))
    vendor = cursor.fetchone()
    cursor.close()
    conn.close()
    if not vendor:
        flash(f'Vendor with ID {id} not found!', 'danger')
        return redirect(url_for('update_search'))
    return render_template('edit_vendor.html', vendor=vendor)

@app.route('/vendor/update/<int:id>', methods=['POST'])
def update_vendor(id):
    """Processes the submission from the edit vendor form."""
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn: return "<h1>Error: Could not connect to the database.</h1>", 500
        try:
            cursor = conn.cursor()
            query = """
                UPDATE vendors SET 
                    vendor_name = %s, 
                    vendor_email = %s, 
                    vendor_pancard = %s, 
                    vendor_phone_number = %s
                WHERE vendor_id = %s
            """
            args = (
                request.form['vendor_name'],
                request.form['vendor_email'],
                request.form['vendor_pancard'],
                request.form['vendor_phone'],
                id
            )
            cursor.execute(query, args)
            conn.commit()
            flash('Vendor updated successfully!', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error updating vendor: {err.msg}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('vendors_list'))

# --- 7c. Edit and Update Farmer ---
@app.route('/farmer/edit/<int:id>', methods=['GET'])
def edit_farmer_form(id):
    """Shows the form to edit an existing farmer."""
    conn = get_db_connection()
    if not conn: return "<h1>Error: Could not connect to the database.</h1>", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM farmers WHERE farmer_id = %s", (id,))
    farmer = cursor.fetchone()
    cursor.close()
    conn.close()
    if not farmer:
        flash(f'Farmer with ID {id} not found!', 'danger')
        return redirect(url_for('update_search'))
    return render_template('edit_farmer.html', farmer=farmer)

@app.route('/farmer/update/<int:id>', methods=['POST'])
def update_farmer(id):
    """Processes the submission from the edit farmer form."""
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn: return "<h1>Error: Could not connect to the database.</h1>", 500
        try:
            cursor = conn.cursor()
            query = """
                UPDATE farmers SET 
                    farmer_name = %s, 
                    farmer_phone_number = %s, 
                    farmer_address = %s
                WHERE farmer_id = %s
            """
            args = (
                request.form['farmer_name'],
                request.form['farmer_phone'],
                request.form['farmer_address'],
                id
            )
            cursor.execute(query, args)
            conn.commit()
            flash('Farmer updated successfully!', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error updating farmer: {err.msg}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('farmers_list'))

# --- 7d. Edit and Update Product ---
@app.route('/product/edit/<int:id>', methods=['GET'])
def edit_product_form(id):
    """Shows the form to edit an existing product."""
    conn = get_db_connection()
    if not conn: return "<h1>Error: Could not connect to the database.</h1>", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    if not product:
        flash(f'Product with ID {id} not found!', 'danger')
        return redirect(url_for('update_search'))
    return render_template('edit_product.html', product=product)

@app.route('/product/update/<int:id>', methods=['POST'])
def update_product(id):
    """Processes the submission from the edit product form."""
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            return "<h1>Error: Could not connect to the database.</h1>", 500
        try:
            cursor = conn.cursor()
            query = """
                UPDATE products SET 
                    product_name = %s, 
                    category = %s, 
                    product_quantity = %s, 
                    product_price = %s
                WHERE product_id = %s
            """
            args = (
                request.form['product_name'],
                request.form['category'],
                request.form['quantity'],
                request.form['price'],
                id
            )
            cursor.execute(query, args)
            conn.commit()
            flash('Product updated successfully!', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error updating product: {err.msg}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('products_list'))


# --- 8. RUN THE APPLICATION ---
if __name__ == '__main__':
    app.run(debug=True)