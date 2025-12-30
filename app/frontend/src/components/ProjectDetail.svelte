<script>
  import { projectApi, roundApi, nodeApi } from '../lib/api.js';
  import { onMount } from 'svelte';
  import RoundCreateForm from './RoundCreateForm.svelte';
  import StepCreateForm from './StepCreateForm.svelte';
  import NodeCreateForm from './NodeCreateForm.svelte';
  import ProjectEditForm from './ProjectEditForm.svelte';

  export let projectId;

  let project = null;
  let rounds = [];
  let nodes = [];
  let roundSteps = {}; // roundId -> steps[]
  let loading = true;
  let error = '';
  let showRoundForm = false;
  let showStepForm = false;
  let showNodeForm = false;
  let showEditForm = false;
  let selectedRoundId = null;

  onMount(async () => {
    await loadProject();
    await loadRounds();
    await loadNodes();
  });

  async function loadProject() {
    try {
      project = await projectApi.get(projectId);
    } catch (err) {
      error = err.message || 'プロジェクトの取得に失敗しました';
    } finally {
      loading = false;
    }
  }

  async function loadRounds() {
    try {
      const response = await projectApi.getRounds(projectId);
      rounds = response.results || response || [];
      // 各Roundのステップを読み込む
      for (const round of rounds) {
        await loadRoundSteps(round.id);
      }
    } catch (err) {
      console.error('Failed to load rounds:', err);
    }
  }

  async function loadRoundSteps(roundId) {
    try {
      const response = await roundApi.getSteps(roundId);
      roundSteps[roundId] = response.results || response || [];
    } catch (err) {
      console.error(`Failed to load steps for round ${roundId}:`, err);
      roundSteps[roundId] = [];
    }
  }

  async function loadNodes() {
    try {
      const response = await projectApi.getNodes(projectId);
      nodes = response.results || response || [];
    } catch (err) {
      console.error('Failed to load nodes:', err);
    }
  }

  function handleRoundCreated() {
    showRoundForm = false;
    loadRounds();
  }

  async function handleStepCreated() {
    showStepForm = false;
    const roundId = selectedRoundId;
    selectedRoundId = null;
    await loadRoundSteps(roundId);
  }

  function handleNodeCreated() {
    showNodeForm = false;
    loadNodes();
  }

  function openStepForm(roundId) {
    selectedRoundId = roundId;
    showStepForm = true;
  }

  function getStepTypeLabel(stepType) {
    const labels = {
      'overview': '俯瞰',
      'extract': '要素抽出',
      'flow': '流れ構築',
      'mvp': '最小仕様',
      'expand': '拡張余地',
    };
    return labels[stepType] || stepType;
  }

  async function handleProjectUpdated() {
    showEditForm = false;
    await loadProject();
  }
</script>

