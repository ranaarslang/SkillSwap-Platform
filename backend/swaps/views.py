from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .matcher import calculate_matches
from .models import Message, Profile, Review, Session
from .serializers import MessageSerializer, ProfileSerializer, ReviewSerializer, SessionSerializer, UserSerializer

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        data = request.data
        if User.objects.filter(username=data.get("username")).exists():
            return Response({"detail": "Username already exists."}, status=400)
        user = User.objects.create_user(username=data["username"], password=data["password"], first_name=data.get("first_name", ""), last_name=data.get("last_name", ""))
        Profile.objects.create(user=user, bio=data.get("bio", ""), skills_offered=data.get("skills_offered", []), skills_wanted=data.get("skills_wanted", []), portfolio_links=data.get("portfolio_links", []))
        return Response({"token": Token.objects.create(user=user).key, "user": UserSerializer(user).data}, status=201)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if not user: return Response({"detail": "Invalid credentials."}, status=401)
        return Response({"token": Token.objects.get_or_create(user=user)[0].key, "user": UserSerializer(user).data})

class MeView(APIView):
    def get(self, request): return Response(ProfileSerializer(request.user.profile).data)
    def put(self, request):
        serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True); serializer.save(); return Response(serializer.data)

class MatchListView(APIView):
    def get(self, request):
        matches = calculate_matches(request.user, Profile.objects.select_related("user").all())
        return Response([{**ProfileSerializer(item["profile"]).data, "match_score": item["score"]} for item in matches])

class MatchDetailView(APIView):
    def get(self, request, pk):
        profile = generics.get_object_or_404(Profile.objects.select_related("user"), user_id=pk)
        match = next((item for item in calculate_matches(request.user, [profile]) if item["profile"].pk == profile.pk), None)
        if match is None:
            return Response({"detail": "Match not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({**ProfileSerializer(profile).data, "match_score": match["score"]})

class SessionListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    def get_queryset(self): return Session.objects.filter(Q(requester=self.request.user) | Q(partner=self.request.user)).select_related("requester", "partner")
    def perform_create(self, serializer): serializer.save(requester=self.request.user, partner_id=self.request.data["partner"])

class SessionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Session.objects.all(); serializer_class = SessionSerializer

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    def perform_create(self, serializer): serializer.save(reviewer=self.request.user)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    def get_queryset(self):
        peer = self.request.query_params.get("peer")
        return Message.objects.filter(Q(sender=self.request.user, recipient_id=peer) | Q(sender_id=peer, recipient=self.request.user)).order_by("created_at")
