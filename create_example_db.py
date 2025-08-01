import sqlite3
from datetime import datetime, timedelta
import random

def create_example_database(db_path: str = "example.db"):
    """
    Create an example SQLite database with four related tables:
    - customers: Customer information
    - categories: Product categories
    - products: Product catalog
    - orders: Customer orders
    """
    
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Creating example database: {db_path}")
    
    # Drop tables if they exist (for clean slate)
    tables_to_drop = ['orders', 'products', 'categories', 'customers']
    for table in tables_to_drop:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            registration_date DATE,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_date DATE,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category_id INTEGER,
            price DECIMAL(10,2) NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            description TEXT,
            sku TEXT UNIQUE,
            created_date DATE,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            order_date DATETIME,
            status TEXT DEFAULT 'pending',
            shipping_address TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    
    print("Tables created successfully!")
    
    # Insert sample data
    print("Inserting sample data...")
    
    # Sample customers
    customers_data = [
        ('John', 'Doe', 'john.doe@email.com', '555-0101', '123 Main St', 'New York', 'NY', '10001', '2023-01-15', 1),
        ('Jane', 'Smith', 'jane.smith@email.com', '555-0102', '456 Oak Ave', 'Los Angeles', 'CA', '90210', '2023-02-20', 1),
        ('Bob', 'Johnson', 'bob.johnson@email.com', '555-0103', '789 Pine Rd', 'Chicago', 'IL', '60601', '2023-03-10', 1),
        ('Alice', 'Williams', 'alice.williams@email.com', '555-0104', '321 Elm St', 'Houston', 'TX', '77001', '2023-04-05', 1),
        ('Charlie', 'Brown', 'charlie.brown@email.com', '555-0105', '654 Maple Dr', 'Phoenix', 'AZ', '85001', '2023-05-12', 1),
        ('Diana', 'Davis', 'diana.davis@email.com', '555-0106', '987 Cedar Ln', 'Philadelphia', 'PA', '19101', '2023-06-18', 0),
        ('Eva', 'Miller', 'eva.miller@email.com', '555-0107', '147 Birch Way', 'San Antonio', 'TX', '78201', '2023-07-22', 1),
        ('Frank', 'Wilson', 'frank.wilson@email.com', '555-0108', '258 Spruce St', 'San Diego', 'CA', '92101', '2023-08-30', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code, registration_date, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', customers_data)
    
    # Sample categories
    categories_data = [
        ('Electronics', 'Electronic devices and gadgets', '2023-01-01', 1),
        ('Clothing', 'Apparel and fashion items', '2023-01-01', 1),
        ('Books', 'Books and educational materials', '2023-01-01', 1),
        ('Home & Garden', 'Home improvement and gardening supplies', '2023-01-01', 1),
        ('Sports', 'Sports equipment and accessories', '2023-01-01', 1),
        ('Toys', 'Toys and games for all ages', '2023-01-01', 0)
    ]
    
    cursor.executemany('''
        INSERT INTO categories (category_name, description, created_date, is_active)
        VALUES (?, ?, ?, ?)
    ''', categories_data)
    
    # Sample products
    products_data = [
        ('Smartphone X1', 1, 699.99, 50, 'Latest smartphone with advanced features', 'PHONE-001', '2023-01-10', 1),
        ('Laptop Pro', 1, 1299.99, 25, 'High-performance laptop for professionals', 'LAPTOP-001', '2023-01-15', 1),
        ('Wireless Headphones', 1, 199.99, 100, 'Premium wireless headphones with noise cancellation', 'AUDIO-001', '2023-01-20', 1),
        ('Designer Jeans', 2, 89.99, 75, 'Comfortable and stylish denim jeans', 'CLOTH-001', '2023-02-01', 1),
        ('Cotton T-Shirt', 2, 24.99, 200, 'Basic cotton t-shirt in various colors', 'CLOTH-002', '2023-02-05', 1),
        ('Winter Jacket', 2, 149.99, 40, 'Warm winter jacket for cold weather', 'CLOTH-003', '2023-02-10', 1),
        ('Python Programming Guide', 3, 39.99, 60, 'Comprehensive guide to Python programming', 'BOOK-001', '2023-03-01', 1),
        ('Data Science Handbook', 3, 49.99, 30, 'Essential handbook for data science', 'BOOK-002', '2023-03-05', 1),
        ('Garden Hose', 4, 29.99, 80, '50-foot garden hose with spray nozzle', 'GARDEN-001', '2023-04-01', 1),
        ('Power Drill', 4, 79.99, 35, 'Cordless power drill with battery', 'TOOL-001', '2023-04-05', 1),
        ('Tennis Racket', 5, 129.99, 20, 'Professional tennis racket', 'SPORT-001', '2023-05-01', 1),
        ('Basketball', 5, 34.99, 45, 'Official size basketball', 'SPORT-002', '2023-05-05', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO products (product_name, category_id, price, stock_quantity, description, sku, created_date, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', products_data)
    
    # Generate sample orders
    orders_data = []
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    # Create orders for the past 6 months
    base_date = datetime.now() - timedelta(days=180)
    
    for i in range(50):  # Generate 50 sample orders
        customer_id = random.randint(1, 8)
        product_id = random.randint(1, 12)
        quantity = random.randint(1, 5)
        
        # Get product price (simplified - in real scenario you'd query the products table)
        product_prices = {1: 699.99, 2: 1299.99, 3: 199.99, 4: 89.99, 5: 24.99, 6: 149.99,
                         7: 39.99, 8: 49.99, 9: 29.99, 10: 79.99, 11: 129.99, 12: 34.99}
        unit_price = product_prices.get(product_id, 50.00)
        total_amount = unit_price * quantity
        
        order_date = base_date + timedelta(days=random.randint(0, 180))
        status = random.choice(statuses)
        
        # Sample addresses
        addresses = [
            '123 Main St, New York, NY 10001',
            '456 Oak Ave, Los Angeles, CA 90210',
            '789 Pine Rd, Chicago, IL 60601',
            '321 Elm St, Houston, TX 77001'
        ]
        shipping_address = random.choice(addresses)
        
        orders_data.append((customer_id, product_id, quantity, unit_price, total_amount, 
                          order_date.strftime('%Y-%m-%d %H:%M:%S'), status, shipping_address))
    
    cursor.executemany('''
        INSERT INTO orders (customer_id, product_id, quantity, unit_price, total_amount, order_date, status, shipping_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', orders_data)
    
    # Commit changes and close connection
    conn.commit()
    
    # Display summary
    print("\nDatabase created successfully with the following data:")
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    customers_count = cursor.fetchone()[0]
    print(f"- Customers: {customers_count} records")
    
    cursor.execute("SELECT COUNT(*) FROM categories")
    categories_count = cursor.fetchone()[0]
    print(f"- Categories: {categories_count} records")
    
    cursor.execute("SELECT COUNT(*) FROM products")
    products_count = cursor.fetchone()[0]
    print(f"- Products: {products_count} records")
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    orders_count = cursor.fetchone()[0]
    print(f"- Orders: {orders_count} records")
    
    conn.close()
    print(f"\nDatabase saved as: {db_path}")
    print("You can now use this database with the JSON exporter!")

def main():
    """Create the example database."""
    create_example_database("example.db")
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Run this script to create the example database")
    print("2. Use the SQLite to JSON exporter with:")
    print("   - Database path: 'example.db'")
    print("   - All tables will be exported")
    print("3. The four tables are:")
    print("   - customers: Customer information")
    print("   - categories: Product categories") 
    print("   - products: Product catalog")
    print("   - orders: Customer orders")

if __name__ == "__main__":
    main()
