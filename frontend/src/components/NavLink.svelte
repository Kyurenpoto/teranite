<script lang="ts">
  let link = "";
  let width = "w-[var(--grid-column-1)]";
  export { link, width };
</script>

<a href="{link}" on:click>
  <div class="{width} nav-link">
    <slot/>
  </div>
</a>

<style lang="postcss">
  .nav-link {
    @apply h-full grid place-items-center bg-amber-500;
  }
</style>
