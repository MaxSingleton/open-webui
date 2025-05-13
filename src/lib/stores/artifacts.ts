import { writable, type Writable } from 'svelte/store';
import { browser } from '$app/environment';

/**
 * Represents a saved artifact.
 */
export interface Artifact {
  id: string;
  name: string;
  content: string;
  createdAt: number;
}

// Initialize from localStorage if in browser
const initial: Artifact[] = browser
  ? JSON.parse(localStorage.getItem('artifacts') || '[]') || []
  : [];

/** List of saved artifacts */
export const artifacts: Writable<Artifact[]> = writable(initial);

// Persist artifacts to localStorage when changed
if (browser) {
  artifacts.subscribe((list) => {
    try {
      localStorage.setItem('artifacts', JSON.stringify(list));
    } catch {
      // ignore write errors
    }
  });
}

/** Whether the sidebar artifacts folder is open */
export const showArtifactsSidebar: Writable<boolean> = writable(false);

/** Whether to show the artifact detail modal */
export const showArtifactModal: Writable<boolean> = writable(false);

/** Currently selected artifact for detail view */
export const selectedArtifact: Writable<Artifact | null> = writable(null);

/** Add a new artifact */
export function addArtifact(artifact: Artifact) {
  artifacts.update((list) => [...list, artifact]);
}

/** Remove an artifact by id */
export function removeArtifact(id: string) {
  artifacts.update((list) => list.filter((a) => a.id !== id));
}

/** Open artifact detail modal for given artifact */
export function openArtifactDetail(artifact: Artifact) {
  selectedArtifact.set(artifact);
  showArtifactModal.set(true);
}