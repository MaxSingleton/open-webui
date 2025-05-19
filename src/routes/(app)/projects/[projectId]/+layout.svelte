<script lang="ts">
  import { page } from '$app/stores';
  $: projectId = $page.params.projectId;
</script>

<svelte:head>
  <title>Project {projectId}</title>
</svelte:head>

<slot />