<script>
  import { onMount } from 'svelte';
  import { nodeApi } from '../lib/api.js';
  import { createEventDispatcher } from 'svelte';
  import NodeEditForm from './NodeEditForm.svelte';
  import NodeLinkCreateForm from './NodeLinkCreateForm.svelte';

  export let nodeId;

  const dispatch = createEventDispatcher();

  let node = null;
  let loading = true;
  let error = '';
  let showEditForm = false;
  let links = { outgoing: [], incoming: [] };
  let linksLoading = false;
  let showLinkForm = false;

  onMount(async () => {
    await loadNode();
    await loadLinks();
  });

  $: if (nodeId) {
    loadNode();
    loadLinks();
  }

  async function loadNode() {
    if (!nodeId) return;
    
    loading = true;
    error = '';
    try {
      node = await nodeApi.get(nodeId);
    } catch (err) {
      error = err.message || 'ノードの取得に失敗しました';
    } finally {
      loading = false;
    }
  }

  async function loadLinks() {
    if (!nodeId) return;
    
    linksLoading = true;
    try {
      links = await nodeApi.getLinks(nodeId);
    } catch (err) {
      console.error('Failed to load links:', err);
      links = { outgoing: [], incoming: [] };
    } finally {
      linksLoading = false;
    }
  }

  function handleBack() {
    dispatch('back');
  }

  function handleEdit() {
    showEditForm = true;
  }

  function handleEditCancel() {
    showEditForm = false;
  }

  async function handleNodeUpdated() {
    showEditForm = false;
    await loadNode();
    dispatch('updated');
  }

  function handleLinkCreated() {
    showLinkForm = false;
    loadLinks();
  }

  function handleLinkCancel() {
    showLinkForm = false;
  }

  async function handleLinkDelete(linkId) {
    if (!confirm('このリンクを削除しますか？')) {
      return;
    }

    try {
      await nodeApi.deleteLink(nodeId, linkId);
      await loadLinks();
    } catch (err) {
      error = err.message || 'リンクの削除に失敗しました';
    }
  }

  function handleLinkNodeClick(targetNodeId) {
    dispatch('linkNodeClick', { nodeId: targetNodeId });
  }

  async function handleDelete() {
    if (!confirm('このノードを削除しますか？')) {
      return;
    }

    try {
      await nodeApi.delete(nodeId);
      dispatch('deleted');
    } catch (err) {
      error = err.message || 'ノードの削除に失敗しました';
    }
  }
</script>

