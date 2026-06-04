import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

@st.cache_resource
def get_connection():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY, customer_name TEXT,
        city TEXT, state TEXT, age INTEGER, gender TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY, product_name TEXT,
        category TEXT, price REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY, customer_id INTEGER,
        product_id INTEGER, quantity INTEGER,
        order_date TEXT, status TEXT)''')

    customers_data = [
        (1,'Priya Sharma','Mumbai','Maharashtra',28,'Female'),
        (2,'Rahul Verma','Delhi','Delhi',35,'Male'),
        (3,'Anita Singh','Bangalore','Karnataka',24,'Female'),
        (4,'Amit Kumar','Hyderabad','Telangana',31,'Male'),
        (5,'Sneha Patel','Chennai','Tamil Nadu',27,'Female'),
        (6,'Vikram Nair','Pune','Maharashtra',42,'Male'),
        (7,'Deepa Reddy','Kolkata','West Bengal',33,'Female'),
        (8,'Arjun Mehta','Jaipur','Rajasthan',29,'Male'),
        (9,'Pooja Iyer','Ahmedabad','Gujarat',26,'Female'),
        (10,'Suresh Gupta','Lucknow','Uttar Pradesh',38,'Male'),
        (11,'Kavya Menon','Mumbai','Maharashtra',22,'Female'),
        (12,'Rajesh Das','Delhi','Delhi',45,'Male'),
        (13,'Meera Joshi','Bangalore','Karnataka',30,'Female'),
        (14,'Nikhil Tiwari','Hyderabad','Telangana',27,'Male'),
        (15,'Asha Pillai','Chennai','Tamil Nadu',36,'Female')
    ]

    products_data = [
        (1,'iPhone 15','Electronics',79999),
        (2,'Samsung TV 55"','Electronics',54999),
        (3,'Nike Running Shoes','Footwear',8999),
        (4,'Levi Jeans','Clothing',3499),
        (5,'Instant Pot','Kitchen',6999),
        (6,'MacBook Air','Electronics',114999),
        (7,'Adidas T-Shirt','Clothing',1499),
        (8,'Mixer Grinder','Kitchen',3999),
        (9,'Puma Sneakers','Footwear',5999),
        (10,'Boat Earphones','Electronics',2499),
        (11,'Kurti Set','Clothing',1299),
        (12,'Air Fryer','Kitchen',4999),
        (13,'HP Laptop','Electronics',55999),
        (14,'Woodland Shoes','Footwear',4499),
        (15,'Cotton Bedsheet','Home',1899)
    ]

    orders_data = [
        (1,1,1,1,'2024-01-15','Delivered'),
        (2,2,3,2,'2024-01-20','Delivered'),
        (3,3,6,1,'2024-02-05','Delivered'),
        (4,4,10,3,'2024-02-10','Delivered'),
        (5,5,4,2,'2024-02-14','Cancelled'),
        (6,6,2,1,'2024-03-01','Delivered'),
        (7,7,7,4,'2024-03-15','Delivered'),
        (8,8,5,1,'2024-03-20','Delivered'),
        (9,9,11,3,'2024-04-01','Delivered'),
        (10,10,13,1,'2024-04-10','Returned'),
        (11,11,9,2,'2024-04-15','Delivered'),
        (12,12,8,1,'2024-05-01','Delivered'),
        (13,13,15,2,'2024-05-10','Delivered'),
        (14,14,12,1,'2024-05-20','Delivered'),
        (15,15,14,1,'2024-06-01','Delivered'),
        (16,1,10,2,'2024-06-10','Delivered'),
        (17,2,7,3,'2024-06-15','Delivered'),
        (18,3,4,1,'2024-07-01','Cancelled'),
        (19,4,1,1,'2024-07-10','Delivered'),
        (20,5,6,1,'2024-07-20','Delivered'),
        (21,6,11,4,'2024-08-01','Delivered'),
        (22,7,3,1,'2024-08-10','Delivered'),
        (23,8,13,1,'2024-08-15','Returned'),
        (24,9,2,1,'2024-09-01','Delivered'),
        (25,10,5,2,'2024-09-10','Delivered'),
        (26,11,1,1,'2024-09-20','Delivered'),
        (27,12,9,2,'2024-10-01','Delivered'),
        (28,13,6,1,'2024-10-10','Delivered'),
        (29,14,15,3,'2024-10-20','Delivered'),
        (30,15,8,2,'2024-11-01','Delivered'),
        (31,1,4,2,'2024-11-10','Delivered'),
        (32,2,12,1,'2024-11-15','Delivered'),
        (33,3,10,4,'2024-11-20','Delivered'),
        (34,4,7,3,'2024-12-01','Delivered'),
        (35,5,14,1,'2024-12-10','Delivered'),
        (36,6,1,1,'2024-12-15','Delivered'),
        (37,7,5,1,'2024-12-20','Delivered'),
        (38,8,11,5,'2024-12-25','Delivered'),
        (39,9,13,1,'2024-12-28','Delivered'),
        (40,10,3,2,'2024-12-30','Delivered')
    ]

    cursor.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?)', customers_data)
    cursor.executemany('INSERT INTO products VALUES (?,?,?,?)', products_data)
    cursor.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)', orders_data)
    conn.commit()
    return conn

conn = get_connection()

st.title("🛒 E-Commerce Sales Analysis Dashboard")
st.markdown("**Interactive business insights from retail sales data**")
st.markdown("---")

query_kpi = '''
SELECT 
    ROUND(SUM(p.price * o.quantity), 2) as total_revenue,
    COUNT(o.order_id) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    ROUND(AVG(p.price * o.quantity), 2) as avg_order_value
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = "Delivered"
'''
kpi = pd.read_sql_query(query_kpi, conn)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{kpi['total_revenue'][0]:,.0f}")
col2.metric("Total Orders", kpi['total_orders'][0])
col3.metric("Unique Customers", kpi['unique_customers'][0])
col4.metric("Avg Order Value", f"₹{kpi['avg_order_value'][0]:,.0f}")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Revenue by Category")
    query_cat = '''
    SELECT p.category, ROUND(SUM(p.price * o.quantity), 2) as revenue
    FROM orders o JOIN products p ON o.product_id = p.product_id
    WHERE o.status = "Delivered"
    GROUP BY p.category ORDER BY revenue DESC
    '''
    df_cat = pd.read_sql_query(query_cat, conn)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='revenue', y='category', data=df_cat, palette='husl', ax=ax)
    ax.set_xlabel('Revenue (₹)')
    ax.set_ylabel('Category')
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("📊 Order Status Breakdown")
    query_status = 'SELECT status, COUNT(order_id) as count FROM orders GROUP BY status'
    df_status = pd.read_sql_query(query_status, conn)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.pie(df_status['count'], labels=df_status['status'],
            autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c', '#f39c12'])
    st.pyplot(fig2)
    plt.close()

st.markdown("---")
st.subheader("📈 Monthly Revenue Trend")
query_monthly = '''
SELECT strftime("%Y-%m", order_date) as month,
       ROUND(SUM(p.price * o.quantity), 2) as revenue
