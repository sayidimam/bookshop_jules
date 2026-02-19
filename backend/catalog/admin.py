from django.contrib import admin
from .models import Author, Publisher, Category, Tag, Book, BookImage

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'regular_price', 'sale_price', 'stock', 'is_active')
    search_fields = ('title', 'isbn', 'authors__name', 'publisher__name')
    list_filter = ('is_active', 'publisher', 'categories')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BookImageInline]
    filter_horizontal = ('authors', 'categories', 'tags', 'related_books')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
