from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Author(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='authors/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='publishers/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    description = models.TextField(blank=True)

    # Relations
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    tags = models.ManyToManyField(Tag, blank=True, related_name='books')

    # Book Details
    isbn = models.CharField('ISBN', max_length=13, unique=True, blank=True, null=True, db_index=True)
    edition = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=50, default='Bangla') # Default to Bangla
    page_count = models.PositiveIntegerField(null=True, blank=True)

    # Pricing & Stock
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    # Meta
    is_active = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Images
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, null=True)

    # Related Books (Manual curation or fallback to algo)
    related_books = models.ManyToManyField('self', blank=True, symmetrical=False)

    # Bundle Product
    is_bundle = models.BooleanField(default=False, help_text="Is this a bundle of other books?")

    def save(self, *args, **kwargs):
        if not self.slug:
            # Append ID or random string if title exists to ensure uniqueness, but for now simple slugify
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Book.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(base_slug, num)
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='books/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_cover = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.book.title}"

class BundleItem(models.Model):
    bundle = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bundle_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='included_in_bundles')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in {self.bundle.title}"
