from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status,generics,viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle

from inmuebleslist_app.api.serializers import ComentarioSerializer, EmpresaSerializer, EdificacionSerializer
from inmuebleslist_app.models import Comentario, Empresa, Edificacion
from inmuebleslist_app.api.permissions import IsAdminOrReadOnly, ComentarioUserOrReadOnly
from inmuebleslist_app.api.throttling import ComentarioCreateThrottle,ComentarioListThrottle

class UsuarioComentario(generics.ListAPIView):
    
    serializer_class = ComentarioSerializer
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Comentario.objects.filter( comentario_user__username = username )
    
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Comentario.objects.filter( comentario_user__username = username )

class ComentarioCreate(generics.CreateAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ComentarioCreateThrottle]
    
    def get_queryset(self):
        return Comentario.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        inmueble = Edificacion.objects.get(pk=pk)
        
        user = self.request.user
        comentario_queryset = Comentario.objects.filter(edificacion=inmueble, comentario_user = user)
        
        if comentario_queryset.exists():
            raise ValidationError("El usuario ya escribió un comentario para este inmueble")
        
        if inmueble.number_calificacion == 0:
            inmueble.avg_calificacion = serializer.validated_data['calificacion']
        else:
            inmueble.avg_calificacion = (serializer.validated_data['calificacion'] + inmueble.avg_calificacion) / 2    
                    
        inmueble.number_calificacion = inmueble.number_calificacion + 1
                    
        serializer.save(edificacion=inmueble, comentario_user = user)

class ComentarioList(generics.ListCreateAPIView):
    # queryset = Comentario.objects.all()
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle,AnonRateThrottle]
    serializer_class = ComentarioSerializer
    throttle_classes = [ComentarioListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comentario_user__username','active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comentario.objects.filter(edificacion = pk)

class EdificacionList(generics.ListAPIView):
    queryset = Edificacion.objects.all()
    serializer_class = EdificacionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['direccion','empresa__nombre']

class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [ComentarioUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    
class EmpresaVS(viewsets.ModelViewSet):
    
    permission_classes = [IsAdminOrReadOnly]
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer  
    
class EmpresaAV(APIView):
    permission_classes = [IsAdminOrReadOnly,]
    
    def get(self,request):
        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(empresas, many = True, context = {'request':request})
        return Response(serializer.data)
        
    def post(self,request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class EmpresaDetalleAV(APIView):
    permission_classes = [IsAdminOrReadOnly,]
    
    def get(self,request,pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error':'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmpresaSerializer(empresa, context={'request':request})
        return Response(serializer.data)    
    
    def put(self,request,pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error':'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = EmpresaSerializer(empresa, data=request.data, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error':'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
     
class EdificacionListAV(APIView):
    
    # Metodo GET para obtener todos los inmuebles
    def get(self,request,*args,**kwargs):
        edificacion = Edificacion.objects.all()
        serializer = EdificacionSerializer(edificacion, many=True)
        return Response(serializer.data)
    
    # Metodo POST para registrar UN inmueble
    def post(self,request,*args,**kwargs):
        serializer = EdificacionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EdificacionDetalleAV(APIView):
    
    # Metodo GET para obtener UN solo INMUEBLE por su ID
    def get(self,request,pk,*args,**kwargs):
        try:
            edificacion = Edificacion.objects.get(pk=pk)  
        except Edificacion.DoesNotExist:
            return Response({'Error':'edificacion no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EdificacionSerializer(edificacion)
        return Response(serializer.data)
    
    # Metodo PUT para actualziar UN inmuble por su ID
    def put(self,request,pk,*args,**kwargs):
        try:
            edificacion = Edificacion.objects.get(pk=pk)  
        except Edificacion.DoesNotExist:
            return Response({'Error':'edificacion no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EdificacionSerializer(edificacion, data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self,request,pk,*args,**kwargs):
        try:
            edificacion = Edificacion.objects.get(pk=pk)  
        except Edificacion.DoesNotExist:
            return Response({'Error':'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        edificacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
# class EmpresaVS(viewsets.ViewSet):
    
#     def list(self,request):
#         queryset = Empresa.objects.all()
#         serializer = EmpresaSerializer(queryset, many = True)
        
#         return Response(serializer.data)
    
#     def retrive(self, request, pk):
#         queryset = Empresa.objects.all()
#         edificacionlist = get_object_or_404(queryset,pk=pk)
#         serializer = EmpresaSerializer(edificacionlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = EmpresaSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def update(self, request, pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response({'error':'Empresa no encontrada'}, status = status.HTTP_404_NOT_FOUND)    
        
#         serializer = EmpresaSerializer(empresa, data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#     def destroy(self, request, pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response({'error':'Empresa no encontrada'}, status = status.HTTP_404_NOT_FOUND)    
        
#         empresa.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    
    
    
# class ComentarioList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self,request,*args,**kwargs):
#         return self.create(request, *args, **kwargs)

# class ComentarioDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer

#     def get(self, request, *args,**kwargs):
#         return self.retrieve(request, *args,**kwargs)
        
        
        
        
        
        
        
        
        
# @api_view(['GET','POST'])
# def inmuebles_list(request):
#     if request.method == 'GET':
#         inmuebles = Inmueble.objects.all()
#         serializer = InmuebleSerializer(inmuebles, many = True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         de_serializer = InmuebleSerializer(data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors)
        
        
# @api_view(['GET','PUT','DELETE'])
# def inmuebles_detalle(request,pk):
    # if request.method == 'GET':
    #     try:   
    #         inmueble = Inmueble.objects.get(pk=pk)
    #         serializer = InmuebleSerializer(inmueble)
    #         return Response(serializer.data) 
    #     except Inmueble.DoesNotExist:
    #         return Response({'Error': 'El inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)
        
    # if request.method == 'PUT':
    #     inmueble = Inmueble.objects.get(pk=pk)
    #     de_serializer = InmuebleSerializer( inmueble, data=request.data)
    #     if de_serializer.is_valid():
    #         de_serializer.save()
    #         return Response(de_serializer.data)
    #     else:
    #         return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # if request.method == 'DELETE':
        try:
            inmueble = Inmueble.objects.get(pk=pk)
            inmueble.delete()
        except Inmueble.DoesNotExist:
            return Response({'Error':'El inmueble no existe'},status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)