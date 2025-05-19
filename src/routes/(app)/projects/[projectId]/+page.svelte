<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  onMount(() => {
    const id = $page.params.projectId;
    goto(`/projects/${id}/home`);
  });
</script>