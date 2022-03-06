import { writable } from "svelte/store";

function createHasAccount() {
  const { subscribe, update } = writable<Boolean>(localStorage.hasAccount === "true");

  return {
    subscribe,
    toggle: () => update((x) => !x),
  };
}

export let hasAccount = createHasAccount();

hasAccount.subscribe((x) => (localStorage.hasAccount = String(x)));
