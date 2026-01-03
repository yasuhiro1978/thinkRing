<script>
  import { projectApi, roundApi, nodeApi } from '../lib/api.js';
  import { onMount } from 'svelte';
  import RoundCreateForm from './RoundCreateForm.svelte';
  import RoundEditForm from './RoundEditForm.svelte';
  import StepCreateForm from './StepCreateForm.svelte';
  import NodeCreateForm from './NodeCreateForm.svelte';
  import ProjectEditForm from './ProjectEditForm.svelte';
  import NodeDetail from './NodeDetail.svelte';
  import RoundSummary from './RoundSummary.svelte';
  import WordTree from './WordTree.svelte';

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
  let selectedNodeId = null;
  let showRoundSummary = false;
  let summaryRound = null;
  let showRoundEditForm = false;
  let editingRound = null;
  let showWordTree = false;

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

  function handleNodeBack() {
    selectedNodeId = null;
  }

  function handleNodeUpdated() {
    loadNodes();
    selectedNodeId = null;
  }

  function handleNodeDeleted() {
    loadNodes();
    selectedNodeId = null;
  }

  function handleLinkNodeClick(event) {
    const { nodeId } = event.detail;
    selectedNodeId = nodeId;
  }

  function openStepForm(roundId) {
    selectedRoundId = roundId;
    showStepForm = true;
  }

  function getStepTypeLabel(stepType, stepTypeNumber) {
    const labels = {
      'overview': '俯瞰',
      'extract': '要素抽出',
      'flow': '流れ構築',
      'mvp': '最小仕様',
      'expand': '拡張余地',
    };
    const label = labels[stepType] || stepType;
    // 番号が提供されている場合は番号付きで返す
    if (stepTypeNumber) {
      return `${stepTypeNumber}. ${label}`;
    }
    return label;
  }

  async function handleProjectUpdated() {
    showEditForm = false;
    await loadProject();
  }

  // Phase 5.2: 周カウンター表示（最大周番号を使用）
  $: currentRoundNumber = rounds.length > 0 ? Math.max(...rounds.map(r => r.round_number)) : 0;

  // Phase 5.5: 周のまとめ画面
  function openRoundSummary(round) {
    summaryRound = round;
    showRoundSummary = true;
  }

  function handleSummaryClose() {
    showRoundSummary = false;
    summaryRound = null;
  }

  function handleNextRoundFromSummary() {
    showRoundSummary = false;
    summaryRound = null;
    showRoundForm = true; // 次の周の作成フォームを開く
  }

  function handleCompleteFromSummary() {
    // TODO: プロジェクトを完了状態にするAPI呼び出し
    console.log('プロジェクトを完了します');
    showRoundSummary = false;
    summaryRound = null;
  }

  function handlePendingFromSummary() {
    // TODO: プロジェクトをペンディング状態にするAPI呼び出し
    console.log('プロジェクトをペンディングにします');
    showRoundSummary = false;
    summaryRound = null;
  }

  // Phase 5.1: 周の編集機能
  function openRoundEdit(round) {
    editingRound = round;
    showRoundEditForm = true;
  }

  async function handleRoundUpdated() {
    showRoundEditForm = false;
    editingRound = null;
    await loadRounds();
  }

  function handleRoundEditCancel() {
    showRoundEditForm = false;
    editingRound = null;
  }
</script>

