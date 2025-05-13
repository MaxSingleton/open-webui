<script lang="ts">
  import type { PreviewBlock } from '$lib/utils/htmlPreview';
  export let blocks: PreviewBlock[] = [];
  // index of currently displayed block
  let idx = 0;
  let copied = false;
  let iframeElement: HTMLIFrameElement;

  function prev() {
    idx = Math.max(0, idx - 1);
  }
  function next() {
    idx = Math.min(blocks.length - 1, idx + 1);
  }
  async function copy() {
    try {
      await navigator.clipboard.writeText(blocks[idx].content);
      copied = true;
      setTimeout(() => (copied = false), 2000);
    } catch {
      // ignore
    }
  }
  function fullscreen() {
    if (!iframeElement) return;
    if (iframeElement.requestFullscreen) iframeElement.requestFullscreen();
    else if ((iframeElement as any).webkitRequestFullscreen) (iframeElement as any).webkitRequestFullscreen();
    else if ((iframeElement as any).msRequestFullscreen) (iframeElement as any).msRequestFullscreen();
  }
</script>

<div class="flex flex-col h-full bg-white dark:bg-gray-900">
  <div class="flex items-center justify-between p-2 border-b border-gray-200 dark:border-gray-800">
  <div class="pointer-events-auto z-20 flex justify-between items-center p-2.5 font-primary text-gray-900 dark:text-white">
    <button
      on:click={prev}
      disabled={idx <= 0}
      class="self-center p-1 hover:bg-black/5 dark:hover:bg-white/5 dark:hover:text-white hover:text-black rounded-md transition disabled:cursor-not-allowed"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" class="size-3.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
      </svg>
    </button>
    <div class="text-xs self-center dark:text-gray-100 min-w-fit">
      Version {idx + 1} of {blocks.length}
    </div>
    <button
      on:click={next}
      disabled={idx >= blocks.length - 1}
      class="self-center p-1 hover:bg-black/5 dark:hover:bg-white/5 dark:hover:text-white hover:text-black rounded-md transition disabled:cursor-not-allowed"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" class="size-3.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
      </svg>
    </button>
  </div>
    <div class="flex items-center gap-1">
      <button
        on:click={copy}
        class="copy-code-button bg-none border-none text-xs bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-md px-1.5 py-0.5"
      >
        {copied ? 'Copied' : 'Copy'}
      </button>
      {#if blocks[idx].type === 'iframe'}
        <button
          on:click={fullscreen}
          class="bg-none border-none text-xs bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-md px-1.5 py-0.5"
        >
          Fullscreen
        </button>
      {/if}
    </div>
  </div>
  <div class="flex-1 relative">
    {#if blocks[idx].type === 'iframe'}
      <iframe
        bind:this={iframeElement}
        class="w-full h-full border-0"
        srcdoc={blocks[idx].content}
        sandbox="allow-scripts allow-same-origin"
      ></iframe>
    {:else if blocks[idx].type === 'svg'}
      <div class="w-full h-full overflow-auto p-2" innerHTML={blocks[idx].content}></div>
    {/if}
  </div>
</div>