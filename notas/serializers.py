from rest_framework import serializers
from .models import Nota

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ('id', 'usuario', 'titulo', 'contenido', 'fecha_creacion', 'fecha_actualizacion')
    
    def create(self, validated_data):
        # Asigna automáticamente el usuario actual al campo de usuario
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)