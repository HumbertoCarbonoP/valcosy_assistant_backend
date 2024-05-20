from django.urls import path
from .views import ValcosyAssistantOntology, ValcosyAssistantRouter, ValcosyAssistantRecomendator, ValcosyAssistantPreferences

urlpatterns = [
    path('valcosy_assistant/ontology', ValcosyAssistantOntology.as_view(), name='valcosy_assistant_ontology'),
    path('valcosy_assistant/routeFinder', ValcosyAssistantRouter.as_view(), name='valcosy_assistant_router'),
    path('valcosy_assistant/recomendator', ValcosyAssistantRecomendator.as_view(), name='valcosy_assistant_recomendator'),
    path('valcosy_assistant/preferences', ValcosyAssistantPreferences.as_view(), name='valcosy_assistant_preferences'),
]