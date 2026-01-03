from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import Project, Round, ProcessStep, Node, NodeLink
from .serializers import (
    ProjectSerializer,
    RoundSerializer,
    ProcessStepSerializer,
    NodeSerializer,
    NodeLinkSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """プロジェクトViewSet"""
    
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """現在のユーザーのプロジェクトのみ取得"""
        return Project.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """プロジェクト作成時にユーザーを設定"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get', 'post'])
    def rounds(self, request, pk=None):
        """プロジェクトの周一覧を取得、または周を作成"""
        project = self.get_object()
        
        if request.method == 'GET':
            rounds = Round.objects.filter(project=project).order_by('round_number')
            serializer = RoundSerializer(rounds, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = RoundSerializer(
                data=request.data,
                context={'project': project, 'request': request}
            )
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    # 一意制約違反の場合（同じプロジェクトで同じ周番号）
                    if 'round_number' in str(e) or 'unique' in str(e).lower():
                        return Response(
                            {
                                'error': {
                                    'code': 'DUPLICATE_ROUND',
                                    'message': f'このプロジェクトには既に第{serializer.validated_data.get("round_number", "")}周が存在します。各プロジェクトでは各周番号を1つまでしか作成できません。',
                                    'type': 'IntegrityError'
                                }
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    # その他のIntegrityError
                    return Response(
                        {
                            'error': {
                                'code': 'INTEGRITY_ERROR',
                                'message': 'データの整合性エラーが発生しました。',
                                'type': 'IntegrityError'
                            }
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def nodes(self, request, pk=None):
        """プロジェクトのノード一覧を取得"""
        project = self.get_object()
        nodes = Node.objects.filter(project=project).order_by('-created_at')
        serializer = NodeSerializer(nodes, many=True)
        return Response(serializer.data)


class RoundViewSet(viewsets.ModelViewSet):
    """周ViewSet"""
    
    serializer_class = RoundSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """現在のユーザーのプロジェクトに属する周のみ取得"""
        return Round.objects.filter(
            project__user=self.request.user
        ).order_by('project', 'round_number')
    
    def perform_update(self, serializer):
        """周の更新処理（Phase 5.1）"""
        serializer.save()
    
    @action(detail=True, methods=['get', 'post'])
    def steps(self, request, pk=None):
        """周のステップ一覧を取得、またはステップを作成"""
        round_obj = self.get_object()
        
        if request.method == 'GET':
            steps = ProcessStep.objects.filter(round=round_obj)
            # ステップ種別の順序でソート（1. 俯瞰、2. 要素抽出、3. 流れ構築、4. 最小仕様、5. 拡張余地）
            step_type_order = {
                'overview': 1,
                'extract': 2,
                'flow': 3,
                'mvp': 4,
                'expand': 5,
            }
            steps_list = list(steps)
            steps_list.sort(key=lambda s: step_type_order.get(s.step_type, 99))
            serializer = ProcessStepSerializer(steps_list, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = ProcessStepSerializer(
                data=request.data,
                context={'round': round_obj, 'request': request}
            )
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    # 一意制約違反の場合
                    if 'step_type' in str(e) or 'unique' in str(e).lower():
                        step_type = serializer.validated_data.get('step_type', '')
                        # ステップタイプの日本語ラベルを取得
                        step_type_label = dict(ProcessStep.STEP_TYPE_CHOICES).get(step_type, step_type)
                        return Response(
                            {
                                'error': {
                                    'code': 'DUPLICATE_STEP',
                                    'message': f'この周には既に「{step_type_label}」ステップが存在します。各周では各ステップタイプを1つまでしか作成できません。',
                                    'type': 'IntegrityError'
                                }
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    # その他のIntegrityError
                    return Response(
                        {
                            'error': {
                                'code': 'INTEGRITY_ERROR',
                                'message': 'データの整合性エラーが発生しました。',
                                'type': 'IntegrityError'
                            }
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProcessStepViewSet(viewsets.ReadOnlyModelViewSet):
    """思考プロセスのステップViewSet（読み取り専用）"""
    
    serializer_class = ProcessStepSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """現在のユーザーのプロジェクトに属するステップのみ取得"""
        return ProcessStep.objects.filter(
            project__user=self.request.user
        ).order_by('round', 'step_type')


class NodeViewSet(viewsets.ModelViewSet):
    """ノードViewSet"""
    
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """現在のユーザーのプロジェクトに属するノード、またはグローバルノードを取得"""
        # グローバルノード（project=None）も含める
        return Node.objects.filter(
            project__user=self.request.user
        ) | Node.objects.filter(project__isnull=True)
    
    @action(detail=False, methods=['get'])
    def global_nodes(self, request):
        """グローバルノード一覧を取得"""
        nodes = Node.objects.filter(project__isnull=True).order_by('-created_at')
        serializer = self.get_serializer(nodes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get', 'post', 'delete'])
    def links(self, request, pk=None):
        """ノードのリンク一覧を取得、リンクを作成、またはリンクを削除"""
        node = self.get_object()
        
        if request.method == 'GET':
            # リンク一覧を取得
            outgoing_links = NodeLink.objects.filter(from_node=node)
            incoming_links = NodeLink.objects.filter(to_node=node)
            
            outgoing_data = NodeLinkSerializer(outgoing_links, many=True).data
            incoming_data = NodeLinkSerializer(incoming_links, many=True).data
            
            return Response({
                'outgoing': outgoing_data,
                'incoming': incoming_data
            })
        
        elif request.method == 'POST':
            # リンクを作成
            serializer = NodeLinkSerializer(
                data=request.data,
                context={'from_node': node, 'request': request}
            )
            if serializer.is_valid():
                # to_node_idを取得
                to_node_id = request.data.get('to_node_id')
                if not to_node_id:
                    return Response(
                        {'error': 'to_node_id is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    to_node = Node.objects.get(id=to_node_id)
                except Node.DoesNotExist:
                    return Response(
                        {'error': 'to_node not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                serializer.save(to_node=to_node)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            # リンクを削除
            import json
            # DELETEリクエストのbodyを直接読み取る
            try:
                if request.body:
                    body_data = json.loads(request.body.decode('utf-8'))
                    link_id = body_data.get('link_id')
                else:
                    link_id = None
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                return Response(
                    {'error': 'Invalid JSON in request body'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not link_id:
                return Response(
                    {'error': 'link_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                link = NodeLink.objects.get(id=link_id)
                # このノードが送信元または送信先であることを確認
                if link.from_node != node and link.to_node != node:
                    return Response(
                        {'error': 'Link does not belong to this node'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                link.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except NodeLink.DoesNotExist:
                return Response(
                    {'error': 'Link not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {'error': f'Internal server error: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                return Response(
                    {'error': 'Link not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
