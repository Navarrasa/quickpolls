from django.contrib import admin
from .models import CustomUser, Poll, Option, Vote

"""
Admin configuration for the QuickPolls application.
This file registers the models with the Django admin site, allowing them to be managed through the admin interface.
"""

admin.site.register(CustomUser)
admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Vote)

admin.site.site_header = "QuickPolls Admin"
admin.site.site_title = "QuickPolls Admin Portal"
admin.site.index_title = "Welcome to QuickPolls Admin Portal"
