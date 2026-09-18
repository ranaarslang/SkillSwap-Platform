from django.urls import path
from .views import LoginView, MatchDetailView, MatchListView, MeView, MessageListView, ReviewCreateView, SessionDetailView, SessionListCreateView, SignupView

urlpatterns = [
    path("auth/signup/", SignupView.as_view()), path("auth/login/", LoginView.as_view()), path("profile/me/", MeView.as_view()),
    path("matches/", MatchListView.as_view()), path("matches/<int:pk>/", MatchDetailView.as_view()),
    path("sessions/", SessionListCreateView.as_view()), path("sessions/<int:pk>/", SessionDetailView.as_view()),
    path("reviews/", ReviewCreateView.as_view()), path("messages/", MessageListView.as_view()),
]
