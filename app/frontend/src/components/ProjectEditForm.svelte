<script>
  import { projectApi } from '../lib/api.js';
  import { createEventDispatcher } from 'svelte';

  export let project;

  const dispatch = createEventDispatcher();

  let title = project.title;
  let status = project.status;
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
      await projectApi.update(project.id, { title, status });
      dispatch('updated');
    } catch (err) {
      error = err.message || 'プロジェクトの更新に失敗しました';
    } finally {
      loading = false;
    }
  }

  function handleCancel() {
    dispatch('cancel');
  }
</script>

<div class="project-edit-form">
  <h3>プロジェクトを編集</h3>

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
          更新中...
        {:else}
          更新
        {/if}
      </button>
      <button type="button" class="btn btn-secondary" on:click={handleCancel} disabled={loading}>
        キャンセル
      </button>
    </div>
  </form>
</div>

<style>
  .project-edit-form {
    margin: 1rem 0;
    padding: 1rem;
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
  }

  h3 {
    margin: 0 0 1rem 0;
    color: #1f2937;
    font-size: 1.125rem;
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

  input[type="text"],
  select {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 0.875rem;
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
    gap: 0.5rem;
    justify-content: flex-end;
    margin-top: 1rem;
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

