from rest_framework import serializers

from inmuebleslist_app.models import Comentario, Edificacion, Empresa

class ComentarioSerializer(serializers.ModelSerializer):
    comentario_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Comentario
        fields = '__all__'
            

class EdificacionSerializer(serializers.ModelSerializer):
    
    comentarios = ComentarioSerializer(many=True, read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre')
    
    class Meta:
        model = Edificacion
        fields = '__all__'
        # fields = ['id','pais','active','imagen']
        # exclude = ['id']
            
class EmpresaSerializer(serializers.ModelSerializer):
    
    edificacionlist = EdificacionSerializer(many = True, read_only = True)
    # edificacionlist = serializers.StringRelatedField(many = True)
    # edificacionlist = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    # edificacionlist = serializers.HyperlinkedRelatedField(
    #     many = True, 
    #     read_only = True,
    #     view_name = 'edificacion-detail'
    #     )
    
    class Meta:
        fields = '__all__'
        model = Empresa            
            

    