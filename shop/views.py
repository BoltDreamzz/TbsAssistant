# cart/views.py

# shop/views.py

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/homepage.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem

def get_cart(request):
    """Get the cart for the logged-in user or session."""
    if request.user.is_authenticated:
        return Cart.objects.get_or_create(user=request.user)[0]
    else:
        # Use session-based cart for anonymous users
        cart_id = request.session.get('cart_id')
        if cart_id:
            return Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
            return cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

# shop/views.py

def flash_sale_list(request):
    flash_sales = Product.objects.filter(is_flash_sale_active=True)
    return render(request, 'shop/flash_sale_list.html', {'flash_sales': flash_sales})
