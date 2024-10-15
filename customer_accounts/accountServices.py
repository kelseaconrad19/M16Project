from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.orm import Session
from application.database import db
from circuitbreaker import circuit
from models import CustomerAccount
from schemas import customer_account_schema

def add_customer_account(customer_account_data):
    try:
        with Session(db.engine) as session:
            # Start a new transaction block
            new_customer_account = CustomerAccount(
                username=customer_account_data['username'],
                password=customer_account_data['password'],
                customer_id=customer_account_data['customer_id']
            )
            session.add(new_customer_account)

            # Commit the changes after exiting the session block
            session.commit()

            return customer_account_schema.dump(new_customer_account), 201

    except ValidationError as e:
        return {'message': e.messages}, 400
    except Exception as e:
        print(f"Error adding customer account: {str(e)}")
        return {'message': f'Unexpected error: {str(e)}'}, 500


def view_customer_account(customer_account_id):
    try:
        with Session(db.engine) as session:
            # Query the customer account by ID
            customer_account = (
                session.query(CustomerAccount)
                .filter(CustomerAccount.id == customer_account_id)
                .one_or_none()
            )
            if customer_account is None:
                return {'message': 'Customer account not found'}, 404

            return customer_account_schema.dump(customer_account), 200
    except Exception as e:
        print(f"Error viewing customer account: {str(e)}")
        return {'message': f'An unexpected error occurred: {str(e)}'}, 500


# Update a customer account
def update_customer_account(customer_account_id, new_account_data):
    try:
        with Session(db.engine) as session:
            # Query the customer account by ID
            customer_account = session.query(CustomerAccount).filter(CustomerAccount.id == customer_account_id).first()
            if not customer_account:
                return {'message': 'Customer account not found'}, 404

            # Load new data into the customer account instance
            customer_account_data = customer_account_schema.load(new_account_data, partial=True)

            # Update fields
            customer_account.username = customer_account_data.get("username", customer_account.username)
            customer_account.password = customer_account_data.get("password", customer_account.password)
            customer_account.customer_id = customer_account_data.get("customer_id", customer_account.customer_id)

            # Commit changes
            session.commit()

            return customer_account_schema.dump(customer_account), 200
    except ValidationError as err:
        return {'message': err.messages}, 422
    except Exception as e:
        print(f"Error updating customer account: {str(e)}")
        return {'message': f'An unexpected error occurred: {str(e)}'}, 500




def delete_customer_account(customer_account_id):
    try:
        with Session(db.engine) as session:
            # Query the customer account by ID
            customer_account = session.query(CustomerAccount).filter(CustomerAccount.id == customer_account_id).first()
            if not customer_account:
                return {'message': 'Customer account not found'}, 404

            # Delete the customer account
            session.delete(customer_account)
            session.commit()

            return {'message': 'Account deleted successfully'}, 200
    except Exception as e:
        print(f"Error deleting customer account: {str(e)}")
        return {'message': f'An unexpected error occurred: {str(e)}'}, 500


