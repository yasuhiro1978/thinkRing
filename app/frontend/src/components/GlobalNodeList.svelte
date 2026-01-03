<script>
  import { onMount } from 'svelte';
  import { nodeApi } from '../lib/api.js';
  import NodeCreateForm from './NodeCreateForm.svelte';
  import NodeDetail from './NodeDetail.svelte';

  let globalNodes = [];
  let loading = true;
  let error = '';
  let showCreateForm = false;
  let selectedNodeId = null;

  onMount(async () => {
    await loadGlobalNodes();
  });

  async function loadGlobalNodes() {
    loading = true;
    error = '';
    try {
      const result = await nodeApi.getGlobalNodes();
      globalNodes = result;
    } catch (err) {
      error = err.message || 'グローバルノードの取得に失敗しました';
    } finally {
      loading = false;
    }
  }

  function handleNodeCreated() {
    error = ''; // エラーメッセージをクリア
    showCreateForm = false;
    loadGlobalNodes();
  }

  function handleCreateCancel() {
    error = ''; // エラーメッセージをクリア
    showCreateForm = false;
  }

  function handleNodeClick(nodeId) {
    selectedNodeId = nodeId;
  }

  function handleBackToList() {
    selectedNodeId = null;
  }

  function handleNodeUpdated() {
    loadGlobalNodes();
    selectedNodeId = null;
  }

  function handleNodeDeleted() {
    loadGlobalNodes();
    selectedNodeId = null;
  }
</script>

<div class="global-node-list">
  <div class="header">
    <h2>グローバルノード</h2>
    {#if !selectedNodeId}
      <button class="btn btn-primary" on:click={() => showCreateForm = true}>
        + グローバルノードを作成
      </button>
    {/if}
  </div>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  {#if loading}
    <p>読み込み中...</p>
  {:else if selectedNodeId}
    <NodeDetail
      nodeId={selectedNodeId}
      on:back={handleBackToList}
      on:updated={handleNodeUpdated}
      on:deleted={handleNodeDeleted}
    />
  {:else if showCreateForm}
    <NodeCreateForm
      projectId={null}
      rounds={[]}
      on:created={handleNodeCreated}
      on:cancel={handleCreateCancel}
    />
  {:else if globalNodes.length === 0}
    <p class="empty">グローバルノードがありません。作成してください。</p>
  {:else}
    <div class="nodes-grid">
      {#each globalNodes as node}
        <div class="node-card" on:click={() => handleNodeClick(node.id)}>
          <h3>{node.title}</h3>
          {#if node.context}
            <p class="context">{node.context}</p>
          {/if}
          <div class="node-meta">
            <span class="badge badge-global">グローバル</span>
            <span class="date">{new Date(node.created_at).toLocaleDateString('ja-JP')}</span>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .global-node-list {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 2rem;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  h2 {
    margin: 0;
    color: #1f2937;
    font-size: 1.5rem;
  }

  .error {
    padding: 1rem;
    margin-bottom: 1rem;
    background-color: #fee2e2;
    color: #dc2626;
    border-radius: 4px;
  }

  .empty {
    text-align: center;
    padding: 3rem;
    color: #6b7280;
  }

  .nodes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .node-card {
    padding: 1.5rem;
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .node-card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border-color: #2563eb;
  }

  .node-card h3 {
    margin: 0 0 0.5rem 0;
    color: #1f2937;
    font-size: 1.125rem;
  }

  .node-card .context {
    margin: 0.5rem 0;
    color: #6b7280;
    font-size: 0.875rem;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .node-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }

  .badge {
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
  }

  .badge-global {
    background-color: #dbeafe;
    color: #1e40af;
  }

  .date {
    color: #6b7280;
    font-size: 0.875rem;
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
</style>

