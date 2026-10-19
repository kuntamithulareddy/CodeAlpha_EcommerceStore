from django.core.management.base import BaseCommand
from store.models import Product

PRODUCTS = [
    {
        "name": "Everyday Backpack",
        "description": "A lightweight backpack for college, travel and daily use.",
        "price": "899.00",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80",
        "stock": 15,
    },
    {
        "name": "Wireless Headphones",
        "description": "Comfortable wireless headphones for music and online classes.",
        "price": "1499.00",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80",
        "stock": 12,
    },
    {
        "name": "Classic Wrist Watch",
        "description": "A simple everyday watch with a clean, classic design.",
        "price": "1199.00",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
        "stock": 8,
    },
    {
        "name": "Everyday Sneakers",
        "description": "Versatile sneakers designed for everyday comfort.",
        "price": "1799.00",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
        "stock": 10,
    },
    {
        "name": "Insulated Water Bottle",
        "description": "Reusable bottle for keeping water close during busy days.",
        "price": "499.00",
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=900&q=80",
        "stock": 20,
    },
    {
        "name": "Desk Lamp",
        "description": "A compact desk lamp for your study table.",
        "price": "699.00",
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80",
        "stock": 9,
    },
]

class Command(BaseCommand):
    help = "Add demo products to the store database."

    def handle(self, *args, **options):
        created = 0
        for item in PRODUCTS:
            _, was_created = Product.objects.get_or_create(
                name=item["name"],
                defaults=item,
            )
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(
            f"Seed complete. Added {created} new products; total products: {Product.objects.count()}."
        ))
