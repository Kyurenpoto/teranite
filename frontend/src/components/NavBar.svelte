<script lang="ts">
  import NavLink from "./NavLink.svelte";
  import { hasAccount } from "../stores.js";

  let class_name = "";
  export { class_name as class };

  const l_nav = [
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

<header class="w-full mt-0 grid place-items-center {class_name}">
  <section class="flex flex-col gap-y-10">
    <nav class="w-[var(--grid-column-12)] h-20 flex flex-row items-center justify-between">
      <section class="nav-list">
        {#each l_nav as { image, link }}
          <NavLink link="{link}">
            {image}
          </NavLink>
        {/each}
      </section>
      <section class="nav-list">
        <button class="w-[var(--grid-column-3)] nav-link" on:click="{hasAccount.toggle}">account</button>
      </section>
    </nav>
    <slot />
  </section>
</header>
