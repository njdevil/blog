from models import Post, Tag, Comment
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
	prepopulated_fields={"slug":("title",)}
	list_display=('id','category','date','title','viewable')

class TagAdmin(admin.ModelAdmin):
	list_display=('id','tag')

class CommentAdmin(admin.ModelAdmin):
	list_display=('id','title','date','approved')

admin.site.register(Post,PostAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Comment,CommentAdmin)
