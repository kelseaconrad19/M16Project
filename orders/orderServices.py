from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.orm import Session
from models import Order, Product, order_product
from schemas import orders_schema, order_schema
from application.database import db
from circuitbreaker import circuit
from sqlalchemy import select

def add_order(order_data):
    try:
        with Session(db.engine) as session:
            # Create a new order with the provided date and customer_id
            new_order = Order(
                date=order_data['date'],
                customer_id=order_data['customer_id']
            )

            # Add the order to the session and commit to save it to generate the order ID
            session.add(new_order)
            session.commit()  # Commit here to ensure the order ID is available

            # Add products to the order, with quantities if provided
            for product_data in order_data.get('products', []):
                product_instance = session.query(Product).filter(Product.id == product_data['id']).first()
                if product_instance:
                    quantity = product_data['quantity']
                    # Insert into the Order_Product association table
                    session.execute(order_product.insert().values(
                        order_id=new_order.id,
                        product_id=product_instance.id,
                        quantity=quantity
                    ))

            # Commit the changes to save the product associations
            session.commit()

            # Return the serialized new order
            return order_schema.dump(new_order), 201

    except IntegrityError as ie:
        print(f"Integrity Error: {str(ie)}")
        return {'message': 'The provided customer ID or product ID does not exist. Please provide valid data.'}, 400
    except ValidationError as err:
        return {'message': err.messages}, 422
    except Exception as e:
        print(f"Error adding order: {str(e)}")
        return {'message': f'An unexpected error occurred: {str(e)}'}, 500


def view_order(order_id):
    try:
        query = select(Order).filter(Order.id == order_id)
        order = db.session.execute(query).scalars().first()
        return order
    except Exception as e:
        raise e

