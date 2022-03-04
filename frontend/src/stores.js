import { writable } from "svelte/store";

function createHasAccount() {
  const { subscribe, set, update } = writable(true);

  return {
    subscribe,
    toggle: () => update((x) => !x),
  };
}

export let hasAccount = createHasAccount();
