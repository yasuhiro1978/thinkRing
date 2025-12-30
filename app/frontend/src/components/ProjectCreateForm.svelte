<script>
  import { projectApi } from '../lib/api.js';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let title = '';
  let status = 'active';
  let loading = false;
  let error = '';

  const statusOptions = [
    { value: 'active', label: 'アクティブ' },
    { value: 'pending', label: 'ペンディング' },
    { value: 'completed', label: '完了' },
  ];

  async function handleSubmit() {
    if (!title.trim()) {
      error = 'プロジェクト名を入力してください';
      return;
    }

    loading = true;
    error = '';

    try {
      const result = await projectApi.create(title, status);
      dispatch('created');
      // フォームをリセット
      title = '';
      status = 'active';
    } catch (err) {
      error = err.message || 'プロジェクトの作成に失敗しました';
    } finally {
      loading = false;
    }
  }

  function handleCancel() {
    dispatch('cancel');
  }
</script>

<div class="project-create-form">
  <h2>新しいプロジェクトを作成</h2>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  <form on:submit|preventDefault={handleSubmit}>
    <div class="form-group">
      <label for="title">プロジェクト名 *</label>
      <input
        type="text"
        id="title"
        bind:value={title}
        placeholder="プロジェクト名を入力"
        required
        disabled={loading}
      />
    </div>

    <div class="form-group">
      <label for="status">ステータス</label>
      <select id="status" bind:value={status} disabled={loading}>
        {#each statusOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
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
  .project-create-form {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  }

  h2 {
    color: #1f2937;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #374151;
    font-weight: 600;
    font-size: 0.875rem;
  }

  input[type="text"],
  select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 1rem;
    box-sizing: border-box;
  }

  input:focus,
  select:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }

  input:disabled,
  select:disabled {
    background-color: #f3f4f6;
    cursor: not-allowed;
  }

  .form-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
    margin-top: 2rem;
  }

  .btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 600;
    transition: background-color 0.2s;
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
    padding: 0.75rem;
    margin-bottom: 1rem;
    background-color: #fee2e2;
    color: #dc2626;
    border-radius: 4px;
    font-size: 0.875rem;
  }
</style>

