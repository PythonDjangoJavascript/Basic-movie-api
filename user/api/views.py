from rest_framework.authtoken.models import Token
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
            user = serialized_data.save()
            # token = Token.objects.get_or_create(user=user)
            # print(f'------------------{token}--------------')
            # print(f'------------------{token[0].key}--------------')
            data = {
                **serialized_data.data,
                'Token': Token.objects.get(user=user).key
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response({'Error': serialized_data.errors, },
                        status=status.HTTP_400_BAD_REQUEST)
