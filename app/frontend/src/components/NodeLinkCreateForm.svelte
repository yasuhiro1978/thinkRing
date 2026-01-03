<script>
  import { onMount } from 'svelte';
  import { nodeApi } from '../lib/api.js';
  import { createEventDispatcher } from 'svelte';

  export let fromNodeId;

  const dispatch = createEventDispatcher();

  let toNodeId = '';
  let weight = 0.5;
  let availableNodes = [];
  let loading = false;
  let error = '';
  let existingLinks = [];

  onMount(async () => {
    await loadAvailableNodes();
    await loadExistingLinks();
  });

  async function loadAvailableNodes() {
    try {
      // グローバルノードとプロジェクトノードの両方を取得
      // 現在のノードを除外する必要があるので、後でフィルタリング
      const globalNodes = await nodeApi.getGlobalNodes();
      // TODO: プロジェクトノードも取得する必要があるが、現在のAPIでは取得できない
      // とりあえずグローバルノードのみを使用
      availableNodes = globalNodes.filter(node => node.id !== fromNodeId);
    } catch (err) {
      error = err.message || 'ノード一覧の取得に失敗しました';
    }
  }

  async function loadExistingLinks() {
    try {
      const linksData = await nodeApi.getLinks(fromNodeId);
      existingLinks = [...linksData.outgoing, ...linksData.incoming];
    } catch (err) {
      console.error('Failed to load existing links:', err);
    }
  }

  function isLinkExists(targetNodeId) {
    return existingLinks.some(link => 
      (link.from_node_id === fromNodeId && link.to_node_id === targetNodeId) ||
      (link.from_node_id === targetNodeId && link.to_node_id === fromNodeId)
    );
  }

  async function handleSubmit() {
    error = '';

    if (!toNodeId) {
      error = 'リンク先ノードを選択してください';
      return;
    }

    if (toNodeId === fromNodeId) {
      error = '自分自身へのリンクは作成できません';
      return;
    }

    if (isLinkExists(toNodeId)) {
      error = 'このノードへのリンクは既に存在します';
      return;
    }

    if (weight < 0.1 || weight > 1.0) {
      error = '重みは0.1〜1.0の範囲で入力してください';
      return;
    }

    loading = true;
    try {
      await nodeApi.createLink(fromNodeId, toNodeId, weight);
      dispatch('created');
    } catch (err) {
      error = err.message || 'リンクの作成に失敗しました';
    } finally {
      loading = false;
    }
  }

  function handleCancel() {
    dispatch('cancel');
  }
</script>

<div class="link-create-form">
  <h3>リンクを作成</h3>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  <form on:submit|preventDefault={handleSubmit}>
    <div class="form-group">
      <label for="toNodeId">リンク先ノード</label>
      <select id="toNodeId" bind:value={toNodeId} required>
        <option value="">選択してください</option>
        {#each availableNodes as node}
          <option value={node.id}>{node.title} {#if node.is_global}(グローバル){/if}</option>
        {/each}
      </select>
    </div>

    <div class="form-group">
      <label for="weight">重み (0.1〜1.0)</label>
      <input
        id="weight"
        type="number"
        min="0.1"
        max="1.0"
        step="0.1"
        bind:value={weight}
        required
      />
    </div>

    <div class="form-actions">
      <button type="submit" class="btn btn-primary" disabled={loading}>
        {loading ? '作成中...' : '作成'}
      </button>
      <button type="button" class="btn btn-secondary" on:click={handleCancel}>
        キャンセル
      </button>
    </div>
  </form>
</div>

<style>
  .link-create-form {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
  }

  .link-create-form h3 {
    margin: 0 0 1rem 0;
    color: #1f2937;
    font-size: 1.125rem;
  }

  .error {
    padding: 0.75rem;
    margin-bottom: 1rem;
    background-color: #fee2e2;
    color: #dc2626;
    border-radius: 4px;
    font-size: 0.875rem;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #374151;
    font-weight: 600;
    font-size: 0.875rem;
  }

  .form-group select,
  .form-group input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 0.875rem;
  }

  .form-group select:focus,
  .form-group input:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }

  .form-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1.5rem;
  }

  .btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 600;
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-primary {
    background-color: #2563eb;
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    background-color: #1d4ed8;
  }

  .btn-secondary {
    background-color: #6b7280;
    color: white;
  }

  .btn-secondary:hover {
    background-color: #4b5563;
  }
</style>