<div class="project-detail">
  {#if loading}
    <p>読み込み中...</p>
  {:else if error}
    <div class="error">{error}</div>
  {:else if project}
    <div class="project-header">
      <div class="project-title-section">
        <h2>{project.title}</h2>
        <button class="btn btn-secondary btn-sm" on:click={() => showEditForm = true}>
          編集
        </button>
      </div>
      <div class="project-meta">
        <span class="status status-{project.status}">{project.status}</span>
        <span class="date">作成日: {new Date(project.created_at).toLocaleDateString('ja-JP')}</span>
      </div>
    </div>

    {#if showEditForm}
      <ProjectEditForm
        project={project}
        on:updated={handleProjectUpdated}
        on:cancel={() => showEditForm = false}
      />
    {/if}

    <div class="sections">
      <!-- 周セクション -->
      <section class="section">
        <div class="section-header">
          <h3>周 (Rounds)</h3>
          <button class="btn btn-primary btn-sm" on:click={() => showRoundForm = true}>
            + 周を追加
          </button>
        </div>

        {#if showRoundForm}
          <RoundCreateForm
            projectId={projectId}
            on:created={handleRoundCreated}
            on:cancel={() => showRoundForm = false}
          />
        {/if}

        {#if rounds.length === 0}
          <p class="empty">周がありません</p>
        {:else}
          <div class="rounds-list">
            {#each rounds as round}
              <div class="round-item">
                <div class="round-info">
                  <h4>第{round.round_number}周</h4>
                  {#if round.note}
                    <p class="note">{round.note}</p>
                  {/if}
                  
                  <!-- ステップ一覧 -->
                  {#if roundSteps[round.id] && roundSteps[round.id].length > 0}
                    <div class="steps-list">
                      {#each roundSteps[round.id] as step}
                        <div class="step-item">
                          <span class="step-type">{getStepTypeLabel(step.step_type)}</span>
                          <p class="step-content">{step.content}</p>
                        </div>
                      {/each}
                    </div>
                  {/if}
                </div>
                <div class="round-actions">
                  <button class="btn btn-primary btn-sm" on:click={() => openStepForm(round.id)}>
                    + ステップ追加
                  </button>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- ステップ作成フォーム（周が選択されている場合） -->
      {#if showStepForm && selectedRoundId}
        <StepCreateForm
          roundId={selectedRoundId}
          on:created={handleStepCreated}
          on:cancel={() => { showStepForm = false; selectedRoundId = null; }}
        />
      {/if}

      <!-- ノードセクション -->
      <section class="section">
        <div class="section-header">
          <h3>ノード (Nodes)</h3>
          <button class="btn btn-primary btn-sm" on:click={() => showNodeForm = true}>
            + ノードを追加
          </button>
        </div>

        {#if showNodeForm}
          <NodeCreateForm
            projectId={projectId}
            rounds={rounds}
            on:created={handleNodeCreated}
            on:cancel={() => showNodeForm = false}
          />
        {/if}

        {#if nodes.length === 0}
          <p class="empty">ノードがありません</p>
        {:else}
          <div class="nodes-list">
            {#each nodes as node}
              <div class="node-item">
                <h4>{node.title}</h4>
                {#if node.context}
                  <p class="context">{node.context}</p>
                {/if}
                <div class="node-meta">
                  {#if node.is_global}
                    <span class="badge badge-global">グローバル</span>
                  {/if}
                  <span class="date">{new Date(node.created_at).toLocaleDateString('ja-JP')}</span>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </section>
    </div>
  {/if}
</div>

<style>
  .project-detail {
    max-width: 1000px;
    margin: 2rem auto;
    padding: 2rem;
  }

  .project-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #e5e7eb;
  }

  .project-title-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .project-header h2 {
    color: #1f2937;
    margin: 0;
    font-size: 1.75rem;
  }

  .project-meta {
    display: flex;
    gap: 1rem;
    align-items: center;
    font-size: 0.875rem;
    color: #6b7280;
  }

  .status {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-weight: 500;
  }

  .status-active {
    background-color: #d1fae5;
    color: #065f46;
  }

  .status-pending {
    background-color: #fef3c7;
    color: #92400e;
  }

  .status-completed {
    background-color: #dbeafe;
    color: #1e40af;
  }

  .sections {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .section {
    background-color: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .section-header h3 {
    color: #1f2937;
    margin: 0;
    font-size: 1.25rem;
  }

  .rounds-list,
  .nodes-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .round-item,
  .node-item {
    padding: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    background-color: #f9fafb;
  }

  .round-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
  
  .round-info {
    flex: 1;
  }
  
  .round-info h4 {
    margin: 0 0 0.5rem 0;
    color: #1f2937;
  }
  
  .note {
    margin: 0 0 1rem 0;
    color: #6b7280;
    font-size: 0.875rem;
  }

  .steps-list {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .step-item {
    padding: 0.75rem;
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
  }

  .step-type {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background-color: #dbeafe;
    color: #1e40af;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  .step-content {
    margin: 0;
    color: #4b5563;
    font-size: 0.875rem;
    white-space: pre-wrap;
  }

  .node-item h4 {
    margin: 0 0 0.5rem 0;
    color: #1f2937;
  }

  .context {
    margin: 0.5rem 0;
    color: #4b5563;
    font-size: 0.875rem;
  }

  .node-meta {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-top: 0.5rem;
    font-size: 0.75rem;
    color: #6b7280;
  }

  .badge {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-weight: 500;
  }

  .badge-global {
    background-color: #dbeafe;
    color: #1e40af;
  }

  .btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 600;
  }

  .btn-primary {
    background-color: #2563eb;
    color: white;
  }

  .btn-primary:hover {
    background-color: #1d4ed8;
  }

  .btn-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
  }

  .empty {
    color: #6b7280;
    font-style: italic;
    text-align: center;
    padding: 2rem;
  }

  .error {
    padding: 1rem;
    background-color: #fee2e2;
    color: #dc2626;
    border-radius: 4px;
  }
</style>

