from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inmuebleslist_app.api.views import * # ComentarioDetail, EmpresaAV,EdificacionListAV,EdificacionDetalleAV, EmpresaDetalleAV,ComentarioList

router = DefaultRouter()
router.register('empresa', EmpresaVS, basename='empresa')

urlpatterns = [
    path('edificacion/', EdificacionListAV.as_view(), name='edificacion_listAV'),
    path('edificacion/list/',EdificacionList.as_view(), name='edificiacion-list'),
    path('edificacion/<int:pk>',EdificacionDetalleAV.as_view(), name='edificacion-detail'),
    
    #path('empresa/', EmpresaAV.as_view(), name="empresasAV"),
    #path('empresa/<int:pk>',EmpresaDetalleAV.as_view(), name='empresa-detail'),
    
    path('',include(router.urls)),
    path('edificacion/<int:pk>/comentario-create/',ComentarioCreate.as_view(), name='comentario-create'),
    path('edificacion/<int:pk>/comentario/', ComentarioList.as_view(), name="comentario-list"),
    path('edificacion/comentario/<int:pk>/',ComentarioDetail.as_view(), name='comentario-detail'),
    # path('edificacion/comentarios/<str:username>/',UsuarioComentario.as_view(), name='usuario-comentario-detail'),
    path('edificacion/comentarios/',UsuarioComentario.as_view(), name='usuario-comentario-detail'),
]
