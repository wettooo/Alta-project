from core import db, app
from core.models import *
from flask import render_template, redirect, request
# from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask_login import current_user, login_required
from sqlalchemy import text

@app.route('/products',methods=["GET", "POST", "GET", "DELETE"])
def products():
    if request.method == 'GET':
        final = Product.query.all()
        return final

    elif request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            data = request.form
            print(data)
            product = Product.query.filter_by(id=data.get('PID')).first()
            product.name = data.get('name')
            product.price = data.get('price')
            product.description = data.get('description')
            product.category = data.get('category')
            product.inventory = data.get('inventory')
            db.session.commit()
            return redirect('/admin/inventory')

        else:
            data = request.form
            print(data)
            file = request.files['image']
            # filename = secure_filename(file.filename)
            image_url = os.path.join(app.config['UPLOAD_FOLDER'])
            # file.save(image_url)
            p1 = Product(
                name=data.get('name'),
                price= data.get('price'),
                inventory = data.get('inventory'),
                description = data.get('description'),
                img_url = 'static/uploads/' + file.filename
                )
            print(p1.name, p1.img_url)
            db.session.add(p1)
            db.session.commit()
            return redirect('admin/inventory/add')        

    elif request.method == 'DELETE':
        product = Product.query.filter_by(id=request.json.get('PID')).delete()
        db.session.commit()
        return {"res":"Success"}
    

    
@app.route('/user', methods=["GET", "POST", "GET", "DELETE"])
def users():
    if request.method == 'GET':
        final = User.query.all()
        return final

    elif request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            data = request.form
            print(data)
            user = User.query.filter_by(id=current_user.id).first()
            user.name = data.get('name')
            user.email = data.get('email')
            user.address_1 = data.get('address_1')
            user.address_2 = data.get('address_2')
            user.city = data.get('city')
            user.state = data.get('state')
            user.pincode = data.get('pincode')
            user.mobile = data.get('mobile')
            db.session.commit()
            return redirect('/account')
        else:
            data = dict(request.form)
            u1 = User(**data)
            db.session.add(u1)
            db.session.commit()
            return 'Success'        

    elif request.method == 'DELETE':
        user = User.query.filter_by(id=request.form.get('id')).first()
        user.delete()
        db.session.commit()
        return 'Success'


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        data = request.form
        #cartitems =  db.engine.execute(text('''
        #    select * from cart_item inner join product on cart_item.product = product.id
        #''').execution_options(autocommit=True))
        cartitems = CartItem.query.filter_by(user=current_user.id)
        #db.close()
        order = Order(user=current_user.id,order_date=datetime.now(),total=data.get('order-total'))
        db.session.add(order)
        db.session.commit()
        for item in cartitems:
            orderitem = OrderItem(order_id=order.id, product=item.product, quantity= item.quantity)
            db.session.add(orderitem)
            db.session.commit()
        
        CartItem.query.filter_by(user=current_user.id).delete()
        db.session.commit()
        return redirect('/')

@app.route('/addcartitem', methods=['GET','POST','DELETE'])
def addcart():
    if not current_user.is_authenticated:
        print('NOT AUTH')
        return redirect('/login')
    if request.method == "GET":
        final = CartItem.query.filter_by(user=current_user.id)
        return str(final.count())

    elif request.method == "POST":
        id = request.json.get('PID')
        data = CartItem.query.filter_by(user=current_user.id, product=id)
        if data.count() == 0:
            item = CartItem(
                user=current_user.id,
                product=id, 
                quantity= 1
            )
            db.session.add(item)
        else:
            data = data.first()
            data.quantity += 1
        
        db.session.commit()
        final = CartItem.query.filter_by(user=current_user.id)
        return str(final.count())

    elif request.method == "DELETE":
        id = request.json.get('PID')
        CartItem.query.filter_by(product=id).delete()
        db.session.commit()
        return {"res":"Success"}


