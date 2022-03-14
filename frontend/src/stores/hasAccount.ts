import { writable } from "svelte/store";

function createHasAccount() {
  const { subscribe, set, update } = writable<Boolean>(localStorage.hasAccount === "true");

  return {
    subscribe,
    set,
    toggle: () => update((x) => !x),
  };
}

export const hasAccount = createHasAccount();

hasAccount.subscribe((x) => (localStorage.hasAccount = String(x)));
