from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserAdminSerializer
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated



class UserAdminListView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        users = CustomUser.objects.all().order_by('id')
        serializer = UserAdminSerializer(users, many=True)
        return Response(serializer.data)


class UserAdminToggleBlockView(APIView):
    # permission_classes = [IsAuthenticated]
    def toggle_block(self, user):
        user.is_blocked = not user.is_blocked
        user.save()

    def patch(self, request, id):
        user = self.get_user(id)
        self.toggle_block(user)
        serializer = UserAdminSerializer(user)
        return Response(serializer.data)

    def get_user(self, id):
        return CustomUser.objects.get(id=id)
