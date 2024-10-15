import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from application.database import db
from products.productBP import product_blueprint
from models import Product

class ProductRoutesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a test instance of the Flask app
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
        cls.app.register_blueprint(product_blueprint, url_prefix='/products')

        # Set up the test client
        cls.client = cls.app.test_client()

        # Set up the database for testing
        with cls.app.app_context():
            db.init_app(cls.app)
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Clean up after all tests
        with cls.app.app_context():
            db.drop_all()

    @patch('products.productServices.add_product')
    def test_add_product_success(self, mock_add_product):
        # Mock the add_product service to simulate a successful addition
        mock_add_product.return_value = Product(id=1, name="Widget A", price=19.99)

        response = self.client.post('/products/', json={
            "name": "Widget A",
            "price": 19.99
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Widget A')
        self.assertEqual(response.json['price'], 19.99)

    @patch('products.productServices.view_all_products')
    def test_view_all_products_success(self, mock_view_all_products):
        # Mock the view_all_products service to simulate returning multiple products
        mock_view_all_products.return_value = [
            Product(id=1, name="Widget A", price=19.99),
            Product(id=2, name="Widget B", price=29.99)
        ]

        response = self.client.get('/products/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['name'], 'Widget A')
        self.assertEqual(response.json[1]['name'], 'Widget B')

    @patch('products.productServices.view_product')
    def test_view_product_by_id_success(self, mock_view_product):
        # Mock the view_product service to simulate fetching a specific product
        mock_view_product.return_value = Product(id=1, name="Widget A", price=19.99)

        response = self.client.get('/products/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Widget A')
        self.assertEqual(response.json['price'], 19.99)

if __name__ == '__main__':
    unittest.main()
