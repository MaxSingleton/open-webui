<script lang="ts">
  import { onMount, getContext } from 'svelte';
  import { page } from '$app/stores';
  import { showSidebar, WEBUI_NAME } from '$lib/stores';
  import MenuLines from '$lib/components/icons/MenuLines.svelte';
  const i18n = getContext('i18n');
  let loaded = false;
  onMount(() => {
    loaded = true;
  });
</script>

<svelte:head>
  <title>{$i18n?.t('Projects') ?? 'Projects'} | {$WEBUI_NAME}</title>
</svelte:head>

  {#if loaded}
  <div class="relative flex flex-col flex-1 transition-width duration-200 ease-in-out {$showSidebar ? 'md:max-w-[calc(100%-260px)]' : ''}">
    <nav class="px-2.5 pt-1 backdrop-blur-xl drag-region">
      <div class="flex items-center gap-1">
        <div class="{$showSidebar ? 'md:hidden' : ''} self-center flex flex-none items-center">
          <button
            id="sidebar-toggle-button"
            class="cursor-pointer p-1.5 flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition"
          on:click={() => showSidebar.set(!$showSidebar)}
            aria-label="Toggle Sidebar"
          >
            <div class="m-auto self-center">
              <MenuLines />
            </div>
          </button>
        </div>
        <div>
          <div class="flex gap-1 scrollbar-none overflow-x-auto w-fit text-center text-sm font-medium rounded-full bg-transparent py-1 touch-auto pointer-events-auto">
            {#if $page.params.projectId}
            <a
                href={`/projects/${$page.params.projectId}/home`}
                class="min-w-fit rounded-full p-1.5 {$page.url.pathname.endsWith('/home') ? '' : 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
              >{$i18n?.t('Home') ?? 'Home'}</a>
              <a
                href={`/projects/${$page.params.projectId}/planning`}
                class="min-w-fit rounded-full p-1.5 {$page.url.pathname.endsWith('/planning') ? '' : 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
              >{$i18n?.t('Workflow') ?? 'Workflow'}</a>
              <a
                href={`/projects/${$page.params.projectId}/documents`}
                class="min-w-fit rounded-full p-1.5 {$page.url.pathname.endsWith('/documents') ? '' : 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
              >{$i18n?.t('Documents') ?? 'Documents'}</a>
            {/if}
          </div>
        </div>
      </div>
    </nav>
    <div class="pb-1 px-[18px] flex-1 max-h-full overflow-y-auto" id="projects-container">
      <slot />
    </div>
  </div>
{/if}