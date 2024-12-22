from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase, Customer


class PurchaseCreateTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.product = Product.objects.create(name="Товар 1", price=3000)
        self.product2 = Product.objects.create(name="Товар 2", price=2500)

    def test_purchase_creation(self):
        response = self.client.get(reverse('purchase_create', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введите свое имя')

    def test_successful_purchase_submission(self):
        response = self.client.post(reverse('purchase_create', kwargs={'product_id': self.product.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product.id
        })
        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.person, 'Иван')
        self.assertEqual(purchase.address, 'Москва')
        self.assertEqual(purchase.product, self.product)

        customer = Customer.objects.get(name='Иван', address='Москва')
        self.assertEqual(customer.total_spent, self.product.price)
        self.assertEqual(customer.discount, 0.0)

    def test_discount_update_after_purchase(self):
        response = self.client.post(reverse('purchase_create', kwargs={'product_id': self.product2.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product2.id
        })

        customer = Customer.objects.get(name='Иван', address='Москва')
        self.assertEqual(customer.total_spent, self.product.price + self.product2.price)
        self.assertEqual(customer.discount, 5.0)  # Скидка должна быть 5% для суммы >= 5000

    def test_multiple_purchases_and_discount_update(self):
        response1 = self.client.post(reverse('purchase_create', kwargs={'product_id': self.product.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product.id
        })
        response2 = self.client.post(reverse('purchase_create', kwargs={'product_id': self.product2.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product2.id
        })

        customer = Customer.objects.get(name='Иван', address='Москва')
        self.assertEqual(customer.discount, 5.0)

        self.assertEqual(customer.total_spent, self.product.price + self.product2.price)

    def test_discount_update_after_purchase(self):
        self.client.post(reverse('purchase_create', kwargs={'product_id': self.product.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product.id
        })

        self.client.post(reverse('purchase_create', kwargs={'product_id': self.product2.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product2.id
        })

        customer = Customer.objects.get(name='Иван', address='Москва')
        self.assertEqual(customer.total_spent, self.product.price + self.product2.price)
        self.assertEqual(customer.discount, 5.0)