<script>
  import { onMount, onDestroy } from 'svelte';
  import { projectApi, nodeApi } from '../lib/api.js';
  import { createEventDispatcher } from 'svelte';

  export let projectId;

  const dispatch = createEventDispatcher();

  let container;
  let network = null;
  let Network = null;
  let networkImportError = null;
  let nodes = [];
  let edges = [];
  let loading = true;
  let error = '';

  onMount(async () => {
    // vis-networkを動的にインポート
    try {
      const visNetwork = await import('vis-network/standalone');
      Network = visNetwork.Network;
    } catch (err) {
      networkImportError = err;
      error = `vis-networkライブラリの読み込みに失敗しました: ${err.message}`;
      loading = false;
      return;
    }
    
    await loadNodesAndLinks();
    if (container) {
      initializeNetwork();
    }
  });

  onDestroy(() => {
    if (network) {
      network.destroy();
    }
  });

  async function loadNodesAndLinks() {
    try {
      loading = true;
      error = '';
      
      // プロジェクトに紐づくノードを取得
      const projectNodes = await projectApi.getNodes(projectId);
      
      // 各ノードのリンクを取得
      const nodeData = [];
      const edgeData = [];
      
      for (const node of projectNodes) {
        // ノードデータを作成
        nodeData.push({
          id: node.id,
          label: node.title || '無題',
          title: node.context ? `${node.title}\n文脈: ${node.context}` : node.title,
          color: {
            background: '#e3f2fd',
            border: '#1976d2',
            highlight: {
              background: '#bbdefb',
              border: '#0d47a1'
            }
          },
          shape: 'box',
          font: {
            size: 14,
            face: 'Arial'
          }
        });
        
        // ノードのリンクを取得
        try {
          const linksData = await nodeApi.getLinks(node.id);
          
          // 送信リンク（outgoing）
          for (const link of linksData.outgoing || []) {
            // プロジェクト内のノードのみを表示
            const targetNode = projectNodes.find(n => n.id === link.to_node_id);
            if (targetNode) {
              const weight = parseFloat(link.weight) || 0.5;
              edgeData.push({
                from: node.id,
                to: link.to_node_id,
                width: Math.max(1, weight * 3),
                color: {
                  color: '#666',
                  highlight: '#1976d2',
                  opacity: 0.6
                },
                label: `重み: ${weight.toFixed(1)}`,
                font: {
                  size: 10,
                  align: 'middle'
                }
              });
            }
          }
        } catch (err) {
          console.error(`Failed to load links for node ${node.id}:`, err);
        }
      }
      
      nodes = nodeData;
      edges = edgeData;
    } catch (err) {
      error = err.message || 'ノードの読み込みに失敗しました';
      console.error('Failed to load nodes:', err);
    } finally {
      loading = false;
    }
  }

  function initializeNetwork() {
    if (!container) {
      return;
    }
    
    if (!Network) {
      error = 'vis-networkライブラリの読み込みに失敗しました';
      return;
    }
    
    const data = {
      nodes: nodes,
      edges: edges
    };
    
    const options = {
      nodes: {
        shape: 'box',
        font: {
          size: 14,
          face: 'Arial'
        },
        borderWidth: 2,
        shadow: true
      },
      edges: {
        arrows: {
          to: {
            enabled: true,
            scaleFactor: 0.5
          }
        },
        smooth: {
          type: 'continuous',
          roundness: 0.5
        },
        shadow: true
      },
      physics: {
        enabled: true,
        stabilization: {
          enabled: true,
          iterations: 200
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 100,
        zoomView: true,
        dragView: true
      }
    };
    
    try {
      network = new Network(container, data, options);
      
      // ノードクリックイベント
      network.on('click', (params) => {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          dispatch('nodeClick', { nodeId });
        }
      });
      
      // ダブルクリックでズームイン
      network.on('doubleClick', (params) => {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          network.focus(nodeId, {
            scale: 1.5,
            animation: true
          });
        }
      });
    } catch (err) {
      error = `グラフの初期化に失敗しました: ${err.message}`;
      console.error('Failed to initialize network:', err);
    }
  }

  // ノードとエッジが更新されたらネットワークを更新
  $: if (network && nodes.length > 0) {
    network.setData({ nodes, edges });
  }
</script>

<div class="word-tree-container">
  {#if loading}
    <div class="loading">読み込み中...</div>
  {:else if error}
    <div class="error">{error}</div>
  {:else if nodes.length === 0}
    <div class="empty">ノードがありません</div>
  {:else}
    <div class="network-container" bind:this={container}></div>
    <div class="info">
      <span>ノード数: {nodes.length}</span>
      <span>リンク数: {edges.length}</span>
    </div>
  {/if}
</div>

<style>
  .word-tree-container {
    width: 100%;
    height: 600px;
    position: relative;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    background-color: #f9fafb;
  }

  .network-container {
    width: 100%;
    height: 100%;
  }

  .loading,
  .error,
  .empty {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    font-size: 1rem;
    color: #6b7280;
  }

  .error {
    color: #dc2626;
    background-color: #fee2e2;
    padding: 1rem;
    border-radius: 4px;
    margin: 1rem;
  }

  .info {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-size: 0.875rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    gap: 1rem;
  }

  .info span {
    color: #374151;
  }
</style>

