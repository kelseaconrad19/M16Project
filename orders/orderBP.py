from flask import Blueprint

from orders.orderController import add_order, view_order

order_blueprint = Blueprint('order_bp', __name__)

order_blueprint.route('/', methods=['POST'])(add_order)
order_blueprint.route('/<int:id>', methods=['GET'])(view_order)