from django.contrib import admin
from .models import Profile, ProfileImage


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    readonly_fields = ('id',)
    list_per_page = 30
    
admin.site.register(Profile, ProfileAdmin)

class ProfileImageAdmin(admin.ModelAdmin):
    model = ProfileImage
    list_display = ('user', 'image', 'thumbnail')

    def thumbnail(self, obj):
        return '<img src="{thumb}" width="150" />'.format(thumb=obj.image.url,)
        
    thumbnail.allow_tags = True
    thumbnail.short_description = 'Image'
    
admin.site.register(ProfileImage, ProfileImageAdmin)

