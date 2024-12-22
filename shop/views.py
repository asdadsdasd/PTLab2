from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product, Purchase, Customer

from .models import Product, Purchase

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        # Сохраняем покупку, но не отправляем ответ
        self.object = form.save()

        # Получаем продукт и данные из формы
        product = self.object.product  # Получаем продукт из формы
        person_name = self.object.person  # Имя покупателя из формы
        address = self.object.address  # Адрес покупателя из формы

        # Проверяем, есть ли покупатель с таким именем и адресом, если нет, создаем нового
        customer, created = Customer.objects.get_or_create(name=person_name, address=address)

        # Обновляем данные покупателя
        customer.total_spent += product.price
        customer.update_discount()

        # Возвращаем сообщение с благодарностью
        return HttpResponse(f'Спасибо за покупку, {person_name}! Ваша скидка: {customer.discount}%')

