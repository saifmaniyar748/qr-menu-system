from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(10), nullable=False)
    items = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_first_request
def create_tables():
    db.create_all()

menu_items = ["Pizza", "Burger", "Pasta", "Fries", "Salad", "Soda"]

@app.route('/')
def home():
    return redirect('/table/1')

@app.route('/table/<int:table_number>')
def table_menu(table_number):
    return render_template('menu.html', table_number=table_number, menu=menu_items)

@app.route('/order', methods=['POST'])
def order():
    table_number = request.form['table']
    selected_items = request.form.getlist('items')
    items_str = ", ".join(selected_items)
    new_order = Order(table_number=table_number, items=items_str)
    db.session.add(new_order)
    db.session.commit()
    return render_template('order_success.html', table_number=table_number, items=selected_items)

@app.route('/admin')
def admin():
    all_orders = Order.query.order_by(Order.timestamp.desc()).all()
    return render_template('admin.html', orders=all_orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
