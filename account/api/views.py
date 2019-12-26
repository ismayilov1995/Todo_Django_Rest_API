from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.api.permissions import IsAnonymous
from account.api.serializers import RegisterSerializer, ChangePasswordSerializers, UserSerializer
from account.api.throttles import RegisterThrottle


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.pk)
        return obj

    # Aktual istifadeci ozunu update etsin deye
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class RegisterUser(CreateAPIView):
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymous]
    throttle_classes = [RegisterThrottle]

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        self.user = self.request.user
        serializer = ChangePasswordSerializers(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            if not self.user.check_password(old_password):
                return Response({'old_password': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
            self.user.set_password(serializer.data.get('new_password'))
            self.user.save()
            update_session_auth_hash(request, self.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)