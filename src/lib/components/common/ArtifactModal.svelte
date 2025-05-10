<script lang="ts">
  import Modal from './Modal.svelte';
  import XMark from '../icons/XMark.svelte';
  import { showArtifactModal, selectedArtifact } from '$lib/stores/artifacts';
  import { get } from 'svelte/store';

  // Subscribe to current artifact
  let artifact = get(selectedArtifact);
  selectedArtifact.subscribe((v) => artifact = v);

  const close = () => {
    showArtifactModal.set(false);
  };
</script>

<Modal show={get(showArtifactModal)} size="full" on:close={close} className="overflow-hidden">
  {#if artifact}
    <div class="flex flex-col h-full bg-white dark:bg-gray-900">
      <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800">
        <div class="font-semibold text-lg truncate">{artifact.name}</div>
        <button class="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-800" on:click={close}>
          <XMark className="size-5 text-gray-600 dark:text-gray-300" />
        </button>
      </div>
      <div class="flex-1">
        <iframe
          class="w-full h-full border-0"
          srcdoc={artifact.content}
          sandbox="allow-scripts allow-same-origin"
        ></iframe>
      </div>
    </div>
  {/if}
</Modal>