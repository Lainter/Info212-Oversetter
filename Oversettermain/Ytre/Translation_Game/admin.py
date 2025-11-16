from django.contrib import admin
from .models import Language, Tag, Word, Translation

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'language')
    list_filter = ('language', 'tags')
    search_fields = ('word',)


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('source_word', 'target_word')
    search_fields = ('source_word__word', 'target_word__word')
    list_filter = ('source_word__language', 'target_word__language')