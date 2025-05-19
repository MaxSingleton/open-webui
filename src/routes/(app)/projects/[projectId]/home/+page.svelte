<script lang="ts">
  import { page } from '$app/stores';
  $: projectId = $page.params.projectId;
</script>

<div class="px-6 py-4">
  <h2 class="text-xl font-semibold mb-4">Home</h2>
  <p>Project {projectId} Home content coming soon.</p>
</div>