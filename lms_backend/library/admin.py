from django.contrib import admin
from library.models import User,Book,BookRequest,Tag,UserProfile
from rest_framework.authtoken.models import Token

class BookRequestAdmin(admin.ModelAdmin):
    list_display=('id','book','user','status',)
    list_filter=('status',)
    search_fields=('user__username','book__title',)
    
    
class BookAdmin(admin.ModelAdmin):
    list_display=['book_id','title','stock','tags_list','users_requested']
    
    def book_id(self,obj):
        return obj.id
    
    book_id.short_description="Book Serial Number"
    book_id.admin_order_field = 'id' #automatic
    
    def users_requested(self,obj):
        user_requests = obj.bookrequest_set.select_related('user').all()
        
        user_count = user_requests.count()
        if user_count>0:
            usernames = ', '.join(book_reqs.user.username for book_reqs in user_requests)
            return f'{user_count}-{usernames}'
    users_requested.short_description = 'Requests by students.'
    
    def tags_list(self, obj):
        return ', '.join(tag.tag_type for tag in obj.tags.all())

    tags_list.short_description = 'Tags'  # Display name for the column

class TagAdmin(admin.ModelAdmin):
    list_display = ['id','tag_type','associated_books']   
    
    def associated_books(self, obj):
        return ', '.join(book.title for book in obj.book.all()) if obj.book.exists() else '-'
    
    associated_books.short_description = 'Relevant Books'    
 
                    
admin.site.register(User)
admin.site.register(Token)
admin.site.register(Book,BookAdmin)
admin.site.register(BookRequest,BookRequestAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(UserProfile)