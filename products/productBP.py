from flask import Blueprint
from products.productController import add_product, view_all_products, view_product, update_product, delete_product

product_blueprint = Blueprint('product_bp', __name__)

product_blueprint.route('/', methods=['POST'])(add_product)
product_blueprint.route('/', methods=['GET'])(view_all_products)
product_blueprint.route('/<int:id>', methods=['GET'])(view_product)
product_blueprint.route('/<int:id>', methods=['PUT'])(update_product)
product_blueprint.route('/<int:id>', methods=['DELETE'])(delete_product)