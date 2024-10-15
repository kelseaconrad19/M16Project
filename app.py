from flask import Flask, jsonify, app
from flask_swagger_ui import get_swaggerui_blueprint
from application.caching import cache
from application.limiter import limiter

from schemas import *
from models import *

from customers.customerBP import customer_blueprint
from customer_accounts.accountBP import customer_account_blueprint
from orders.orderBP import order_blueprint
from products.productBP import product_blueprint
from customer_accounts.authBP import authBP

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "eCommerce Project API"
    }
)

def create_app(config_name):
    my_app = Flask(__name__)
    my_app.config.from_object(f'application.config.{config_name}')

    cache_config = {
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300
    }
    my_app.config.update(cache_config)

    cache.init_app(my_app)
    limiter.init_app(my_app)

    my_app.register_blueprint(authBP, url_prefix='/auth')
    my_app.register_blueprint(customer_blueprint, url_prefix='/customers')
    my_app.register_blueprint(customer_account_blueprint, url_prefix='/customer_accounts')
    my_app.register_blueprint(order_blueprint, url_prefix='/orders')
    my_app.register_blueprint(product_blueprint, url_prefix='/products')
    my_app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    db.init_app(my_app)
    my_app.app_context().push()
    ma.init_app(my_app)


    return my_app, cache, limiter


if __name__ == "__main__":
    app, cache, limiter = create_app('DevelopmentConfig')

    with app.app_context():
        db.create_all()
    app.run(debug=True)