from core import app, db
from core.models import *
from flask import render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename
import json

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def admin_only(func):
    if not current_user.admin:
        return redirect('/')
    return func

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        data = request.form
        print(data.get('email'))
        u = User.query.filter_by(email=data.get('email')).first()
        if u:
            if check_password_hash(u.password, data.get('password')):
                login_user(u)
                return redirect('/')
            else:
                return redirect('/login')
    return render_template('ecommerce/login.html')

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            password = generate_password_hash(data.get('password'))
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('ecommerce/register.html')

#Store Routes
@app.route('/',methods = ['GET'])
def home():
    final = Product.query.all()
    print(final)
    return render_template('ecommerce/main.html',data=final)

@app.route('/mobile',methods = ['GET'])
def mobile():
    final = Product.query.filter_by(category='mobile').all()
    print(final)
    return render_template('ecommerce/main.html',data=final)

@app.route('/laptop',methods = ['GET'])
def laptop():
    final = Product.query.filter_by(category='laptop').all()
    print(final)
    return render_template('ecommerce/main.html',data=final)

@app.route('/television',methods = ['GET'])
def television():
    final = Product.query.filter_by(category='TV').all()
    print(final)
    return render_template('ecommerce/main.html',data=final)

@app.route('/product/<id>')
def productpage(id):
    final = Product.query.filter_by(id=id).first()
    print(final)
    return render_template('ecommerce/ProductView.html',data=final)

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == 'GET':
        print(current_user.id)
        data =  db.engine.execute('''
            select * from cart_item, product where cart_item.product = product.id and cart_item.user = {}
        '''.format(current_user.id))
        final = CartItem.query.all()
        print(data)
        return render_template('ecommerce/cart.html',data=data)

    elif request.method == 'POST':
        data = request.form
        items = CartItem.query.filter_by(user=current_user.id)
        for i in items:
            print(data.get(str(i.product)+'_item_qnt'))
            #it = CartItem.query.filter_by(product=i.id).first()
            i.quantity = data.get(str(i.product)+'_item_qnt')
            db.session.commit()
        return redirect('/payments')


@app.route('/payments', methods=['GET', 'POST'])
def Payments():
    if request.method == "GET":
        items =  db.engine.execute('''
            select * from cart_item, product where cart_item.product = product.id and cart_item.user = {}
        '''.format(current_user.id))
        data = User.query.filter_by(id=current_user.id).first()
        return render_template('ecommerce/PaymentPage.html',data=data, order=items)

@app.route('/account', methods=['GET', 'POST'])
def userpage():
    if request.method == "GET":
        data = User.query.filter_by(id=current_user.id).first()
        return render_template('ecommerce/UserProfile.html',data=data)

#Admin Routes
@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
#@admin_only
def admin():
    query = Order.query.all()
    customers = User.query.all()
    count = 0
    sales = dict()
    for i in query:
        
        date = i.order_date.strftime('%b %d ')
        if date not in sales.keys():
            sales[date] = i.total
        else:
            sales[date] = sales[date] + i.total
        print(i.order_date)
        count += i.total
    print(sales)
    final = {
        'total_orders' : len(query),
        'revenue': count,
        'customers':len(customers)
    }
    return render_template('admin/main.html',data=final, sales=json.dumps(sales))

@app.route('/admin/orders')
@login_required
def orders():
    final = Order.query.all()
    return render_template('admin/Orders/orders.html',datas=final)
    # /admin/orders

@app.route('/admin/order/<id>')
@login_required
def orderitems(id):
    order = Order.query.filter_by(id=id).first()
    customer = User.query.filter_by(id=order.user).first()
    #item = OrderItem.query.filter_by(order_id=id)
    item =  db.engine.execute('''
            select * from order_item, product where order_item.product = product.id and order_item.order_id = {}
        '''.format(id))
    return render_template('admin/Orders/orderview.html',order=order, item=item, customer=customer)

@app.route('/admin/inventory')
@login_required
def inventory():
    final = Product.query.all()
    return render_template('admin/inventory/ProductList.html',datas=final)

@app.route('/admin/inventory/add')
@login_required
def AddInventory():
    return render_template('admin/inventory/AddProduct.html')

    
@app.route('/admin/inventory/edit/<id>')
@login_required
def EditInventory(id):
    final = Product.query.filter_by(id=id).first()
    return render_template('admin/inventory/EditProduct.html', data=final)


