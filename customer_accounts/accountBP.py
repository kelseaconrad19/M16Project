from flask import Blueprint
from customer_accounts.accountController import add_customer_account, update_customer_account, view_customer_account, delete_customer_account

customer_account_blueprint = Blueprint('customer_account_bp', __name__)

customer_account_blueprint.route('/', methods=['POST'])(add_customer_account)
customer_account_blueprint.route('/<int:customer_account_id>', methods=['PUT'])(update_customer_account)
customer_account_blueprint.route('/<int:customer_account_id>', methods=['GET'])(view_customer_account)
customer_account_blueprint.route('/<int:customer_account_id>', methods=['DELETE'])(delete_customer_account)