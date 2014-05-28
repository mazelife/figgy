from django.contrib import admin

from storage.models import Book, Alias, Edition


class InlineAliasAdmin(admin.StackedInline):

    model = Alias
    extra = 0


class InlineEditionAdmin(admin.StackedInline):

    model = Edition
    extra = 0


class BookAdmin(admin.ModelAdmin):

    inlines = [InlineEditionAdmin, InlineAliasAdmin]
    list_display = ['id', 'title', 'number_of_editions']

    def number_of_editions(self, obj):
        return obj.edition_set.count()

admin.site.register(Book, BookAdmin)


