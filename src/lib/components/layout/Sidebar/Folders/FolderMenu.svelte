<script lang="ts">
  import { DropdownMenu } from 'bits-ui';
  import { flyAndScale } from '$lib/utils/transitions';
  import { getContext, createEventDispatcher } from 'svelte';

  const i18n = getContext('i18n');
  const dispatch = createEventDispatcher();

  import Dropdown from '$lib/components/common/Dropdown.svelte';
  import GarbageBin from '$lib/components/icons/GarbageBin.svelte';
  import Pencil from '$lib/components/icons/Pencil.svelte';
  import Tooltip from '$lib/components/common/Tooltip.svelte';
  import Download from '$lib/components/icons/Download.svelte';
  import Reset from '$lib/components/icons/Reset.svelte';
  import Plus from '$lib/components/icons/Plus.svelte';

  // Control visibility of menu items
  export let showNewFolder: boolean = false;
  export let showRename: boolean = true;
  export let showExport: boolean = true;
  export let showClear: boolean = true;
  export let showDelete: boolean = true;
  let show = false;
</script>

<Dropdown
	bind:show
	on:change={(e) => {
		if (e.detail === false) {
			dispatch('close');
		}
	}}
>
	<Tooltip content={$i18n.t('More')}>
		<slot />
	</Tooltip>

	<div slot="content">
	<DropdownMenu.Content
			class="w-full max-w-[160px] rounded-lg px-1 py-1.5  z-50 bg-white dark:bg-gray-850 dark:text-white shadow-lg"
			sideOffset={-2}
			side="bottom"
			align="start"
        transition={flyAndScale}
        >
        {#if showNewFolder}
        <DropdownMenu.Item
          class="flex gap-2 items-center px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-md"
          on:click={() => { dispatch('add'); }}
        >
          <Plus strokeWidth="2" />
          <div class="flex items-center">{$i18n.t('New Folder')}</div>
        </DropdownMenu.Item>
        {/if}
        {#if showRename}
        <DropdownMenu.Item
          class="flex gap-2 items-center px-3 py-1.5 text-sm  cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-md"
          on:click={() => { dispatch('rename'); }}
        >
          <Pencil strokeWidth="2" />
          <div class="flex items-center">{$i18n.t('Rename')}</div>
        </DropdownMenu.Item>
        {/if}

        {#if showExport}
        <DropdownMenu.Item
          class="flex gap-2 items-center px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-md"
          on:click={() => { dispatch('export'); }}
        >
          <Download strokeWidth="2" />
          <div class="flex items-center">{$i18n.t('Export')}</div>
        </DropdownMenu.Item>
        {/if}
        {#if showClear}
        <DropdownMenu.Item
          class="flex gap-2 items-center px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-md"
          on:click={() => { dispatch('clear'); }}
        >
          <!-- Clear all chats in this folder -->
          <Reset strokeWidth="2" />
          <div class="flex items-center">{$i18n.t('Clear Chats')}</div>
        </DropdownMenu.Item>
        {/if}

        {#if showDelete}
        <DropdownMenu.Item
          class="flex  gap-2  items-center px-3 py-1.5 text-sm  cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-md"
          on:click={() => { dispatch('delete'); }}
        >
          <GarbageBin strokeWidth="2" />
          <div class="flex items-center">{$i18n.t('Delete')}</div>
        </DropdownMenu.Item>
        {/if}
		</DropdownMenu.Content>
	</div>
</Dropdown>
