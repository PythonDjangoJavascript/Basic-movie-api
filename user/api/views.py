from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user.api.serializers import UserSerializer


@api_view(['POST', ])
def user_registration_view(request):
    """Register a new user"""

    if request.method == 'POST':
        serialized_data = UserSerializer(data=request.data)

        print(request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)

        return Response({'Error': serialized_data.errors, },
                        status=status.HTTP_400_BAD_REQUEST)
