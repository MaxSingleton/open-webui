<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Chat from '$lib/components/chat/Chat.svelte';
  import { createNewChat } from '$lib/apis/chats';
  import { selectedArtifact } from '$lib/stores/artifacts';
  import { chatId as storeChatId } from '$lib/stores';
  import { get } from 'svelte/store';

  let chatId = '';
  let artifact = get(selectedArtifact);
  const unsub = selectedArtifact.subscribe(v => artifact = v);

  onMount(async () => {
    const chat = await createNewChat(localStorage.token);
    chatId = chat.id;
    storeChatId.set(chatId);
  });

  onDestroy(() => {
    unsub();
  });
</script>

<div class="flex h-full w-full">
  <div class="w-1/3 border-r">
    {#if chatId}
      <Chat chatIdProp={chatId} />
    {/if}
  </div>
  <div class="w-2/3">
    {#if artifact}
      <div class="flex flex-col h-full bg-white dark:bg-gray-900">
        <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800">
          <div class="font-semibold text-lg truncate">{artifact.name}</div>
        </div>
        <div class="flex-1">
          <iframe
            class="w-full h-full border-0"
            srcdoc={artifact.content}
            sandbox="allow-scripts allow-same-origin"
          ></iframe>
        </div>
      </div>
    {:else}
      <div class="w-full h-full flex items-center justify-center text-gray-500">
        No artifact selected
      </div>
    {/if}
  </div>
</div>