<script>
  import { createEventDispatcher } from 'svelte';
  import { roundApi, nodeApi } from '../lib/api.js';

  export let round;
  export let roundNumber;
  export let steps = [];
  export let nodes = [];

  const dispatch = createEventDispatcher();

  async function handleNextRound() {
    dispatch('nextRound');
  }

  async function handleComplete() {
    dispatch('complete');
  }

  async function handlePending() {
    dispatch('pending');
  }

  function getStepTypeLabel(stepType, stepTypeNumber) {
    const labels = {
      'overview': '俯瞰',
      'extract': '要素抽出',
      'flow': '流れ構築',
      'mvp': '最小仕様',
      'expand': '拡張余地',
    };
    const label = labels[stepType] || stepType;
    return stepTypeNumber ? `${stepTypeNumber}. ${label}` : label;
  }
</script>

<div class="round-summary">
  <h2>第{roundNumber}周のまとめ</h2>

  {#if round.note}
    <div class="round-note">
      <h3>なんか思いついた？</h3>
      <p>{round.note}</p>
    </div>
  {/if}

  <div class="summary-sections">
    <section class="summary-section">
      <h3>ステップ ({steps.length})</h3>
      {#if steps.length > 0}
        <div class="steps-summary">
          {#each steps as step}
            <div class="step-summary-item">
              <div class="step-summary-header">
                {#if step.step_type_number}
                  <span class="step-type-number">{step.step_type_number}</span>
                {/if}
                <span class="step-type">{getStepTypeLabel(step.step_type, step.step_type_number)}</span>
              </div>
              <p class="step-content">{step.content}</p>
            </div>
          {/each}
        </div>
      {:else}
        <p class="empty">ステップがありません</p>
      {/if}
    </section>

    <section class="summary-section">
      <h3>ノード ({nodes.length})</h3>
      {#if nodes.length > 0}
        <div class="nodes-summary">
          {#each nodes as node}
            <div class="node-summary-item">
              <h4>{node.title}</h4>
              {#if node.context}
                <p class="node-context">{node.context}</p>
              {/if}
            </div>
          {/each}
        </div>
      {:else}
        <p class="empty">ノードがありません</p>
      {/if}
    </section>
  </div>

  <div class="summary-actions">
    {#if roundNumber < 5}
      <button class="btn btn-primary" on:click={handleNextRound}>
        次の周へ
      </button>
    {:else}
      <button class="btn btn-success" on:click={handleComplete}>
        完成
      </button>
    {/if}
    <button class="btn btn-secondary" on:click={handlePending}>
      ペンディングにする
    </button>
  </div>
</div>

<style>
  .round-summary {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  }

  .round-summary h2 {
    margin: 0 0 2rem 0;
    color: #1f2937;
    font-size: 1.75rem;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 1rem;
  }

  .round-note {
    margin-bottom: 2rem;
    padding: 1rem;
    background-color: #fef3c7;
    border: 1px solid #fbbf24;
    border-radius: 4px;
  }

  .round-note h3 {
    margin: 0 0 0.5rem 0;
    color: #92400e;
    font-size: 1rem;
  }

  .round-note p {
    margin: 0;
    color: #78350f;
    white-space: pre-wrap;
  }

  .summary-sections {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    margin-bottom: 2rem;
  }

  .summary-section {
    padding: 1.5rem;
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
  }

  .summary-section h3 {
    margin: 0 0 1rem 0;
    color: #1f2937;
    font-size: 1.25rem;
  }

  .steps-summary,
  .nodes-summary {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .step-summary-item,
  .node-summary-item {
    padding: 1rem;
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
  }

  .step-summary-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .step-type-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background-color: #2563eb;
    color: white;
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
  }

  .step-type {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background-color: #dbeafe;
    color: #1e40af;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
  }

  .step-content {
    margin: 0;
    color: #4b5563;
    font-size: 0.875rem;
    white-space: pre-wrap;
  }

  .node-summary-item h4 {
    margin: 0 0 0.5rem 0;
    color: #1f2937;
    font-size: 1rem;
  }

  .node-context {
    margin: 0;
    color: #6b7280;
    font-size: 0.875rem;
    white-space: pre-wrap;
  }

  .empty {
    color: #6b7280;
    font-style: italic;
    text-align: center;
    padding: 2rem;
  }

  .summary-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    padding-top: 2rem;
    border-top: 2px solid #e5e7eb;
  }

  .btn {
    padding: 0.75rem 2rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
  }

  .btn-primary {
    background-color: #2563eb;
    color: white;
  }

  .btn-primary:hover {
    background-color: #1d4ed8;
  }

  .btn-success {
    background-color: #10b981;
    color: white;
  }

  .btn-success:hover {
    background-color: #059669;
  }

  .btn-secondary {
    background-color: #6b7280;
    color: white;
  }

  .btn-secondary:hover {
    background-color: #4b5563;
  }
</style>

