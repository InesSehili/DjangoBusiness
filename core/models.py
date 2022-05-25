from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import messages

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('p', 'primary'),
    ('s', 'secondary'),
    ('d', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"slug": self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordred = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordred = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordred=False)
    order_qs = Order.objects.filter(user=request.user, ordred=False)
    print(order_qs)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(
                request, "Quantité du Produit ajouté a éte modifier dans le panier")
            return redirect("core:product", slug=slug)

        else:
            order.items.add(order_item)
            messages.info(request, "Produit ajouté dans le panier")
            return redirect("core:product", slug=slug)
    else:
        order = Order.objects.create(
            user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        messages.info(
            request, "Quantité du Produit ajouté a éte modifier dans le panier")
        return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get(
        item=item, user=request.user, ordred=False)
    order_qs = Order.objects.filter(user=request.user, ordred=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(order_item)
            # votre product a été supprimé du panier
            messages.info(
                request, "votre product a été supprimé du panier")
            return redirect("core:product", slug=slug)
        else:
            # ce produit n'existe pas dans le panier
            messages.info(
                request, "ce produit n'existe pas dans le panier")
            return redirect("core:product", slug=slug)

    else:
        # il n'y a aucune commande pour cet utilisateur
        messages.info(
            request, "il n'y a aucune commande pour cet utilisateur")
        return redirect("core:product", slug=slug)
