from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session
from application.database import db
from circuitbreaker import circuit
from models import Product
from schemas import product_schema, products_schema


def add_product(product_data):
    try:
        if product_data:
            new_product = None
            with Session(db.engine) as session:
                with session.begin():
                    new_product = Product(
                        name = product_data['name'],
                        price = product_data['price']
                    )
                    session.add(new_product)
            session.refresh(new_product)
            return new_product, 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def view_all_products():
    try:
        with Session(db.engine) as session:
            products = db.session.query(Product).all()
            return products_schema.dump(products)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def view_product(product_id):
    try:
        with Session(db.engine) as session:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product is None:
                return None
            print(product_schema.dump(product))
            return product_schema.dump(product), 200

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def update_product(product_id, product_data):
    try:
        with Session(db.engine) as session:
            # Query the product
            product = session.query(Product).filter(Product.id == product_id).first()

            # If the product is not found, return an error message
            if not product:
                return {'message': 'Product not found'}, 404

            # Manually update the fields
            if 'name' in product_data:
                product.name = product_data['name']
            if 'price' in product_data:
                product.price = product_data['price']

            # Commit the changes to the database
            session.add(product)
            session.commit()

            # Return the updated product
            return product_schema.dump(product), 200

    except ValidationError as err:
        return {'message': err.messages}, 422
    except Exception as e:
        # Print detailed error for debugging purposes
        print(f"Error updating product: {str(e)}")
        return {'message': f'An unexpected error occurred: {str(e)}'}, 500



    except Exception as e:
        print(f"Error updating product: {str(e)}")
        return {'message': f'An unexpected error occurred: {str(e)}'}, 500

        product.name = product_data['name']
        product.price = product_data['price']
        product.orders = product_data['orders']
        return product_schema.jsonify(product), 200

def delete_product(product_id):
    with Session(db.engine) as session:
        with session.begin():
            product = session.query(Product).filter(Product.id == product_id).first()
            return session.delete(product), 200