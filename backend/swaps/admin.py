from django.contrib import admin
from .models import Message, Profile, Review, Session
admin.site.register([Profile, Session, Message, Review])
