<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Chat from '$lib/components/chat/Chat.svelte';
  // Builder-only: suppress layout artifacts and clear any existing chat ID
  import { chatId as storeChatId, builderMode } from '$lib/stores';
  // For live HTML previews
  import HtmlPreview from '$lib/components/common/HtmlPreview.svelte';
  import { extractPreviewBlocks, type PreviewBlock } from '$lib/utils/htmlPreview';
  import { writable, derived } from 'svelte/store';
  import { createMessagesList } from '$lib/utils';

  // Track running list of messages for preview extraction
  const messages = writable<Array<{ role: string; content: string }>>([]);
  function onHistoryChange(history) {
    // build flat list of messages in order
    messages.set(createMessagesList(history, history.currentId));
  }
  // Derive preview blocks from messages
  const previewBlocks: typeof PreviewBlock[] = derived(
    messages,
    $msgs => extractPreviewBlocks($msgs)
  );

  onMount(() => {
    // Enter Builder mode (suppress controls pane artifacts)
    builderMode.set(true);
    // Clear any existing chat ID so we lazily create on first message send
    storeChatId.set('');
  });
  onDestroy(() => {
    // Leave Builder mode when unmounting
    builderMode.set(false);
  });

</script>

<div class="flex flex-1 h-full w-full flex-row">
  <div class="w-1/3 border-r h-full flex flex-col">
      <Chat
        disableLayout={true}
        onHistoryChange={onHistoryChange}
      />
  </div>
  <div class="w-2/3 h-full flex flex-col">
    {#if $previewBlocks.length > 0}
      <!-- Live HTML/CSS/JS preview of code blocks -->
      <HtmlPreview blocks={$previewBlocks} />
    {:else}
      <div class="w-full h-full flex items-center justify-center text-gray-500">
        No HTML/CSS/JS preview available
      </div>
    {/if}
  </div>
</div>