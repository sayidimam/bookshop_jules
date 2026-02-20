from django.contrib import admin
from .models import Review, ReviewImage, Question, Answer, UserCollection, CollectionItem

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase')
    search_fields = ('book__title', 'user__phone_number')
    inlines = [ReviewImageInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'book', 'user', 'is_approved')
    list_filter = ('is_approved',)
    inlines = [AnswerInline]

class CollectionItemInline(admin.TabularInline):
    model = CollectionItem
    extra = 1

@admin.register(UserCollection)
class UserCollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_public', 'created_at')
    inlines = [CollectionItemInline]
