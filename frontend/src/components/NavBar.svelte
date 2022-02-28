<script lang="ts">
  import NavLink from './NavLink.svelte';

  let class_name = '';
  export { class_name as class };
  
  const l_nav = [
      { image: 'home', link: '/' },
      { image: 'rank', link: '/rank' },
      { image: 'explore', link: '/explore' },
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

<header class="h-20 w-full mt-0 grid place-items-center {class_name}">
  <nav class="w-[var(--grid-column-12)] h-full flex flex-row items-center justify-between">
    <section class="nav-list">
        {#each l_nav as { image, link }}
            <NavLink image={image} link={link}/>
        {/each}
    </section>
    <section class="nav-list">
        <NavLink image="account" link="/account" width="w-[var(--grid-column-3)]"/>
    </section>
  </nav>
</header>
