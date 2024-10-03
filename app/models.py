from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Kategoriya")

    def get_newses(self):
        newses = self.news_set.order_by("-created").filter(is_active=True)
        return newses

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Tags(models.Model):
    name = models.CharField(max_length=30, verbose_name="Tag nomi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Taglar"


class News(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(max_length=255, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Matni")
    image = models.ImageField(upload_to="news/images/", null=True, blank=True, verbose_name="Rasmi")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    views = models.IntegerField(default=0, verbose_name="Ko'rishlar soni")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Maqola kategoriyasi")
    tags = models.ManyToManyField(Tags, verbose_name="Taglar")
    is_active = models.BooleanField(default=True, verbose_name="Saytga chiqarish")
    is_banner = models.BooleanField(default=False, verbose_name="Bannerga chiqarish")
    is_weekly = models.BooleanField(default=False, verbose_name="Haftalik yangilik")

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQppJKxBxJI-9UWLe2VVmzuBd24zsq4_ihxZw&s"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Yanglik"
        verbose_name_plural = "Yangiliklar"
        permissions = [
            ("can_deliver_pizzas", "Can deliver pizzas")
        ]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

