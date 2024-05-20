from rest_framework.views import APIView
from rest_framework.response import Response
from .src.ontologia.ontologia import habitaciones_disponibles
from datetime import date
from .src.rutas.rutas import encontrar_ruta
from .src.habitaciones.habitaciones import recomendar_habitacion
from .src.gustos.gustos import run_preferences

class ValcosyAssistantOntology(APIView):
    def get(self, request):
        response = habitaciones_disponibles(date(2023, 5, 15), date(2023, 5, 18))
        return Response({'result': response})

class ValcosyAssistantRouter(APIView):
    def get(self, request):
        params = request.query_params
        final_node = int(params.get('final_node'))
        climate = params.get('climate')
        hour = params.get('hour')
        response = encontrar_ruta(final_node, climate, hour)
        return Response({'result': response})
    
class ValcosyAssistantRecomendator(APIView):
    def get(self, request):
        response = recomendar_habitacion(1, 200, 1)
        return Response({'result': response})
    
class ValcosyAssistantPreferences(APIView):
    def get(self, request):
        run_preferences()
        return Response({'result': 'Los gustos fueron calculados exitosamente...'})