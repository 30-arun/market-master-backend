from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserTemplate
from products.models import NewProduct


@receiver(post_save, sender=UserTemplate)
def create_products(sender, instance, created, **kwargs):
    if created:
        # Define unique data for each product
        products_data = [
            {
                "name": "Airpods Wireless Bluetooth Headphones",
                "slug": "airpods",
                "image": "products/airpods.jpg",
                "brand": "Apple",
                "description": "Bluetooth technology lets you connect it with compatible devices wirelessly High-quality AAC audio offers immersive listening experience Built-in microphone allows you to take calls while working.",
                "rating": "4.50",
                "numReviews": 12,
                "price": "89.99",
                "countinStock": 10
            },
            {
                "name": "iPhone 11 Pro 256GB Memory",
                "slug": "iphone",
                "image": "products/phone.jpg",
                "brand": "Apple",
                "description": "Introducing the iPhone 11 Pro. A transformative triple-camera system that adds tons of capability without complexity. An unprecedented leap in battery life.",
                "rating": "4.00",
                "numReviews": 8,
                "price": "599.99",
                "countinStock": 5
            },
            {
                "name": "Cannon EOS 80D DSLR Camera",
                "slug": "camera",
                "image": "products/camera.jpg",
                "brand": "Cannon",
                "description": "Characterized by versatile imaging specs, the Canon EOS 80D further clarifies itself using a pair of robust focusing systems and an intuitive design.",
                "rating": "3.00",
                "numReviews": 12,
                "price": "929.99",
                "countinStock": 5
            },
            {
                "name": "Sony Playstation 4 Pro White Version",
                "slug": "gaming",
                "image": "products/playstation.jpg",
                "brand": "Sony",
                "description": "The ultimate home entertainment center starts with PlayStation. Whether you are into gaming, HD movies, television, music.",
                "rating": "5.00",
                "numReviews": 12,
                "price": "399.99",
                "countinStock": 11
            }
        ]

        # Create a new product for each item in products_data
        for product_data in products_data:
            NewProduct.objects.create(
                user_template=instance,
                name=product_data['name'],
                description=product_data['description'],
                image=product_data['image'],
                slug=product_data['slug'],
                brand=product_data['brand'],
                rating=product_data['rating'],
                numReviews=product_data['numReviews'],
                price=product_data['price'],
                countinStock=product_data['countinStock']
            )