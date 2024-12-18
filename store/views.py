from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Cart
from django.contrib import messages
from .forms import OrderForm

def product_list(request):
    products=Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product':product})


def add_to_cart(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    cart, created=Cart.objects.get_or_create(user=request.user)
    cart.add_item(product_id=product.id, quantity=1)
    return redirect('view_cart')
    # return render(request, 'store/product_detail.html', {'product': product})


def view_cart(request):
    cart, created=Cart.objects.get_or_create(user=request.user)
    items=[]
    total_price=0
    # total_price=cart.get_total_price()
    for product_id, quantity in cart.items.items():
        product=Product.objects.get(id=product_id)
        subtotal=product.price*quantity
        total_price+=subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'store/cart.html', {'items': items, 'total_price': total_price})




def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items:
        messages.error(request, "Cart is empty.")
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']

            total_price = sum(
                Product.objects.get(id=product_id).price * quantity
                for product_id, quantity in cart.items.items()
            )

            order = Order.objects.create(
                customer=request.user,
                full_name=full_name,
                address=address,
                phone=phone,
                email=email,
                total_price=total_price,
            )

            for product_id, quantity in cart.items.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(order=order, product=product, quantity=quantity)
                product.stock -= quantity
                product.save()

            cart.clear()
            return render(request, 'store/order_confirmation.html', {'order': order})
        else:
            # Pass the invalid form back to the template
            return render(request, 'store/checkout.html', {'cart': cart, 'form': form})
    else:
        # Initialize a blank form for a GET request
        form = OrderForm()

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


