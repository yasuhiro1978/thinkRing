from django.urls import path, include
from apps.projects.urls import (
    round_urlpatterns,
    step_urlpatterns,
    node_urlpatterns
)

urlpatterns = [
    path('auth/', include('apps.auth.urls')),
    path('projects/', include('apps.projects.urls')),  # /projects/ エンドポイント
    path('rounds/', include(round_urlpatterns)),  # /rounds/ エンドポイント
    path('steps/', include(step_urlpatterns)),  # /steps/ エンドポイント
    path('nodes/', include(node_urlpatterns)),  # /nodes/ エンドポイント
]

