/**
 * 認証関連のユーティリティ
 */

export function isAuthenticated() {
  return !!localStorage.getItem('access_token');
}

export function getAccessToken() {
  return localStorage.getItem('access_token');
}

export function clearAuth() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

