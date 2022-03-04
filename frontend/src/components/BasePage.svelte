<script lang="ts">
  import RestHeader from "./RestHeader.svelte";
  import NavBar from "./NavBar.svelte";
  import InfoNavBar from "./InfoNavBar.svelte";
  import { hasAccount } from "../stores";
</script>

<div class="min-h-screen w-[calc(100vw-var(--scrollbar-width))] flex flex-col bg-[#242424]">
  <NavBar class="bg-blue-900">
    {#if $hasAccount == false}
      <RestHeader />
    {/if}
  </NavBar>
  <main>
    <slot />
  </main>
  <InfoNavBar class="bg-blue-900" />
</div>
