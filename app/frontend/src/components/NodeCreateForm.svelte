<script>
  import { nodeApi } from '../lib/api.js';
  import { createEventDispatcher } from 'svelte';

  export let projectId;
  export let rounds = [];

  const dispatch = createEventDispatcher();

  let title = '';
  let context = '';
  let selectedRoundId = '';
  let isGlobal = false;
  let loading = false;
  let error = '';

  async function handleSubmit() {
    if (!title.trim()) {
      error = 'タイトルを入力してください';
      return;
    }

    loading = true;
    error = '';

    try {
      const data = {
        title,
        context: context || null,
      };

      if (isGlobal) {
        // グローバルノード（project, round, stepはnull）
        data.project_id = null;
        data.round_id = null;
        data.step_id = null;
      } else {
        // プロジェクトに紐づくノード
        data.project_id = projectId;
        if (selectedRoundId) {
          data.round_id = selectedRoundId;
        }
      }

      await nodeApi.create(data);
      dispatch('created');
      title = '';
      context = '';
      selectedRoundId = '';
      isGlobal = false;
    } catch (err) {
      error = err.message || 'ノードの作成に失敗しました';
    } finally {
      loading = false;
    }
  }

  function handleCancel() {
    dispatch('cancel');
  }
</script>

<div class="node-create-form">
  <h4>新しいノードを作成</h4>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  <form on:submit|preventDefault={handleSubmit}>
    <div class="form-group">
      <label>
        <input
          type="checkbox"
          bind:checked={isGlobal}
          disabled={loading}
        />
        グローバルノード（全プロジェクトで共有）
      </label>
    </div>

    {#if !isGlobal && rounds.length > 0}
      <div class="form-group">
        <label for="roundId">周（任意）</label>
        <select id="roundId" bind:value={selectedRoundId} disabled={loading}>
          <option value="">選択しない</option>
          {#each rounds as round}
            <option value={round.id}>第{round.round_number}周</option>
          {/each}
        </select>
      </div>
    {/if}

    <div class="form-group">
      <label for="title">タイトル *</label>
      <input
        type="text"
        id="title"
        bind:value={title}
        placeholder="ノードのタイトルを入力"
        required
        disabled={loading}
      />
    </div>

    <div class="form-group">
      <label for="context">文脈</label>
      <textarea
        id="context"
        bind:value={context}
        rows="4"
        placeholder="ノードの文脈を入力（任意）"
        disabled={loading}
      ></textarea>
    </div>

    <div class="form-actions">
      <button type="submit" class="btn btn-primary" disabled={loading}>
        {#if loading}
          作成中...
        {:else}
          作成
        {/if}
      </button>
      <button type="button" class="btn btn-secondary" on:click={handleCancel} disabled={loading}>
        キャンセル
      </button>
    </div>
  </form>
</div>

<style>
  .node-create-form {
    margin: 1rem 0;
    padding: 1rem;
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
  }

  h4 {
    margin: 0 0 1rem 0;
    color: #1f2937;
    font-size: 1rem;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #374151;
    font-weight: 600;
    font-size: 0.875rem;
  }

  label input[type="checkbox"] {
    margin-right: 0.5rem;
  }

  input[type="text"],
  select,
  textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 0.875rem;
    box-sizing: border-box;
    font-family: inherit;
  }

  input:focus,
  select:focus,
  textarea:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }

  input:disabled,
  select:disabled,
  textarea:disabled {
    background-color: #f3f4f6;
    cursor: not-allowed;
  }

  .form-actions {
    display: flex;
    gap: 0.5rem;
    justify-content: flex-end;
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
    opacity: 0.6;
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

  .btn-secondary:hover:not(:disabled) {
    background-color: #4b5563;
  }

  .error {
    padding: 0.5rem;
    margin-bottom: 1rem;
    background-color: #fee2e2;
    color: #dc2626;
    border-radius: 4px;
    font-size: 0.875rem;
  }
</style>

