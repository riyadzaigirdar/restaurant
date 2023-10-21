from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from user.serializers import UserSerializer
from core.decorators import is_authenticated

User = get_user_model()


@api_view(["POST"])
def login(request):
    user = User.objects.get(email=request.data.get("email"))

    if not user:
        return Response({"message": "that email is not registered", "data": None}, status=status.HTTP_404_NOT_FOUND)

    correct_pass = user.check_password(request.data.get("password"))

    if correct_pass:
        return Response({"message": "Successfully generated token", "data": {"token": user.create_token()}}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "password didn't match", "data": None}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@is_authenticated(['admin'])
def employee(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully created employee", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors, "data": None}, status=400)
    else:
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response({"message": "Successfully listed all users", "data": serializer.data}, status=status.HTTP_200_OK)
