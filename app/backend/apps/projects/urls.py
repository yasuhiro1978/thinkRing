from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    RoundViewSet,
    ProcessStepViewSet,
    NodeViewSet
)

# プロジェクト用のルーター
project_router = DefaultRouter()
project_router.register(r'', ProjectViewSet, basename='project')

# 周用のルーター
round_router = DefaultRouter()
round_router.register(r'', RoundViewSet, basename='round')

# ステップ用のルーター
step_router = DefaultRouter()
step_router.register(r'', ProcessStepViewSet, basename='step')

# ノード用のルーター
node_router = DefaultRouter()
node_router.register(r'', NodeViewSet, basename='node')

# プロジェクト用のURL（/projects/ でアクセス）
urlpatterns = [
    path('', include(project_router.urls)),
]

# 周用のURL（/rounds/ でアクセス）
round_urlpatterns = [
    path('', include(round_router.urls)),
]

# ステップ用のURL（/steps/ でアクセス）
step_urlpatterns = [
    path('', include(step_router.urls)),
]

# ノード用のURL（/nodes/ でアクセス）
node_urlpatterns = [
    path('', include(node_router.urls)),
]
