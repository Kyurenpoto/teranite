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

<header class="h-20 w-full mt-0 grid place-items-center {class_name}">
  <nav class="w-[var(--grid-column-12)] h-full flex flex-row items-center justify-between">
    <section class="nav-list">
      {#each l_nav as { image, link }}
        <NavLink link="{link}">
          {image}
        </NavLink>
      {/each}
    </section>
    <section class="nav-list">
      <div class="w-[var(--grid-column-3)] nav-link" on:click="{hasAccount.toggle}">account</div>
    </section>
  </nav>
</header>

<style lang="postcss">
  .nav-list {
    @apply h-full flex flex-row gap-x-[var(--grid-gutter-width)];
  }
  .nav-link {
    @apply h-full grid place-items-center bg-amber-500;
  }
</style>
