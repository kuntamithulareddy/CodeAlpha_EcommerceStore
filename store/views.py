from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .cart import add_to_cart, get_cart, update_cart, CART_SESSION_KEY
from .forms import CheckoutForm
from .models import Order, OrderItem, Product

def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "store/product_detail.html", {"product": product})

def cart_view(request):
    return render(request, "store/cart.html", get_cart(request))

def cart_add(request, product_id):
    if request.method != "POST":
        return redirect("home")
    product = get_object_or_404(Product, pk=product_id)
    if product.stock < 1:
        messages.error(request, "Sorry, this product is out of stock.")
    else:
        add_to_cart(request, product.id)
        messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart")

def cart_update(request, product_id):
    if request.method != "POST":
        return redirect("cart")
    get_object_or_404(Product, pk=product_id)
    try:
        quantity = int(request.POST.get("quantity", "1"))
    except ValueError:
        quantity = 1
    update_cart(request, product_id, quantity)
    messages.success(request, "Cart updated.")
    return redirect("cart")

def cart_remove(request, product_id):
    if request.method != "POST":
        return redirect("cart")
    cart = request.session.get(CART_SESSION_KEY, {})
    cart.pop(str(product_id), None)
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True
    messages.success(request, "Product removed from cart.")
    return redirect("cart")

@login_required
def checkout(request):
    cart_data = get_cart(request)
    if not cart_data["items"]:
        messages.info(request, "Your cart is empty.")
        return redirect("home")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Re-check stock before creating the order.
                locked_products = {}
                for item in cart_data["items"]:
                    product = Product.objects.select_for_update().get(pk=item["product"].pk)
                    if item["quantity"] > product.stock:
                        messages.error(request, f"Not enough stock for {product.name}. Please update your cart.")
                        return redirect("cart")
                    locked_products[product.pk] = product

                order = Order.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data["full_name"],
                    email=form.cleaned_data["email"],
                    address=form.cleaned_data["address"],
                    city=form.cleaned_data["city"],
                    postal_code=form.cleaned_data["postal_code"],
                    total=cart_data["total"],
                )
                for item in cart_data["items"]:
                    product = locked_products[item["product"].pk]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        unit_price=product.price,
                        quantity=item["quantity"],
                    )
                    product.stock -= item["quantity"]
                    product.save(update_fields=["stock"])
            request.session[CART_SESSION_KEY] = {}
            return render(request, "store/order_success.html", {"order": order})
    else:
        form = CheckoutForm(initial={
            "full_name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        })
    return render(request, "store/checkout.html", {"form": form, **cart_data})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "store/my_orders.html", {"orders": orders})
