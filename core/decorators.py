import os
import jwt
from rest_framework import status
from rest_framework.response import Response


def is_authenticated(roles=[]):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            # Your custom authentication logic here based on roles.
            authorization = request.headers.get("Authorization")

            if not authorization:
                return Response({"message": "Authentication credentials are not provided", "data": None}, status=status.HTTP_401_UNAUTHORIZED)

            user = None

            try:
                user = jwt.decode(authorization, os.environ.get(
                    'JWT_SECRET'), algorithms="HS256")
            except:
                return Response({"message": "Authentication credentials are not provided", "data": None}, status=status.HTTP_401_UNAUTHORIZED)

            request.user = user

            if len(roles) == 0:
                return view_func(request, *args, **kwargs)

            user_role = user.get('role')

            if user_role != None and user_role in roles:
                # Authentication successful
                return view_func(request, *args, **kwargs)
            else:
                # Authentication failed
                response_data = {
                    'message': 'You are not allowed to access.', "data": None}
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        return wrapped_view
    return decorator
