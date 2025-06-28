<script lang="ts">
  import { getContext, onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Plus from '$lib/components/icons/Plus.svelte';
  import Info from '$lib/components/icons/Info.svelte';
  const i18n = getContext('i18n');

  interface Project {
    id: string;
    name: string;
    meta?: { [key: string]: any };
    created_at: number;
    updated_at: number;
  }

  let projects: Project[] = [];
  let showCreateModal = false;
  let showEditModal = false;
  let editingId: string | null = null;
  let formData = {
    name: '',
    number: '',
    location: '',
    category: '',
    area: '',
    description: ''
  };

  function openCreateModal() {
    editingId = null;
    formData = { name: '', number: '', location: '', category: '', area: '', description: '' };
    showCreateModal = true;
  }

  function openEditModal(project: Project) {
    editingId = project.id;
    formData = {
      name: project.name,
      number: project.meta?.number ?? '',
      location: project.meta?.location ?? '',
      category: project.meta?.category ?? '',
      area: project.meta?.area ?? '',
      description: project.meta?.description ?? ''
    };
    showEditModal = true;
  }

  function closeModal() {
    showCreateModal = false;
    showEditModal = false;
    editingId = null;
  }

  async function fetchProjects() {
    try {
      const token = localStorage.token || '';
      const res = await fetch('/api/v1/folders/', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (res.ok) {
        projects = await res.json();
      } else {
        console.error('Failed to fetch projects');
      }
    } catch (e) {
      console.error('Error fetching projects', e);
    }
  }

  async function submitCreate() {
    if (!formData.name) return;
    try {
      const token = localStorage.token || '';
      const res = await fetch('/api/v1/folders/', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        const project = await res.json();
        await fetchProjects();
        closeModal();
        goto(`/projects/${project.id}/home`);
      } else {
        console.error('Error creating project');
      }
    } catch (e) {
      console.error('Error creating project', e);
    }
  }

  async function submitEdit() {
    if (!formData.name || !editingId) return;
    try {
      const token = localStorage.token || '';
      const res = await fetch(`/api/v1/folders/${editingId}/update`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        await fetchProjects();
        closeModal();
      } else {
        console.error('Error updating project');
      }
    } catch (e) {
      console.error('Error updating project', e);
    }
  }

  onMount(() => {
    fetchProjects();
  });
</script>

<svelte:head>
  <title>{$i18n?.t('Projects') ?? 'Projects'}</title>
</svelte:head>

<div class="p-6">
  <div class="flex justify-between items-center mb-6">
    <div class="flex items-center text-xl font-medium">
      {$i18n?.t('Projects') ?? 'Projects'}
      <span class="ml-2 text-lg font-medium text-gray-500 dark:text-gray-300">({projects.length})</span>
    </div>
    <button
      class="flex items-center space-x-1 px-3 py-2 rounded-xl hover:bg-gray-200 dark:hover:bg-gray-700 transition font-medium text-sm"
      on:click={openCreateModal}
    >
      <Plus class="size-4" />
      <span>{$i18n?.t('New Project') ?? 'New Project'}</span>
    </button>
  </div>
  {#if projects.length === 0}
    <div>
      <p class="text-gray-500">{$i18n?.t('No projects yet.') ?? 'No projects yet.'}</p>
    </div>
  {:else}
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      {#each projects as project}
        <div class="border rounded-lg p-4 flex flex-col justify-between bg-white dark:bg-gray-800">
          <div>
            <h3 class="text-lg font-semibold">{project.name}</h3>
            {#if project.meta?.description}
              <p class="text-sm text-gray-500 mt-1">{project.meta.description}</p>
            {/if}
          </div>
          <div class="flex justify-end mt-4 space-x-2">
            <button
              on:click={() => openEditModal(project)}
              class="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
              aria-label="Edit Project"
            >
              <Info class="size-5" />
            </button>
            <button
              on:click={() => goto(`/projects/${project.id}/home`)}
              class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              {$i18n?.t('Open') ?? 'Open'}
            </button>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

{#if showCreateModal}
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
      <h2 class="text-lg font-medium mb-4">{$i18n?.t('Create Project') ?? 'Create Project'}</h2>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1" for="name">{$i18n?.t('Project Name') ?? 'Project Name'}</label>
          <input id="name" type="text" bind:value={formData.name} class="w-full border rounded px-3 py-2" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1" for="number">{$i18n?.t('Project Number') ?? 'Project Number'}</label>
          <input id="number" type="text" bind:value={formData.number} class="w-full border rounded px-3 py-2" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1" for="location">{$i18n?.t('Project Location') ?? 'Project Location'}</label>
          <input id="location" type="text" bind:value={formData.location} class="w-full border rounded px-3 py-2" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1" for="category">{$i18n?.t('Project Category') ?? 'Project Category'}</label>
          <input id="category" type="text" bind:value={formData.category} class="w-full border rounded px-3 py-2" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1" for="area">{$i18n?.t('Project Area') ?? 'Project Area'}</label>
          <input id="area" type="text" bind:value={formData.area} class="w-full border rounded px-3 py-2" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1" for="description">{$i18n?.t('Project Description') ?? 'Project Description'}</label>
          <textarea id="description" bind:value={formData.description} class="w-full border rounded px-3 py-2" rows="3"></textarea>
        </div>
      </div>
      <div class="mt-6 flex justify-end space-x-2">
        <button class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600" on:click={closeModal}>
          {$i18n?.t('Cancel') ?? 'Cancel'}
        </button>
        <button class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700" on:click={submitCreate}>
          {$i18n?.t('Create') ?? 'Create'}
        </button>
      </div>
    </div>
  </div>
{/if}

{#if showEditModal}
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
      <h2 class="text-lg font-medium mb-4">{$i18n?.t('Edit Project') ?? 'Edit Project'}</h2>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1" for="name">{$i18n?.t('Project Name') ?? 'Project Name'}</label>
          <input id="name" type="text" bind:value={formData.name} class="w-full border rounded px-3 py-2" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1" for="description">{$i18n?.t('Project Description') ?? 'Project Description'}</label>
          <textarea id="description" bind:value={formData.description} class="w-full border rounded px-3 py-2" rows="3"></textarea>
        </div>
      </div>
      <div class="mt-6 flex justify-end space-x-2">
        <button class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600" on:click={closeModal}>
          {$i18n?.t('Cancel') ?? 'Cancel'}
        </button>
        <button class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700" on:click={submitEdit}>
          {$i18n?.t('Save') ?? 'Save'}
        </button>
      </div>
    </div>
  </div>
{/if}