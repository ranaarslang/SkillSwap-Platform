from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    skills_offered = models.JSONField(default=list)
    skills_wanted = models.JSONField(default=list)
    portfolio_links = models.JSONField(default=list)
    is_verified = models.BooleanField(default=False)
    avatar_color = models.CharField(max_length=20, default="#f2b84b")
    availability = models.CharField(max_length=100, default="Weeknights")

class Session(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("accepted", "Accepted"), ("completed", "Completed"), ("declined", "Declined")]
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requested_sessions")
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_sessions")
    title = models.CharField(max_length=160)
    scheduled_for = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name="review")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
