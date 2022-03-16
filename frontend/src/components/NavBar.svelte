<script lang="ts">
  import { hasAccount } from "../stores/hasAccount";
  import NavLink from "./NavLink.svelte";

  let className = "";
  export { className as class };

  const lNav = [
    { image: "home", link: "/" },
    { image: "rank", link: "/rank" },
    { image: "explore", link: "/explore" },
  ];
</script>

<style lang="postcss">
  .nav-list {
    @apply h-full flex flex-row gap-x-[var(--grid-gutter-width)];
  }
  .nav-link {
    @apply h-full grid place-items-center bg-amber-500;
  }
</style>

<header class="w-full mt-0 grid place-items-center {className}">
  <section class="flex flex-col gap-y-10">
    <nav class="w-[var(--grid-column-12)] h-20 flex flex-row items-center justify-between">
      <section class="nav-list">
        {#each lNav as { image, link }}
          <NavLink link="{link}">
            {image}
          </NavLink>
        {/each}
      </section>
      <section class="nav-list">
        {#if $hasAccount === true}
          <button class="w-[var(--grid-column-3)] nav-link" on:click="{hasAccount.toggle}">logout</button>
        {:else}
          <a href="/login">
            <button class="w-[var(--grid-column-3)] nav-link">login</button>
          </a>
        {/if}
      </section>
    </nav>
    <slot />
  </section>
</header>
