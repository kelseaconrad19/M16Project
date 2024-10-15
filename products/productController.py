from flask import request, jsonify
from schemas import product_schema, products_schema
import products.productServices as productServices
from marshmallow import ValidationError
from application.caching import cache
from application.limiter import limiter

def add_product():
    try:
        product_data = product_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 422
    product_save = productServices.add_product(product_data)
    if product_save:
        return jsonify(product_schema.dump(product_save)), 201
    else:
        return jsonify({'message': 'error'}), 400

def view_all_products():
    products = productServices.view_all_products()
    if products:
        return jsonify(products_schema.dump(products)), 200  # Use products_schema to serialize
    else:
        return jsonify({'message': 'No products found'}), 404


def view_product(id):
    product = productServices.view_product(id)
    if product:
        return jsonify(product_schema.dump(product)), 200  # Use product_schema to serialize
    else:
        return jsonify({'message': 'No product found'}), 404


def update_product(id):
    try:
        product_data = product_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    updated_product, status_code = productServices.update_product(id, product_data)

    return jsonify(updated_product), status_code

def delete_product(id):
    product = productServices.delete_product(id)
    if product:
        return jsonify({'message': 'product deleted'}), 200
    else:
        return jsonify({'message': 'product not found'}), 404
