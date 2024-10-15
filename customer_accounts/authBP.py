from flask import Blueprint
from customer_accounts.authController import login

authBP = Blueprint('auth_bp', __name__)

authBP.route('/login', methods=['POST'])(login)