from django.db import models
from django.conf import settings
from catalog.models import Book
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', db_index=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', db_index=True)

    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], db_index=True)
    text = models.TextField(blank=True)

    is_verified_purchase = models.BooleanField(default=False, db_index=True)
    likes_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}* by {self.user.phone_number} on {self.book.title}"

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='reviews/')

    def __str__(self):
        return f"Image for Review {self.review.id}"

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.text[:50]}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()

    is_official = models.BooleanField(default=False, help_text="Answer by Admin/Author")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A: {self.text[:50]}"

class UserCollection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.phone_number}"

class CollectionItem(models.Model):
    collection = models.ForeignKey(UserCollection, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('collection', 'book')
