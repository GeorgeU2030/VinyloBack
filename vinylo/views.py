from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from music_app.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def vinylo(request):
    return Response({'message': 'This is the Backend of Vinylo :)!'})


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if user.check_password(request.data['password']):
        token, created = Token.objects.get_or_create(user=user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'avatar': user.avatar,
            'year': user.year,
            'dateInit': user.date_init,
            'currentDate': user.current_date,
        }
        return Response({'token': token.key, 'user': user_data}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({'message': 'succesfull'}, status=status.HTTP_201_CREATED)

    if 'email' in serializer.errors:
        error_msg = {"error": "Email already exists."}
        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_user(request):
    user_id = request.query_params.get('id')

    if not user_id:
        return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    user.username = data.get('username', user.username)
    user.name = data.get('name', user.name)
    user.avatar = data.get('avatar', user.avatar)
    user.date_init = data.get('dateInit', user.date_init)
    user.current_date = data.get('dateInit', user.current_date)

    user.save()
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'name': user.name,
        'avatar': user.avatar,
        'year': user.year,
        'dateInit': user.date_init,
        'currentDate': user.current_date
    }
    return Response({'message': 'User updated successfully', 'user': user_data}, status=status.HTTP_200_OK)