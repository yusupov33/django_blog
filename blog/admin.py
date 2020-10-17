from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ('title','slug')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hirerarchy = 'publish'
    ordering = ('status','publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('author','body')