<script>
  import { authApi } from '../lib/api.js';
  
  let username = '';
  let password = '';
  let error = '';
  let loading = false;
  
  async function handleLogin() {
    error = '';
    loading = true;
    
    try {
      await authApi.login(username, password);
      // ログイン成功時は親コンポーネントに通知
      window.location.reload();
    } catch (err) {
      error = err.message || 'ログインに失敗しました';
    } finally {
      loading = false;
    }
  }
</script>

<div class="login-form">
  <h2>ログイン</h2>
  
  {#if error}
    <div class="error">{error}</div>
  {/if}
  
  <form on:submit|preventDefault={handleLogin}>
    <div class="form-group">
      <label for="username">ユーザー名</label>
      <input
        id="username"
        type="text"
        bind:value={username}
        required
        disabled={loading}
      />
    </div>
    
    <div class="form-group">
      <label for="password">パスワード</label>
      <input
        id="password"
        type="password"
        bind:value={password}
        required
        disabled={loading}
      />
    </div>
    
    <button type="submit" disabled={loading}>
      {loading ? 'ログイン中...' : 'ログイン'}
    </button>
  </form>
</div>

<style>
  .login-form {
    max-width: 400px;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
  }
  
  h2 {
    margin-top: 0;
    color: #2563EB;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  
  input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  input:disabled {
    background-color: #f3f4f6;
    cursor: not-allowed;
  }
  
  button {
    width: 100%;
    padding: 0.75rem;
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
  }
  
  button:hover:not(:disabled) {
    background-color: #1d4ed8;
  }
  
  button:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
  }
  
  .error {
    padding: 0.75rem;
    margin-bottom: 1rem;
    background-color: #fee2e2;
    color: #dc2626;
    border-radius: 4px;
  }
</style>

