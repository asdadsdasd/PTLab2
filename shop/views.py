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
        self.object = form.save()

        product = self.object.product
        person_name = self.object.person
        address = self.object.address

        customer, created = Customer.objects.get_or_create(name=person_name, address=address)

        customer.total_spent += product.price
        customer.update_discount()

        return HttpResponse(f'Спасибо за покупку, {person_name}! Ваша скидка: {customer.discount}%')