<div class="project-detail">
  {#if loading}
    <p>読み込み中...</p>
  {:else if error}
    <div class="error">{error}</div>
  {:else if selectedNodeId}
    <NodeDetail
      nodeId={selectedNodeId}
      on:back={handleNodeBack}
      on:updated={handleNodeUpdated}
      on:deleted={handleNodeDeleted}
      on:linkNodeClick={handleLinkNodeClick}
    />
  {:else if showRoundSummary && summaryRound}
    <RoundSummary
      round={summaryRound}
      roundNumber={summaryRound.round_number}
      steps={roundSteps[summaryRound.id] || []}
      nodes={nodes.filter(n => n.round_id === summaryRound.id)}
      on:close={handleSummaryClose}
      on:nextRound={handleNextRoundFromSummary}
      on:complete={handleCompleteFromSummary}
      on:pending={handlePendingFromSummary}
    />
  {:else if showWordTree}
    <div class="word-tree-section">
      <div class="section-header">
        <h2>ワードツリー</h2>
        <button class="btn btn-secondary btn-sm" on:click={() => showWordTree = false}>
          戻る
        </button>
      </div>
      <WordTree
        projectId={projectId}
        on:nodeClick={(e) => {
          selectedNodeId = e.detail.nodeId;
          showWordTree = false;
        }}
      />
    </div>
  {:else if project}
    <div class="project-header">
      <div class="project-title-section">
        <h2>{project.title}</h2>
        {#if currentRoundNumber > 0}
          <div class="round-counter">
            <span class="round-counter-label">周カウンター:</span>
            <span class="round-counter-value">第{currentRoundNumber}周 / 5周</span>
          </div>
        {/if}
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
          <button class="btn btn-primary btn-sm" on:click={() => {
            showRoundForm = true;
          }}>
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
            {#each rounds as round, index}
              <div class="round-item">
                <div class="round-info">
                  <h4>第{round.round_number}周</h4>
                  {#if round.note}
                    <p class="note">{round.note}</p>
                  {/if}
                  
                  <!-- 前周の内容を表示（2周目以降） -->
                  {#if round.round_number > 1 && index > 0}
                    {@const previousRound = rounds[index - 1]}
                    {#if previousRound && roundSteps[previousRound.id] && roundSteps[previousRound.id].length > 0}
                      <div class="previous-round-content">
                        <h5>前周（第{previousRound.round_number}周）の内容</h5>
                        <div class="previous-steps">
                          {#each roundSteps[previousRound.id] as prevStep}
                            <div class="previous-step-item">
                              <span class="previous-step-type">{getStepTypeLabel(prevStep.step_type, prevStep.step_type_number)}</span>
                              <p class="previous-step-content">{prevStep.content}</p>
                            </div>
                          {/each}
                        </div>
                      </div>
                    {/if}
                  {/if}
                  
                  <!-- ステップ一覧 -->
                  {#if roundSteps[round.id] && roundSteps[round.id].length > 0}
                    <div class="steps-list">
                      {#each roundSteps[round.id] as step}
                        <div class="step-item">
                          <div class="step-header">
                            {#if step.step_type_number}
                              <span class="step-type-number">{step.step_type_number}</span>
                            {/if}
                            <span class="step-type">{getStepTypeLabel(step.step_type, step.step_type_number)}</span>
                          </div>
                          <p class="step-content">{step.content}</p>
                        </div>
                      {/each}
                    </div>
                  {:else if roundSteps[round.id] !== undefined}
                    <p class="empty">ステップがありません</p>
                  {/if}
                </div>
                <div class="round-actions">
                  <button class="btn btn-primary btn-sm" on:click={() => {
                    openStepForm(round.id);
                  }}>
                    + ステップ追加
                  </button>
                  <button class="btn btn-secondary btn-sm" on:click={() => openRoundEdit(round)}>
                    編集
                  </button>
                  <button class="btn btn-secondary btn-sm" on:click={() => openRoundSummary(round)}>
                    まとめ
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
          existingSteps={roundSteps[selectedRoundId] || []}
          on:created={handleStepCreated}
          on:cancel={() => { showStepForm = false; selectedRoundId = null; }}
        />
      {/if}

      <!-- 周編集フォーム（Phase 5.1） -->
      {#if showRoundEditForm && editingRound}
        <RoundEditForm
          round={editingRound}
          on:updated={handleRoundUpdated}
          on:cancel={handleRoundEditCancel}
        />
      {/if}

      <!-- ノードセクション -->
      <section class="section">
        <div class="section-header">
          <h3>ノード (Nodes)</h3>
          <div class="section-actions">
            <button class="btn btn-secondary btn-sm" on:click={() => showWordTree = true}>
              ワードツリー
            </button>
            <button class="btn btn-primary btn-sm" on:click={() => {
              showNodeForm = true;
            }}>
              + ノードを追加
            </button>
          </div>
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
              <div class="node-item" style="cursor: pointer;" on:click={() => selectedNodeId = node.id}>
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
    position: relative;
    z-index: 1;
  }

  .project-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid rgba(0, 217, 255, 0.3);
  }

  .project-title-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .project-header h2 {
    color: #00d9ff;
    margin: 0;
    font-size: 1.75rem;
    text-shadow: 
      0 0 10px rgba(0, 217, 255, 0.8),
      0 0 20px rgba(0, 217, 255, 0.4);
    font-weight: 700;
    letter-spacing: 1px;
  }

  .round-counter {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(0, 217, 255, 0.2);
    border: 1px solid rgba(0, 217, 255, 0.4);
    border-radius: 8px;
    font-weight: 600;
    box-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
  }

  .round-counter-label {
    color: #00d9ff;
    font-size: 0.875rem;
  }

  .round-counter-value {
    color: #00d9ff;
    font-size: 1rem;
    text-shadow: 0 0 5px rgba(0, 217, 255, 0.5);
  }

  .project-meta {
    display: flex;
    gap: 1rem;
    align-items: center;
    font-size: 0.875rem;
    color: #8b9dc3;
  }

  .status {
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .status-active {
    background: rgba(0, 217, 255, 0.2);
    color: #00d9ff;
    border: 1px solid rgba(0, 217, 255, 0.4);
    box-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
  }

  .status-pending {
    background: rgba(255, 165, 0, 0.2);
    color: #ffa500;
    border: 1px solid rgba(255, 165, 0, 0.4);
    box-shadow: 0 0 10px rgba(255, 165, 0, 0.3);
  }

  .status-completed {
    background: rgba(0, 255, 0, 0.2);
    color: #00ff00;
    border: 1px solid rgba(0, 255, 0, 0.4);
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
  }

  .sections {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .section {
    background: rgba(10, 14, 39, 0.7);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border: 2px solid rgba(0, 217, 255, 0.3);
    border-radius: 12px;
    box-shadow: 
      0 0 30px rgba(0, 217, 255, 0.4),
      inset 0 0 20px rgba(0, 217, 255, 0.1);
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .section-header h3 {
    color: #00d9ff;
    margin: 0;
    font-size: 1.25rem;
    text-shadow: 0 0 5px rgba(0, 217, 255, 0.5);
    font-weight: 700;
  }

  .section-actions {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .word-tree-section {
    padding: 1rem;
  }

  .word-tree-section .section-header {
    margin-bottom: 1rem;
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
    border: 1px solid rgba(0, 217, 255, 0.3);
    border-radius: 8px;
    background: rgba(26, 31, 58, 0.6);
    transition: all 0.3s ease;
  }

  .round-item:hover,
  .node-item:hover {
    border-color: #00d9ff;
    box-shadow: 0 0 15px rgba(0, 217, 255, 0.4);
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
    color: #e0e0e0;
    font-weight: 600;
    text-shadow: 0 0 5px rgba(0, 217, 255, 0.3);
  }
  
  .note {
    margin: 0 0 1rem 0;
    color: #8b9dc3;
    font-size: 0.875rem;
  }

  .previous-round-content {
    margin-top: 1rem;
    padding: 1rem;
    background: rgba(26, 31, 58, 0.6);
    border: 1px solid rgba(0, 217, 255, 0.2);
    border-radius: 6px;
    border-left: 4px solid rgba(139, 157, 195, 0.6);
  }

  .previous-round-content h5 {
    margin: 0 0 0.75rem 0;
    color: #8b9dc3;
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .previous-steps {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .previous-step-item {
    padding: 0.5rem;
    background: rgba(26, 31, 58, 0.8);
    border: 1px solid rgba(0, 217, 255, 0.2);
    border-radius: 6px;
  }

  .previous-step-type {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background: rgba(139, 157, 195, 0.2);
    color: #8b9dc3;
    border: 1px solid rgba(139, 157, 195, 0.3);
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .previous-step-content {
    margin: 0.25rem 0 0 0;
    color: #e0e0e0;
    font-size: 0.875rem;
    white-space: pre-wrap;
  }

  .steps-list {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .step-item {
    padding: 0.75rem;
    background: rgba(26, 31, 58, 0.8);
    border: 1px solid rgba(0, 217, 255, 0.2);
    border-radius: 6px;
    border-left: 4px solid #00d9ff;
    transition: all 0.3s ease;
  }

  .step-item:hover {
    border-color: #00d9ff;
    box-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
  }

  .step-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .step-type-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
    color: #0a0e27;
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
    box-shadow: 0 0 10px rgba(0, 217, 255, 0.5);
  }

  .step-type {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background: rgba(0, 217, 255, 0.2);
    color: #00d9ff;
    border: 1px solid rgba(0, 217, 255, 0.4);
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    box-shadow: 0 0 5px rgba(0, 217, 255, 0.3);
  }

  .step-content {
    margin: 0;
    color: #e0e0e0;
    font-size: 0.875rem;
    white-space: pre-wrap;
  }

  .node-item h4 {
    margin: 0 0 0.5rem 0;
    color: #e0e0e0;
    font-weight: 600;
    text-shadow: 0 0 5px rgba(0, 217, 255, 0.3);
  }

  .context {
    margin: 0.5rem 0;
    color: #8b9dc3;
    font-size: 0.875rem;
  }

  .node-meta {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-top: 0.5rem;
    font-size: 0.75rem;
    color: #8b9dc3;
  }

  .badge {
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .badge-global {
    background: rgba(0, 217, 255, 0.2);
    color: #00d9ff;
    border: 1px solid rgba(0, 217, 255, 0.4);
    box-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
  }

  .btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 600;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .btn-primary {
    background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
    color: #0a0e27;
    border: 1px solid #00d9ff;
    box-shadow: 0 0 10px rgba(0, 217, 255, 0.4);
  }

  .btn-primary:hover {
    background: linear-gradient(135deg, #00ffff 0%, #00d9ff 100%);
    box-shadow: 
      0 0 20px rgba(0, 217, 255, 0.6),
      0 0 30px rgba(0, 217, 255, 0.3);
    transform: translateY(-2px);
  }

  .btn-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
  }

  .empty {
    color: #8b9dc3;
    font-style: italic;
    text-align: center;
    padding: 2rem;
  }

  .error {
    padding: 1rem;
    background: rgba(255, 0, 128, 0.2);
    color: #ff0080;
    border: 1px solid #ff0080;
    border-radius: 6px;
    box-shadow: 0 0 15px rgba(255, 0, 128, 0.3);
    text-shadow: 0 0 5px rgba(255, 0, 128, 0.5);
  }
</style>

