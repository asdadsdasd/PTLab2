from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase, Customer


class PurchaseCreateTestCase(TestCase):

    def setUp(self):
        # Создаем клиента для тестирования
        self.client = Client()
        # Создаем тестовые данные: продукт и покупатель
        self.product = Product.objects.create(name="Товар 1", price=3000)
        self.product2 = Product.objects.create(name="Товар 2", price=2500)

    def test_purchase_creation(self):
        # Тестируем доступность страницы создания покупки
        response = self.client.get(reverse('purchase_create', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введите свое имя')

    def test_successful_purchase_submission(self):
        # Тестируем успешную отправку формы и создание покупки
        response = self.client.post(reverse('purchase_create', kwargs={'product_id': self.product.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product.id
        })
        # Проверяем, что покупка создана
        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.person, 'Иван')
        self.assertEqual(purchase.address, 'Москва')
        self.assertEqual(purchase.product, self.product)

        # Проверяем, что покупатель был создан или обновлен
        customer = Customer.objects.get(name='Иван', address='Москва')
        self.assertEqual(customer.total_spent, self.product.price)
        self.assertEqual(customer.discount, 0.0)  # Скидка должна быть 0.0 для этой суммы

    def test_discount_update_after_purchase(self):
        # Проверяем обновление скидки после покупки
        response = self.client.post(reverse('purchase_create', kwargs={'product_id': self.product2.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product2.id
        })

        # Проверяем, что покупатель получил скидку 5%
        customer = Customer.objects.get(name='Иван', address='Москва')
        self.assertEqual(customer.total_spent, self.product.price + self.product2.price)
        self.assertEqual(customer.discount, 5.0)  # Скидка должна быть 5% для суммы >= 5000

    def test_multiple_purchases_and_discount_update(self):
        # Проверяем, что скидка обновляется после нескольких покупок
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

        # Проверяем, что скидка обновляется на 5%
        customer = Customer.objects.get(name='Иван', address='Москва')
        self.assertEqual(customer.discount, 5.0)  # Скидка должна быть 5% после второй покупки

        # Проверяем, что покупатель потратил правильную сумму
        self.assertEqual(customer.total_spent, self.product.price + self.product2.price)

    def test_discount_update_after_purchase(self):
        # Совершаем первую покупку
        self.client.post(reverse('purchase_create', kwargs={'product_id': self.product.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product.id
        })

        # Совершаем вторую покупку
        self.client.post(reverse('purchase_create', kwargs={'product_id': self.product2.id}), {
            'person': 'Иван',
            'address': 'Москва',
            'product': self.product2.id
        })

        # Проверяем данные покупателя
        customer = Customer.objects.get(name='Иван', address='Москва')
        self.assertEqual(customer.total_spent, self.product.price + self.product2.price)
        self.assertEqual(customer.discount, 5.0)  # Скидка должна быть 5% для суммы >= 5000