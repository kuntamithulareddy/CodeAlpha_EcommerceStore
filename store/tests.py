from django.test import TestCase
from django.urls import reverse
from .models import Product

class StoreTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="A product for testing",
            price="100.00",
            stock=5,
        )

    def test_home_page_shows_product(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_product_detail_page(self):
        response = self.client.get(reverse("product_detail", args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A product for testing")

    def test_add_to_cart_requires_post(self):
        response = self.client.get(reverse("cart_add", args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
