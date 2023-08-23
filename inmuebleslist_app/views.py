# from django.http import JsonResponse

# from inmuebleslist_app.models import Inmueble

# def inmuebles_list(request):
#     inmuebles = Inmueble.objects.all()
#     data = {
#         'inmuebles' : list(inmuebles.values())
#     }
    
#     return JsonResponse(data)

# def inmuebles_detalle(request,pk):
#     inmueble = Inmueble.objects.get(pk=pk)
#     data = {
#         'direccion' : inmueble.direccion,
#         'pais' : inmueble.pais,
#         'descripcion' : inmueble.descripcion,
#         'imagen' : inmueble.imagen,
#         'active' : inmueble.active
#     }
    
#     return JsonResponse(data)