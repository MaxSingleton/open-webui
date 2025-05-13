<script lang="ts">
  import { onMount } from 'svelte';
  import Chat from '$lib/components/chat/Chat.svelte';
  import { createNewChat, updateChatFolderIdById } from '$lib/apis/chats';
  // track chatId in global store (for other UI components)
  import { chatId as storeChatId } from '$lib/stores';
  // For live HTML previews
  import HtmlPreview from '$lib/components/common/HtmlPreview.svelte';
  import { extractPreviewBlocks, type PreviewBlock } from '$lib/utils/htmlPreview';
  import { writable, derived } from 'svelte/store';
  import { createMessagesList } from '$lib/utils';

  let chatId = '';
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

  // Ensure builder chats are stored in the Artifacts folder, not the main chat list
  import { getFolders, createNewFolder } from '$lib/apis/folders';
  onMount(async () => {
    // Create a new chat session for Builder
    const chat = await createNewChat(localStorage.token, {});
    chatId = chat.id;
    // Find or create the top-level 'Artifacts' folder for builder chats
    let folders = await getFolders(localStorage.token);
    let artifact = folders.find((f) => f.name === 'Artifacts');
    if (!artifact) {
      artifact = await createNewFolder(localStorage.token, 'Artifacts');
    }
    // Assign this chat to the Artifacts folder so it does not appear in the main Chats list
    await updateChatFolderIdById(localStorage.token, chatId, artifact?.id);
    // Update global chatId store (triggers sidebar folder refresh)
    storeChatId.set(chatId);
  });

</script>

<div class="flex flex-1 h-full w-full flex-row">
  <div class="w-1/3 border-r h-full flex flex-col">
    {#if chatId}
      <Chat
        chatIdProp={chatId}
        disableLayout={true}
        onHistoryChange={onHistoryChange}
      />
    {/if}
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