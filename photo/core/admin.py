from django.contrib import admin
from .models import profile
from .models import upload,LikePost,FollowersCount,saved

# Register your models here.

admin.site.register(profile)
admin.site.register(upload)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(saved)