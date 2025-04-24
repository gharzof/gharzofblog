from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=100)
    image = models.URLField()
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # slugify qilingan matnni 100 belgigacha qisqartiramiz
            raw_slug = slugify(self.title)[:100]
            # Unikal qilish uchun takrorlanmas slug yasaymiz
            unique_slug = raw_slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{raw_slug[:95]}-{num}"  # 100 belgidan oshmasligi uchun
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
