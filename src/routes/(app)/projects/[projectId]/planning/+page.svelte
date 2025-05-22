<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  let projectId: string;
  $: projectId = $page.params.projectId;

  let connected = false;
  let databaseId: string | null = null;
  let pages: any[] = [];
  let startCursor: string = '';
  let loading = false;

  onMount(async () => {
    try {
      const res = await fetch(`/api/v1/notion/status?project_id=${projectId}`, { credentials: 'include' });
      if (res.ok) {
        const data = await res.json();
        connected = data.connected;
      }
      if (connected) {
        // load configured database ID
        const cfgRes = await fetch(`/api/v1/notion/integration?project_id=${projectId}`, { credentials: 'include' });
        if (cfgRes.ok) {
          const cfg = await cfgRes.json();
          databaseId = cfg.database_id;
          if (databaseId) {
            await loadPages();
          }
        }
      }
    } catch (e) {
      console.error('Failed to fetch Notion connection status', e);
    }
  });

  function connectNotion() {
    window.location.href = `/api/v1/notion/connect?project_id=${projectId}`;
  }

  async function saveIntegration() {
    if (!databaseId) return;
    const res = await fetch(
      `/api/v1/notion/integration?project_id=${projectId}`,
      {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ database_id: databaseId })
      }
    );
    if (res.ok) {
      await loadPages();
    }
  }

  async function loadPages() {
    loading = true;
    const res = await fetch(
      `/api/v1/notion/pages?project_id=${projectId}${startCursor ? `&start_cursor=${startCursor}` : ''}`,
      { credentials: 'include' }
    );
    if (res.ok) {
      const data = await res.json();
      pages = data.results;
      startCursor = data.next_cursor || '';
    }
    loading = false;
  }
</script>

<div class="px-6 py-4">
  <h2 class="text-xl font-semibold mb-4">Planning</h2>

  {#if !connected}
    <div class="space-y-2">
      <p>Connect your Notion workspace to manage tasks, deliverables, and view them in lists, calendars, and boards.</p>
      <button
        on:click={connectNotion}
        class="px-4 py-2 bg-blue-600 text-white rounded"
      >
        Connect to Notion
      </button>
    </div>
  {:else}
    <div class="space-y-4">
      <p class="text-green-600">Notion connected. Enter a Notion database ID to load pages:</p>
      <div class="flex gap-2">
        <input
          type="text"
          placeholder="Notion Database ID"
          bind:value={databaseId}
          class="border p-2 rounded flex-1"
        />
        <button on:click={saveIntegration} class="px-4 py-2 bg-blue-600 text-white rounded">
          Save
        </button>
      </div>
      {#if databaseId}
        <div>
          <h3 class="font-semibold mb-2">Pages</h3>
          {#if loading}
            <p>Loading pages…</p>
          {:else}
            <ul class="list-disc pl-5 space-y-1">
              {#each pages as page}
                <li>{page.id} – {page.properties?.Name?.title[0]?.plain_text || 'Untitled'}</li>
              {/each}
            </ul>
            {#if startCursor}
              <button on:click={loadPages} class="mt-2 px-3 py-1 bg-gray-200 rounded">
                Load more
              </button>
            {/if}
          {/if}
        </div>
      {/if}
    </div>
  {/if}
</div>