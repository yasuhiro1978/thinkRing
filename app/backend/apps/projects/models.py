import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    """プロジェクトモデル"""
    
    STATUS_CHOICES = [
        ('active', 'アクティブ'),
        ('pending', 'ペンディング'),
        ('completed', '完了'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255, verbose_name='プロジェクト名')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='状態'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    
    class Meta:
        db_table = 'projects'
        verbose_name = 'プロジェクト'
        verbose_name_plural = 'プロジェクト'
        indexes = [
            models.Index(fields=['status'], name='idx_projects_status'),
            models.Index(fields=['created_at'], name='idx_projects_created_at'),
            models.Index(fields=['user'], name='idx_projects_user'),
        ]
    
    def __str__(self):
        return self.title


class Round(models.Model):
    """周モデル（1〜5周）"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='rounds',
        verbose_name='プロジェクト'
    )
    round_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='周番号'
    )
    note = models.TextField(blank=True, null=True, verbose_name='メモ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    
    class Meta:
        db_table = 'rounds'
        verbose_name = '周'
        verbose_name_plural = '周'
        unique_together = [['project', 'round_number']]
        indexes = [
            models.Index(fields=['project'], name='idx_rounds_project_id'),
            models.Index(fields=['project', 'round_number'], name='idx_rounds_project_round'),
        ]
    
    def __str__(self):
        return f"{self.project.title} - {self.round_number}周目"


class ProcessStep(models.Model):
    """思考プロセスのステップモデル"""
    
    STEP_TYPE_CHOICES = [
        ('overview', '俯瞰'),
        ('extract', '要素抽出'),
        ('flow', '流れ構築'),
        ('mvp', '最小仕様'),
        ('expand', '拡張余地'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='process_steps',
        verbose_name='プロジェクト'
    )
    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name='process_steps',
        verbose_name='周'
    )
    step_type = models.CharField(
        max_length=20,
        choices=STEP_TYPE_CHOICES,
        verbose_name='ステップ種別'
    )
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    
    class Meta:
        db_table = 'process_steps'
        verbose_name = '思考プロセスのステップ'
        verbose_name_plural = '思考プロセスのステップ'
        unique_together = [['round', 'step_type']]
        indexes = [
            models.Index(fields=['project'], name='idx_process_steps_project_id'),
            models.Index(fields=['round'], name='idx_process_steps_round_id'),
            models.Index(fields=['round', 'step_type'], name='idx_process_steps_round_step'),
        ]
    
    def __str__(self):
        return f"{self.round} - {self.get_step_type_display()}"


class Node(models.Model):
    """ノードモデル（カード＋文脈）"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='nodes',
        null=True,
        blank=True,
        verbose_name='プロジェクト'
    )
    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name='nodes',
        null=True,
        blank=True,
        verbose_name='周'
    )
    step = models.ForeignKey(
        ProcessStep,
        on_delete=models.CASCADE,
        related_name='nodes',
        null=True,
        blank=True,
        verbose_name='ステップ'
    )
    title = models.CharField(max_length=255, verbose_name='タイトル')
    context = models.TextField(blank=True, null=True, verbose_name='文脈')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    
    class Meta:
        db_table = 'nodes'
        verbose_name = 'ノード'
        verbose_name_plural = 'ノード'
        indexes = [
            models.Index(fields=['project'], name='idx_nodes_project_id'),
            models.Index(fields=['round'], name='idx_nodes_round_id'),
            models.Index(fields=['step'], name='idx_nodes_step_id'),
            models.Index(fields=['title'], name='idx_nodes_title'),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_global(self):
        """グローバルノードかどうか"""
        return self.project is None


class NodeLink(models.Model):
    """ノード間リンクモデル"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name='outgoing_links',
        verbose_name='元ノード'
    )
    to_node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name='incoming_links',
        verbose_name='先ノード'
    )
    weight = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.5,
        validators=[MinValueValidator(0.1), MaxValueValidator(1.0)],
        verbose_name='重み'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    
    class Meta:
        db_table = 'node_links'
        verbose_name = 'ノードリンク'
        verbose_name_plural = 'ノードリンク'
        unique_together = [['from_node', 'to_node']]
        indexes = [
            models.Index(fields=['from_node'], name='idx_node_links_from_node'),
            models.Index(fields=['to_node'], name='idx_node_links_to_node'),
        ]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(from_node=models.F('to_node')),
                name='check_different_nodes'
            ),
        ]
    
    def __str__(self):
        return f"{self.from_node.title} -> {self.to_node.title}"

