<script lang="ts">
  export let link = "";
  export let width = "w-[var(--grid-column-1)]";
</script>

<style lang="postcss">
  .nav-link {
    @apply h-full grid place-items-center bg-amber-500;
  }
</style>

<a href="{link}" class="{width} nav-link" on:click>
  <slot />
</a>
