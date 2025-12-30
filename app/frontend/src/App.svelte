<script>
  import { onMount } from 'svelte';
  import { isAuthenticated, clearAuth } from './lib/auth.js';
  import { authApi } from './lib/api.js';
  import LoginForm from './components/LoginForm.svelte';
  import ProjectList from './components/ProjectList.svelte';
  import ProjectDetail from './components/ProjectDetail.svelte';
  
  let authenticated = false;
  let user = null;
  let loading = true;
  let currentView = 'list'; // 'list' or 'detail'
  let projectId = null;
  
  onMount(async () => {
    authenticated = isAuthenticated();
    
    if (authenticated) {
      try {
        user = await authApi.getUser();
      } catch (err) {
        // トークンが無効な場合
        clearAuth();
        authenticated = false;
      }
    }
    
    // URLからプロジェクトIDを取得
    const path = window.location.pathname;
    const match = path.match(/\/projects\/([^\/]+)/);
    if (match) {
      projectId = match[1];
      currentView = 'detail';
    }
    
    loading = false;
  });
  
  function handleLogout() {
    clearAuth();
    authenticated = false;
    user = null;
    currentView = 'list';
    projectId = null;
    window.history.pushState({}, '', '/');
  }
  
  function handleProjectClick(id) {
    projectId = id;
    currentView = 'detail';
    window.history.pushState({}, '', `/projects/${id}`);
  }
  
  function handleBackToList() {
    currentView = 'list';
    projectId = null;
    window.history.pushState({}, '', '/');
  }
  
  // ブラウザの戻る/進むボタンに対応
  window.addEventListener('popstate', () => {
    const path = window.location.pathname;
    const match = path.match(/\/projects\/([^\/]+)/);
    if (match) {
      projectId = match[1];
      currentView = 'detail';
    } else {
      currentView = 'list';
      projectId = null;
    }
  });
</script>

<main>
  <header>
    <h1>thinkRing</h1>
    {#if authenticated && user}
      <div class="user-info">
        {#if currentView === 'detail'}
          <button class="btn-back" on:click={handleBackToList}>← 一覧に戻る</button>
        {/if}
        <span>ようこそ、{user.username}さん</span>
        <button on:click={handleLogout}>ログアウト</button>
      </div>
    {/if}
  </header>
  
  {#if loading}
    <p>読み込み中...</p>
  {:else if !authenticated}
    <LoginForm />
  {:else if currentView === 'detail' && projectId}
    <ProjectDetail projectId={projectId} />
  {:else}
    <ProjectList on:projectClick={(e) => handleProjectClick(e.detail)} />
  {/if}
</main>

<style>
  main {
    min-height: 100vh;
    background-color: #f9fafb;
  }
  
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: white;
    border-bottom: 1px solid #e5e7eb;
  }
  
  h1 {
    margin: 0;
    color: #2563EB;
    font-size: 1.5rem;
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .btn-back {
    padding: 0.5rem 1rem;
    background-color: #6b7280;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
  }
  
  .btn-back:hover {
    background-color: #4b5563;
  }
  
  .user-info button:not(.btn-back) {
    padding: 0.5rem 1rem;
    background-color: #dc2626;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
  }
  
  .user-info button:not(.btn-back):hover {
    background-color: #b91c1c;
  }
</style>
