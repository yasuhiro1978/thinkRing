<script>
  import { projectApi } from '../lib/api.js';
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  import ProjectCreateForm from './ProjectCreateForm.svelte';

  const dispatch = createEventDispatcher();
  
  let projects = [];
  let loading = true;
  let error = '';
  let showCreateForm = false;
  
  async function loadProjects() {
    try {
      const response = await projectApi.list();
      projects = response.results || response;
    } catch (err) {
      error = err.message || 'プロジェクトの取得に失敗しました';
    } finally {
      loading = false;
    }
  }
  
  onMount(async () => {
    await loadProjects();
  });
  
  async function handleDelete(id) {
    if (!confirm('このプロジェクトを削除しますか？')) {
      return;
    }
    
    try {
      await projectApi.delete(id);
      projects = projects.filter(p => p.id !== id);
    } catch (err) {
      alert('削除に失敗しました: ' + err.message);
    }
  }
  
  function handleProjectCreated() {
    showCreateForm = false;
    loadProjects();
  }
  
  function handleCreateCancel() {
    showCreateForm = false;
  }
</script>

<div class="project-list">
  <div class="header">
    <h2>プロジェクト一覧</h2>
    <button class="btn btn-primary" on:click={() => showCreateForm = true}>
      + 新規作成
    </button>
  </div>
  
  {#if showCreateForm}
    <ProjectCreateForm
      on:created={handleProjectCreated}
      on:cancel={handleCreateCancel}
    />
  {/if}
  
  {#if loading}
    <p>読み込み中...</p>
  {:else if error}
    <div class="error">{error}</div>
  {:else if projects.length === 0}
    <p>プロジェクトがありません</p>
  {:else}
    <ul class="project-items">
      {#each projects as project}
        <li class="project-item">
          <div class="project-info">
            <h3>{project.title}</h3>
            <p class="project-meta">
              <span class="status status-{project.status}">{project.status}</span>
              <span class="date">{new Date(project.created_at).toLocaleDateString('ja-JP')}</span>
            </p>
          </div>
          <div class="project-actions">
            <button class="btn btn-primary" on:click={() => dispatch('projectClick', project.id)}>
              詳細
            </button>
            <button class="btn btn-danger" on:click={() => handleDelete(project.id)}>
              削除
            </button>
          </div>
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  .project-list {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  h2 {
    color: #2563EB;
    margin: 0;
  }
  
  .project-items {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .project-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    background-color: white;
  }
  
  .project-info {
    flex: 1;
  }
  
  .project-info h3 {
    margin: 0 0 0.5rem 0;
    color: #1f2937;
  }
  
  .project-meta {
    display: flex;
    gap: 1rem;
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
  
  .project-actions {
    display: flex;
    gap: 0.5rem;
  }
  
  .btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-decoration: none;
    font-size: 0.875rem;
  }
  
  .btn-primary {
    background-color: #2563EB;
    color: white;
  }
  
  .btn-primary:hover {
    background-color: #1d4ed8;
  }
  
  .btn-danger {
    background-color: #dc2626;
    color: white;
  }
  
  .btn-danger:hover {
    background-color: #b91c1c;
  }
  
  .error {
    padding: 1rem;
    background-color: #fee2e2;
    color: #dc2626;
    border-radius: 4px;
  }
</style>

