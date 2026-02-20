from django.contrib import admin
from .models import Author, Publisher, Category, Tag, Book, BookImage, BundleItem

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1

class BundleItemInline(admin.TabularInline):
    model = BundleItem
    extra = 1
    fk_name = 'bundle'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'regular_price', 'sale_price', 'stock', 'is_active', 'is_bundle')
    search_fields = ('title', 'isbn', 'authors__name', 'publisher__name')
    list_filter = ('is_active', 'is_bundle', 'publisher', 'categories')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BookImageInline, BundleItemInline]
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
