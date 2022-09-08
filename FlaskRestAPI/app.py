from ast import parse
from distutils import core
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from models import ProductModel, db
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

class ProductsView(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('name',
    #     type=str,
    #     required=True,
    #     help = "Can't leave blank"
    # )
    # parser.add_argument('price',
    #     type=float,
    #     required=True,
    #     help="Can't leave blank"
    # )
    # parser.add_argument('brand',
    #     type=str,
    #     required=True,
    #     help="Can't leave blank"
    # )/
    def get(self):
        products = ProductModel.query.all()
        return {'Products':list(x.json() for x in products)}
    def post(self):
        data = request.get_json()
        new_product = ProductModel(data['name'],data['description'], data['price'], data['brand'])
        db.session.add(new_product)
        db.session.commit()
        db.session.flush()
        #print(db.id)
        return new_product.json(),201

class SingleProductView(Resource):
    def get(self, id):
        product = ProductModel.query.filter_by(id=id).first()
        if product:
            return product.json()
        return {'message':'Product id not found'},404
    def delete(self, id):
        product = ProductModel.query.filter_by(id=id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'Product not found'},404
    def put(self, id):
        data = request.get_json()
        product = ProductModel.query.filter_by(id=id).first()
        if product:
            product.name = data['name']
            product.price = data['price']
            product.description = data['description']
            product.brand = data['brand']
        else:
            product = ProductModel(id=id,**data)

        db.session.add(product)
        db.session.commit()
        return product.json()
    
api.add_resource(ProductsView, '/products')
api.add_resource(SingleProductView, '/product/<int:id>')

app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=5000)