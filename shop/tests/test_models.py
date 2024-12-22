from django.test import TestCase
from shop.models import Product, Purchase, Customer
from datetime import datetime


class CustomerModelTest(TestCase):

    def setUp(self):
        # Создаем несколько продуктов для тестирования
        self.product1 = Product.objects.create(name="Товар 1", price=3000)
        self.product2 = Product.objects.create(name="Товар 2", price=2500)

    def test_customer_creation(self):
        # Создаем клиента и проверяем его создание
        customer = Customer.objects.create(name="Иван", address="Москва")
        self.assertEqual(customer.name, "Иван")
        self.assertEqual(customer.address, "Москва")
        self.assertEqual(customer.total_spent, 0)
        self.assertEqual(customer.discount, 0.0)

    def test_update_discount_no_discount(self):
        # Создаем клиента и проверяем скидку для низкой суммы покупок
        customer = Customer.objects.create(name="Иван", address="Москва")
        self.assertEqual(customer.discount, 0.0)

    def test_update_discount_5_percent(self):
        # Проверяем скидку 5%, когда сумма покупок >= 5000
        customer = Customer.objects.create(name="Иван", address="Москва")
        customer.total_spent = 5000
        customer.update_discount()
        self.assertEqual(customer.discount, 5.0)

    def test_update_discount_10_percent(self):
        # Проверяем скидку 10%, когда сумма покупок >= 10000
        customer = Customer.objects.create(name="Иван", address="Москва")
        customer.total_spent = 10000
        customer.update_discount()
        self.assertEqual(customer.discount, 10.0)


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price="740")
        Product.objects.create(name="pencil", price="50")

    def test_correctness_types(self):                   
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, int)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, int)        

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="book").price == 740)
        self.assertTrue(Product.objects.get(name="pencil").price == 50)


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="book", price="740")
        self.datetime = datetime.now()
        Purchase.objects.create(product=self.product_book,
                                person="Ivanov",
                                address="Svetlaya St.")

    def test_correctness_types(self):
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).person, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).address, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).date, datetime)

    def test_correctness_data(self):
        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Ivanov")
        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "Svetlaya St.")
        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) == \
            self.datetime.replace(microsecond=0))