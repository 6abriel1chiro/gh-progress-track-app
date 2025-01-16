from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .models import JournalEntry
from .serializers import UserSerializer, JournalEntrySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="post",
    request_body=UserSerializer,
    responses={201: UserSerializer, 400: "Bad Request"},
    operation_description="Register a new user",
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """
    Register a new user with username, email, and password
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JournalEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing journal entries.
    """

    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return entries for the currently authenticated user
        """
        return JournalEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new entry associated with the current user
        """
        serializer.save(user=self.request.user)