FROM orders o JOIN products p ON o.product_id = p.product_id
WHERE o.status = "Delivered"
GROUP BY month ORDER BY month
'''
df_monthly = pd.read_sql_query(query_monthly, conn)
fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(df_monthly['month'], df_monthly['revenue'], marker='o', linewidth=2, color='#e74c3c')
ax3.fill_between(range(len(df_monthly)), df_monthly['revenue'], alpha=0.3, color='#e74c3c')
ax3.set_xticks(range(len(df_monthly)))
ax3.set_xticklabels(df_monthly['month'], rotation=45)
ax3.set_xlabel('Month')
ax3.set_ylabel('Revenue (₹)')
st.pyplot(fig3)
plt.close()

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 5 Products by Revenue")
    query_prod = '''
    SELECT p.product_name, ROUND(SUM(p.price * o.quantity), 2) as revenue
    FROM orders o JOIN products p ON o.product_id = p.product_id
    WHERE o.status = "Delivered"
    GROUP BY p.product_id ORDER BY revenue DESC LIMIT 5
    '''
    df_prod = pd.read_sql_query(query_prod, conn)
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='revenue', y='product_name', data=df_prod, palette='viridis', ax=ax4)
    ax4.set_xlabel('Revenue (₹)')
    ax4.set_ylabel('Product')
    st.pyplot(fig4)
    plt.close()

with col2:
    st.subheader("👥 Top Customers by Spending")
    query_cust = '''
    SELECT c.customer_name, ROUND(SUM(p.price * o.quantity), 2) as total_spent
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON o.product_id = p.product_id
    WHERE o.status = "Delivered"
    GROUP BY c.customer_id ORDER BY total_spent DESC LIMIT 10
    '''
    df_cust = pd.read_sql_query(query_cust, conn)
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='total_spent', y='customer_name', data=df_cust, palette='magma', ax=ax5)
    ax5.set_xlabel('Total Spent (₹)')
    ax5.set_ylabel('Customer')
    st.pyplot(fig5)
    plt.close()

st.markdown("---")
st.subheader("🏙️ Revenue by City")
query_city = '''
SELECT c.city, ROUND(SUM(p.price * o.quantity), 2) as revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.status = "Delivered"
GROUP BY c.city ORDER BY revenue DESC
'''
df_city = pd.read_sql_query(query_city, conn)
fig6, ax6 = plt.subplots(figsize=(12, 5))
sns.barplot(x='revenue', y='city', data=df_city, palette='coolwarm', ax=ax6)
ax6.set_xlabel('Revenue (₹)')
ax6.set_ylabel('City')
st.pyplot(fig6)
plt.close()

st.markdown("---")
st.markdown("**Built by Vishaka Yadubanshi | Data Science Student, CBIT Kadapa**")