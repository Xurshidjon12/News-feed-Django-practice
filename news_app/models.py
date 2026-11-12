from django.urls import reverse
from django.utils import timezone
from django.db import models
from .managers import PublishedManager


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    
class News(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISH = 'PB', 'Publish'

    #  idd ni ozi yozilgan boladi
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT
                              )

    objects = models.Manager() # bu yerda default manager
    published = PublishedManager() # bu yerda PublishedManager manageri ishlatiladi




    class Meta:
        ordering =["-publish_time"]

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse("news_detail", args=[self.slug])



class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.name