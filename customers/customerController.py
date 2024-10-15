from flask import request, jsonify
from schemas import customer_schema, customers_schema
import customers.customerServices as customerServices
from marshmallow import ValidationError
from application.caching import cache
from application.limiter import limiter
from application.decorators import token_required, admin_required

@admin_required
def add_customer():
    try:
        customer_data = customer_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 422
    customer_save = customerServices.add_customer(customer_data)
    if customer_save:
        return jsonify(customer_schema.dump(customer_save)), 201
    else:
        return jsonify({'message': 'Fallback method error activated', 'body': customer_data}), 400

@token_required
@cache.cached(timeout=300)
def view_customer(id):
    customer = customerServices.view_customer(id)
    if customer:
        return customer_schema.jsonify(customer), 200
    else:
        return {"error": "Customer not found"}, 404

@admin_required
def update_customer(id):
    customer_data = customer_schema.load(request.get_json())
    customer, status_code = customerServices.update_customer(id, customer_data)
    return jsonify(customer), status_code

@admin_required
@limiter.limit("1 per day")
def delete_customer(id):
    customer = customerServices.delete_customer(id)
    if customer:
        return jsonify(customer_schema.dump(customer)), 200
    else:
        return {"error": "Customer not found"}, 404