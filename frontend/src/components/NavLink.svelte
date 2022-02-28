<script lang="ts">
  let image = '';
  let link = '';
  let width = 'w-[var(--grid-column-1)]';
  export { image, link, width };
</script>

<style lang="postcss">
  .nav-link {
    @apply h-full grid place-items-center bg-amber-500;
  }
</style>

<a href="{link}" on:click>
  <div class="{width} nav-link">{image}</div>
</a>