<div class="node-detail">
  {#if loading}
    <p>読み込み中...</p>
  {:else if error}
    <div class="error">{error}</div>
    <button class="btn btn-secondary" on:click={handleBack}>戻る</button>
  {:else if node}
    <div class="header">
      <button class="btn btn-secondary" on:click={handleBack}>← 戻る</button>
      <div class="actions">
        <button class="btn btn-primary" on:click={handleEdit}>編集</button>
        <button class="btn btn-danger" on:click={handleDelete}>削除</button>
      </div>
    </div>

    {#if showEditForm}
      <NodeEditForm
        node={node}
        on:updated={handleNodeUpdated}
        on:cancel={handleEditCancel}
      />
    {:else}
      <div class="node-content">
        <div class="node-header">
          <h2>{node.title}</h2>
          <div class="node-badges">
            {#if node.is_global}
              <span class="badge badge-global">グローバル</span>
            {:else if node.project}
              <span class="badge badge-project">プロジェクトノード</span>
            {/if}
          </div>
        </div>

        {#if node.context}
          <div class="context-section">
            <h3>文脈</h3>
            <div class="context-content">{node.context}</div>
          </div>
        {/if}

        <div class="node-meta">
          <div class="meta-item">
            <span class="meta-label">作成日時:</span>
            <span class="meta-value">{new Date(node.created_at).toLocaleString('ja-JP')}</span>
          </div>
          {#if node.updated_at && node.updated_at !== node.created_at}
            <div class="meta-item">
              <span class="meta-label">更新日時:</span>
              <span class="meta-value">{new Date(node.updated_at).toLocaleString('ja-JP')}</span>
            </div>
          {/if}
          {#if node.project}
            <div class="meta-item">
              <span class="meta-label">プロジェクト:</span>
              <span class="meta-value">{node.project_title || '不明'}</span>
            </div>
          {/if}
        </div>

        <div class="links-section">
          <div class="links-header">
            <h3>ノードリンク</h3>
            <button class="btn btn-primary" on:click={() => showLinkForm = true}>リンクを追加</button>
          </div>

          {#if showLinkForm}
            <NodeLinkCreateForm
              fromNodeId={nodeId}
              on:created={handleLinkCreated}
              on:cancel={handleLinkCancel}
            />
          {/if}

          {#if linksLoading}
            <p>リンクを読み込み中...</p>
          {:else}
            <div class="links-container">
              {#if links.outgoing.length > 0}
                <div class="links-group">
                  <h4>送信リンク ({links.outgoing.length})</h4>
                  <ul class="links-list">
                    {#each links.outgoing as link}
                      <li class="link-item">
                        <span class="link-info">
                          <button
                            class="link-node-title"
                            on:click={() => handleLinkNodeClick(link.to_node_id)}
                          >
                            → {link.to_node_title || link.to_node_id}
                          </button>
                          <span class="link-weight">重み: {link.weight}</span>
                        </span>
                        <button
                          class="btn btn-danger btn-small"
                          on:click={() => handleLinkDelete(link.id)}
                        >
                          削除
                        </button>
                      </li>
                    {/each}
                  </ul>
                </div>
              {/if}

              {#if links.incoming.length > 0}
                <div class="links-group">
                  <h4>受信リンク ({links.incoming.length})</h4>
                  <ul class="links-list">
                    {#each links.incoming as link}
                      <li class="link-item">
                        <span class="link-info">
                          <button
                            class="link-node-title"
                            on:click={() => handleLinkNodeClick(link.from_node_id)}
                          >
                            ← {link.from_node_title || link.from_node_id}
                          </button>
                          <span class="link-weight">重み: {link.weight}</span>
                        </span>
                        <button
                          class="btn btn-danger btn-small"
                          on:click={() => handleLinkDelete(link.id)}
                        >
                          削除
                        </button>
                      </li>
                    {/each}
                  </ul>
                </div>
              {/if}

              {#if links.outgoing.length === 0 && links.incoming.length === 0}
                <p class="no-links">リンクがありません</p>
              {/if}
            </div>
          {/if}
        </div>
      </div>
    {/if}
  {/if}
</div>

<style>
  .node-detail {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  .actions {
    display: flex;
    gap: 0.5rem;
  }

  .error {
    padding: 1rem;
    margin-bottom: 1rem;
    background-color: #fee2e2;
    color: #dc2626;
    border-radius: 4px;
  }

  .node-content {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 2rem;
  }

  .node-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #e5e7eb;
  }

  .node-header h2 {
    margin: 0 0 0.5rem 0;
    color: #1f2937;
    font-size: 1.5rem;
  }

  .node-badges {
    display: flex;
    gap: 0.5rem;
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

  .badge-project {
    background-color: #dcfce7;
    color: #166534;
  }

  .context-section {
    margin-bottom: 2rem;
  }

  .context-section h3 {
    margin: 0 0 0.5rem 0;
    color: #374151;
    font-size: 1rem;
    font-weight: 600;
  }

  .context-content {
    padding: 1rem;
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    color: #1f2937;
    line-height: 1.6;
    white-space: pre-wrap;
  }

  .node-meta {
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }

  .meta-item {
    display: flex;
    margin-bottom: 0.5rem;
  }

  .meta-label {
    font-weight: 600;
    color: #6b7280;
    min-width: 120px;
  }

  .meta-value {
    color: #1f2937;
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

  .btn-secondary {
    background-color: #6b7280;
    color: white;
  }

  .btn-secondary:hover {
    background-color: #4b5563;
  }

  .btn-danger {
    background-color: #dc2626;
    color: white;
  }

  .btn-danger:hover {
    background-color: #b91c1c;
  }

  .btn-small {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
  }

  .links-section {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 2px solid #e5e7eb;
  }

  .links-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .links-header h3 {
    margin: 0;
    color: #1f2937;
    font-size: 1.25rem;
  }

  .links-container {
    margin-top: 1rem;
  }

  .links-group {
    margin-bottom: 1.5rem;
  }

  .links-group h4 {
    margin: 0 0 0.5rem 0;
    color: #374151;
    font-size: 1rem;
    font-weight: 600;
  }

  .links-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .link-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
  }

  .link-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex: 1;
  }

  .link-node-title {
    background: none;
    border: none;
    color: #2563eb;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 600;
    text-decoration: underline;
    padding: 0;
  }

  .link-node-title:hover {
    color: #1d4ed8;
  }

  .link-weight {
    color: #6b7280;
    font-size: 0.875rem;
  }

  .no-links {
    color: #6b7280;
    font-style: italic;
    text-align: center;
    padding: 2rem;
  }
</style>

