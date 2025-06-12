from flask import Flask, render_template, request, redirect
app = Flask(__name__)

menu_items = [
    {'id': 1, 'name': 'Paneer Butter Masala', 'price': 180},
    {'id': 2, 'name': 'Chicken Biryani', 'price': 220},
    {'id': 3, 'name': 'Veg Fried Rice', 'price': 150},
    {'id': 4, 'name': 'Masala Dosa', 'price': 100}
]

orders = []

@app.route('/')
def index():
    return redirect('/table/1')

@app.route('/table/<int:table_id>')
def table_home(table_id):
    return render_template('index.html', table_id=table_id)

@app.route('/menu/<int:table_id>', methods=['GET', 'POST'])
def menu(table_id):
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        item = next((item for item in menu_items if item['id'] == item_id), None)
        if item:
            orders.append({'table_id': table_id, 'item': item['name'], 'status': 'Ordered'})
        return redirect(f'/menu/{table_id}')
    return render_template('menu.html', menu=menu_items)

@app.route('/admin')
def admin():
    return render_template('dashboard.html', orders=orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

