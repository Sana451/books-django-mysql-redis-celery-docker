from django.contrib import admin


from .models import AdvUser, Book


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated')
    search_fields = ('username', 'email')
    fields = (
        ('username', 'email', 'register'), ('first_name', 'last_name'),
        ('send_messages', 'is_activated'),
        ('is_staff', 'is_superuser'), 'groups', 'user_permissions',
    )
    readonly_fields = ['register']


admin.site.register(AdvUser, AdvUserAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year_of_publication', 'isbn')
    fields = (('title', 'author'), 'year_of_publication', 'isbn')


admin.site.register(Book, BookAdmin)
