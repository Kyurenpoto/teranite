<script lang="ts">
  import { hasAccount } from "../stores/hasAccount";
  import InfoNavBar from "./InfoNavBar.svelte";
  import NavBar from "./NavBar.svelte";
  import RestHeader from "./RestHeader.svelte";

  const redirects = ["/login/github/callback"];

  export let path = "";
</script>

<div class="min-h-screen w-[calc(100vw-var(--scrollbar-width))] flex flex-col bg-[#242424]">
  {#if !redirects.includes(path)}
    <NavBar class="bg-blue-900">
      {#if path === "/" && !$hasAccount}
        <RestHeader />
      {/if}
    </NavBar>
  {/if}
  <main>
    <slot />
  </main>
  {#if !redirects.includes(path)}
    <InfoNavBar class="bg-blue-900" />
  {/if}
</div>
