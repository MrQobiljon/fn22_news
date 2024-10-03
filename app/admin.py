from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Category, Tags, News, Comment

admin.site.register(Category)
admin.site.register(Tags)


class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = News
        fields = '__all__'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('user', 'news', 'text', 'created')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'views', 'category', 'is_active', 'is_banner', 'is_weekly', 'get_image')
    list_display_links = ('pk', 'name',)
    list_editable = ('category', 'is_active', 'is_banner', 'is_weekly')
    inlines = [
        CommentInline
    ]
    form = NewsAdminForm

    def get_image(self, news):
        if news.image:
            return mark_safe(f'<img src="{news.image.url}" width="100">')
        else:
            return mark_safe(f'<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQppJKxBxJI-9UWLe2VVmzuBd24zsq4_ihxZw&s" width="100px" style="border-radius: 50%;">')

    get_image.short_description = "Rasmi"

    prepopulated_fields = {"slug": ('name',)}