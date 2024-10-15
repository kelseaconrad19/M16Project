from flask import request, jsonify
from schemas import orders_schema, order_schema
import orders.orderServices as orderServices
from marshmallow import ValidationError
from application.caching import cache
from application.limiter import limiter

@limiter.limit("50 per day")
def add_order():
    try:
        # Load the order data from the request JSON
        order_data = order_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 422

    # Add the order using the service
    new_order, status_code = orderServices.add_order(order_data)
    return jsonify(new_order), status_code


@cache.cached(timeout=300)
def view_order(id):
    order = orderServices.view_order(id)
    if order:
        return order_schema.jsonify(order), 200
    else:
        return jsonify({'message': 'order not found'}), 404