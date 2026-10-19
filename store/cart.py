from decimal import Decimal
from .models import Product

CART_SESSION_KEY = "cart"

def get_cart(request):
    raw_cart = request.session.get(CART_SESSION_KEY, {})
    cart = []
    total = Decimal("0.00")

    for product_id, quantity in raw_cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            quantity = max(1, int(quantity))
        except (Product.DoesNotExist, ValueError, TypeError):
            continue

        line_total = product.price * quantity
        cart.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total,
        })
        total += line_total

    return {"items": cart, "total": total}

def add_to_cart(request, product_id, quantity=1):
    product = Product.objects.get(pk=product_id)
    cart = request.session.get(CART_SESSION_KEY, {})
    current_quantity = int(cart.get(str(product_id), 0))
    new_quantity = current_quantity + int(quantity)
    if new_quantity > product.stock:
        new_quantity = product.stock
    if new_quantity > 0:
        cart[str(product_id)] = new_quantity
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

def update_cart(request, product_id, quantity):
    product = Product.objects.get(pk=product_id)
    cart = request.session.get(CART_SESSION_KEY, {})
    quantity = int(quantity)
    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = min(quantity, product.stock)
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True
