<script>
  import { roundApi } from '../lib/api.js';
  import { createEventDispatcher } from 'svelte';

  export let roundId;

  const dispatch = createEventDispatcher();

  const stepTypeOptions = [
    { value: 'overview', label: '俯瞰' },
    { value: 'extract', label: '要素抽出' },
    { value: 'flow', label: '流れ構築' },
    { value: 'mvp', label: '最小仕様' },
    { value: 'expand', label: '拡張余地' },
  ];

  let stepType = 'overview';
  let content = '';
  let loading = false;
  let error = '';

  async function handleSubmit() {
    if (!content.trim()) {
      error = '内容を入力してください';
      return;
    }

    loading = true;
    error = '';

    try {
      await roundApi.createStep(roundId, stepType, content);
      dispatch('created');
      stepType = 'overview';
      content = '';
    } catch (err) {
      error = err.message || 'ステップの作成に失敗しました';
    } finally {
      loading = false;
    }
  }

  function handleCancel() {
    dispatch('cancel');
  }
</script>

<div class="step-create-form">
  <h4>新しいステップを作成</h4>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  <form on:submit|preventDefault={handleSubmit}>
    <div class="form-group">
      <label for="stepType">ステップ種別 *</label>
      <select id="stepType" bind:value={stepType} disabled={loading}>
        {#each stepTypeOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
    </div>

    <div class="form-group">
      <label for="content">内容 *</label>
      <textarea
        id="content"
        bind:value={content}
        rows="5"
        placeholder="ステップの内容を入力"
        required
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
  .step-create-form {
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

  select:focus,
  textarea:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }

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

