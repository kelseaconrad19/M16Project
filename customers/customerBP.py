from flask import Blueprint
from customers.customerController import add_customer, update_customer, view_customer, delete_customer

customer_blueprint = Blueprint('customer_bp', __name__)

customer_blueprint.route('/', methods=['POST'])(add_customer)
customer_blueprint.route('/<int:id>', methods=['GET'])(view_customer)
customer_blueprint.route('/<int:id>', methods=['PUT'])(update_customer)
customer_blueprint.route('/<int:id>', methods=['DELETE'])(delete_customer)