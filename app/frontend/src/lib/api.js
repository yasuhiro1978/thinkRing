/**
 * APIクライアント
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

/**
 * APIリクエストの基本関数
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = localStorage.getItem('access_token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  if (!response.ok) {
    let error;
    try {
      error = await response.json();
    } catch (e) {
      error = { message: 'Unknown error' };
    }
    // エラーレスポンスの構造を確認して適切なメッセージを抽出
    const errorMessage = error?.error?.message || error?.message || error?.detail || `HTTP error! status: ${response.status}`;
    throw new Error(errorMessage);
  }
  
  // 204 No Contentの場合はbodyが空なので、JSONパースをスキップ
  if (response.status === 204 || response.status === 201 && !response.headers.get('content-type')?.includes('application/json')) {
    return null;
  }
  
  // レスポンスにコンテンツがある場合のみJSONパース
  const text = await response.text();
  if (!text) {
    return null;
  }
  
  try {
    return JSON.parse(text);
  } catch (e) {
    // JSONパースに失敗した場合は、テキストをそのまま返す
    return text;
  }
}

/**
 * 認証API
 */
export const authApi = {
  async login(username, password) {
    const data = await apiRequest('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    
    if (data.access) {
      localStorage.setItem('access_token', data.access);
      if (data.refresh) {
        localStorage.setItem('refresh_token', data.refresh);
      }
    }
    
    return data;
  },
  
  async logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    try {
      await apiRequest('/auth/logout/', { method: 'POST' });
    } catch (error) {
      // ログアウトは失敗してもローカルストレージはクリアする
      console.error('Logout error:', error);
    }
  },
  
  async getUser() {
    return apiRequest('/auth/user/');
  },
  
  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token');
    }
    
    const data = await apiRequest('/auth/refresh/', {
      method: 'POST',
      body: JSON.stringify({ refresh: refreshToken }),
    });
    
    if (data.access) {
      localStorage.setItem('access_token', data.access);
    }
    
    return data;
  },
};

/**
 * プロジェクトAPI
 */
export const projectApi = {
  async list() {
    return apiRequest('/projects/');
  },
  
  async get(id) {
    return apiRequest(`/projects/${id}/`);
  },
  
  async create(title, status = 'active') {
    return apiRequest('/projects/', {
      method: 'POST',
      body: JSON.stringify({ title, status }),
    });
  },
  
  async update(id, data) {
    return apiRequest(`/projects/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },
  
  async delete(id) {
    return apiRequest(`/projects/${id}/`, {
      method: 'DELETE',
    });
  },
  
  async getRounds(projectId) {
    return apiRequest(`/projects/${projectId}/rounds/`);
  },
  
  async getNodes(projectId) {
    return apiRequest(`/projects/${projectId}/nodes/`);
  },
  
  async createRound(projectId, roundNumber, note = '') {
    return apiRequest(`/projects/${projectId}/rounds/`, {
      method: 'POST',
      body: JSON.stringify({ round_number: roundNumber, note }),
    });
  },
  
  async getNodes(projectId) {
    return apiRequest(`/projects/${projectId}/nodes/`);
  },
};

/**
 * 周API
 */
export const roundApi = {
  async get(id) {
    return apiRequest(`/rounds/${id}/`);
  },
  
  async update(id, data) {
    return apiRequest(`/rounds/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },
  
  async getSteps(roundId) {
    return apiRequest(`/rounds/${roundId}/steps/`);
  },
  
  async createStep(roundId, stepType, content) {
    return apiRequest(`/rounds/${roundId}/steps/`, {
      method: 'POST',
      body: JSON.stringify({ step_type: stepType, content }),
    });
  },
};

/**
 * ノードAPI
 */
export const nodeApi = {
  async list() {
    return apiRequest('/nodes/');
  },
  
  async get(id) {
    return apiRequest(`/nodes/${id}/`);
  },
  
  async create(data) {
    return apiRequest('/nodes/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  
  async update(id, data) {
    return apiRequest(`/nodes/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },
  
  async delete(id) {
    return apiRequest(`/nodes/${id}/`, {
      method: 'DELETE',
    });
  },
  
  async getGlobalNodes() {
    return apiRequest('/nodes/global_nodes/');
  },
  
  async getLinks(nodeId) {
    return apiRequest(`/nodes/${nodeId}/links/`);
  },
  
  async createLink(fromNodeId, toNodeId, weight = 0.5) {
    return apiRequest(`/nodes/${fromNodeId}/links/`, {
      method: 'POST',
      body: JSON.stringify({ to_node_id: toNodeId, weight }),
    });
  },
  
  async deleteLink(nodeId, linkId) {
    return apiRequest(`/nodes/${nodeId}/links/`, {
      method: 'DELETE',
      body: JSON.stringify({ link_id: linkId }),
    });
  },
};

