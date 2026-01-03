from rest_framework import serializers
from .models import Project, Round, ProcessStep, Node, NodeLink


class ProjectSerializer(serializers.ModelSerializer):
    """プロジェクトシリアライザー"""
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoundSerializer(serializers.ModelSerializer):
    """周シリアライザー"""
    
    project_id = serializers.UUIDField(source='project.id', read_only=True)
    
    class Meta:
        model = Round
        fields = ['id', 'project_id', 'round_number', 'note', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        """周作成時にプロジェクトを設定"""
        project = self.context['project']
        validated_data['project'] = project
        return super().create(validated_data)


class ProcessStepSerializer(serializers.ModelSerializer):
    """思考プロセスのステップシリアライザー"""
    
    round_id = serializers.UUIDField(source='round.id', read_only=True)
    project_id = serializers.UUIDField(source='project.id', read_only=True)
    step_type_number = serializers.SerializerMethodField()
    
    class Meta:
        model = ProcessStep
        fields = ['id', 'project_id', 'round_id', 'step_type', 'step_type_number', 'content', 'created_at']
        read_only_fields = ['id', 'created_at', 'step_type_number']
    
    def get_step_type_number(self, obj):
        """ステップ種別の番号を返す（1〜5）"""
        step_type_order = {
            'overview': 1,
            'extract': 2,
            'flow': 3,
            'mvp': 4,
            'expand': 5,
        }
        return step_type_order.get(obj.step_type, 0)
    
    def create(self, validated_data):
        """ステップ作成時にプロジェクトと周を設定"""
        round = self.context['round']
        validated_data['round'] = round
        validated_data['project'] = round.project
        return super().create(validated_data)


class NodeSerializer(serializers.ModelSerializer):
    """ノードシリアライザー"""
    
    project_id = serializers.UUIDField(source='project.id', read_only=True, allow_null=True)
    round_id = serializers.UUIDField(source='round.id', read_only=True, allow_null=True)
    step_id = serializers.UUIDField(source='step.id', read_only=True, allow_null=True)
    is_global = serializers.BooleanField(read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True, allow_null=True)
    
    class Meta:
        model = Node
        fields = [
            'id', 'project_id', 'round_id', 'step_id',
            'title', 'context', 'is_global', 'project_title',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """ノード作成時にプロジェクト、周、ステップを設定（オプション）"""
        # リクエストデータから取得
        project_id = self.initial_data.get('project_id')
        round_id = self.initial_data.get('round_id')
        step_id = self.initial_data.get('step_id')
        
        if project_id:
            try:
                validated_data['project'] = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise serializers.ValidationError({'project_id': 'Project not found'})
        
        if round_id:
            try:
                validated_data['round'] = Round.objects.get(id=round_id)
                # roundが指定されている場合、projectも自動設定
                if 'project' not in validated_data:
                    validated_data['project'] = validated_data['round'].project
            except Round.DoesNotExist:
                raise serializers.ValidationError({'round_id': 'Round not found'})
        
        if step_id:
            try:
                validated_data['step'] = ProcessStep.objects.get(id=step_id)
                # stepが指定されている場合、roundとprojectも自動設定
                if 'round' not in validated_data:
                    validated_data['round'] = validated_data['step'].round
                if 'project' not in validated_data:
                    validated_data['project'] = validated_data['step'].project
            except ProcessStep.DoesNotExist:
                raise serializers.ValidationError({'step_id': 'ProcessStep not found'})
        
        return super().create(validated_data)


class NodeLinkSerializer(serializers.ModelSerializer):
    """ノードリンクシリアライザー"""
    
    from_node_id = serializers.UUIDField(source='from_node.id', read_only=True)
    to_node_id = serializers.UUIDField(source='to_node.id', read_only=True)
    from_node_title = serializers.CharField(source='from_node.title', read_only=True)
    to_node_title = serializers.CharField(source='to_node.title', read_only=True)
    
    class Meta:
        model = NodeLink
        fields = ['id', 'from_node_id', 'to_node_id', 'from_node_title', 'to_node_title', 'weight', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        """ノードリンク作成時に元ノードを設定"""
        from_node = self.context['from_node']
        validated_data['from_node'] = from_node
        return super().create(validated_data)

