<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	import { flyAndScale } from '$lib/utils/transitions';

export let show = true;
export let size = 'md';
export let containerClassName = 'p-3';
export let className = 'bg-white dark:bg-gray-900 rounded-2xl';
// Optional custom dimensions for the modal content (overrides size)
export let modalWidth: string | undefined;
export let modalHeight: string | undefined;

	let modalElement = null;
	let mounted = false;

	const sizeToWidth = (size) => {
		if (size === 'full') {
			return 'w-full';
		}
		if (size === 'xs') {
			return 'w-[16rem]';
		} else if (size === 'sm') {
			return 'w-[30rem]';
		} else if (size === 'md') {
			return 'w-[42rem]';
		} else {
			return 'w-[56rem]';
		}
	};

	const handleKeyDown = (event: KeyboardEvent) => {
		if (event.key === 'Escape' && isTopModal()) {
			console.log('Escape');
			show = false;
		}
	};

	const isTopModal = () => {
		const modals = document.getElementsByClassName('modal');
		return modals.length && modals[modals.length - 1] === modalElement;
	};

	onMount(() => {
		mounted = true;
	});

	$: if (show && modalElement) {
		document.body.appendChild(modalElement);
		window.addEventListener('keydown', handleKeyDown);
		document.body.style.overflow = 'hidden';
	} else if (modalElement) {
		window.removeEventListener('keydown', handleKeyDown);
		document.body.removeChild(modalElement);
		document.body.style.overflow = 'unset';
	}

	onDestroy(() => {
		show = false;
		if (modalElement) {
			document.body.removeChild(modalElement);
		}
	});
</script>

{#if show}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
  <div
    bind:this={modalElement}
    class="modal fixed inset-0 bg-black/60 {containerClassName} flex justify-center z-9999 overflow-y-auto overscroll-contain"
    in:fade={{ duration: 10 }}
    on:mousedown={() => { show = false; }}
  >
    <div
      class="m-auto shadow-3xl min-h-fit scrollbar-hidden {className}"
      in:flyAndScale
      on:mousedown={(e) => { e.stopPropagation(); }}
      style="{modalWidth ? `width: ${modalWidth};` : ''}{modalHeight ? `height: ${modalHeight};` : ''}"
    >
      <slot />
    </div>
  </div>
{/if}

<style>
	.modal-content {
		animation: scaleUp 0.1s ease-out forwards;
	}

	@keyframes scaleUp {
		from {
			transform: scale(0.985);
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}
</style>
