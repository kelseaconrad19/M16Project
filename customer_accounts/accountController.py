from flask import request, jsonify
from schemas import customer_account_schema, customer_accounts_schema
import customer_accounts.accountServices as accountServices
from marshmallow import ValidationError
from application.caching import cache
from application.limiter import limiter


@limiter.limit("50 per day")
def add_customer_account():
    try:
        account_data = customer_account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    account_save, status_code = accountServices.add_customer_account(account_data)
    return jsonify(account_save), status_code

@cache.cached(timeout=300)
def view_customer_account(customer_account_id):
    account_data, status_code = accountServices.view_customer_account(customer_account_id)
    return jsonify(account_data), status_code



@limiter.limit("5 per day")
def update_customer_account(customer_account_id):
    try:
        account_data = customer_account_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    updated_account, status_code = accountServices.update_customer_account(customer_account_id, account_data)
    return jsonify(updated_account), status_code


@limiter.limit("5 per day")
def delete_customer_account(customer_account_id):
    response, status_code = accountServices.delete_customer_account(customer_account_id)
    return jsonify(response), status_code

