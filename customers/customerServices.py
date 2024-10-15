from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.orm import Session
from schemas import customer_schema
from application.database import db
from models import Customer
from circuitbreaker import circuit
from sqlalchemy import select


@circuit(failure_threshold=5)
def add_customer(customer_data):
    try:
        if customer_data["name"] == "Failure":
            raise Exception("Failure condition triggered.")
        with Session(db.engine) as session:
            with session.begin():
                new_customer = Customer(
                    name=customer_data["name"],
                    email=customer_data["email"],
                    phone=customer_data["phone"],
                    orders=customer_data["orders"]
                )
                session.add(new_customer)
                session.flush()
                session.refresh(new_customer)
            return new_customer, 201
    except Exception as e:
        raise e

def view_customer(customer_id):
    try:
        with Session(db.engine) as session:
            query = select(Customer).where(Customer.id == customer_id)
            customer = db.session.execute(query).scalars().first()
        return customer
    except Exception as e:
        raise e

def update_customer(customer_id, new_customer_data):
    with Session(db.engine) as session:
        with session.begin():
            customer = session.query(Customer).get(customer_id)
            try:
                customer_data = customer_schema.load(new_customer_data)
                customer.name = customer_data["name"]
                customer.email = customer_data["email"]
                customer.phone = customer_data["phone"]
                customer.orders = customer_data["orders"]
                updated_customer = customer_schema.dump(customer)
                session.commit()
                return updated_customer, 200
            except ValidationError as err:
                return err.messages, 400




def delete_customer(customer_id):
    with Session(db.engine) as session:
        with session.begin():
            customer = session.query(Customer).get(customer_id)
            return session.delete(customer), 200


