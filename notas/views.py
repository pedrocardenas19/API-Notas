from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Nota
from .serializers import NotaSerializer

class RegistroView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        # Obtener los datos enviados por el usuario
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return Response({'message': 'El nombre de usuario ya está en uso'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear un nuevo usuario
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Almacenar la contraseña en forma de hash
        )
        
        # Devolver una respuesta exitosa
        return Response({'message': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Autenticación exitosa'})
        else:
            return Response({'message': 'Credenciales inválidas'}, status=401)

class NotaLista(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notas = Nota.objects.filter(usuario=request.user)
        serializer = NotaSerializer(notas, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Crear una nueva instancia de Nota con el usuario actual
        nueva_nota = Nota(usuario=request.user)
        
        # Inicializar el serializer con la nueva instancia de Nota y los datos de la solicitud
        serializer = NotaSerializer(nueva_nota, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class NotaDetalle(APIView):
    permission_classes = [IsAuthenticated]

    def get_nota(self, pk):
        try:
            return Nota.objects.get(pk=pk, usuario=self.request.user)
        except Nota.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        nota = self.get_nota(pk)
        serializer = NotaSerializer(nota)
        return Response(serializer.data)

    def put(self, request, pk):
        nota = self.get_nota(pk)
        serializer = NotaSerializer(nota, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        nota = self.get_nota(pk)
        nota.delete()
        return Response(status=204)
