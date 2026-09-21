from django.contrib import admin

from .models import Cart, CartItem, Movie, Screening, Snack


class ScreeningInline(admin.TabularInline):
    model = Screening
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_minutes', 'classification', 'is_active')
    list_filter = ('is_active', 'classification')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    inlines = (ScreeningInline,)


@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ('movie', 'starts_at', 'auditorium', 'format', 'language')
    list_filter = ('auditorium', 'format', 'language')
    search_fields = ('movie__title',)


@admin.register(Snack)
class SnackAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


admin.site.register(Cart)
admin.site.register(CartItem)
