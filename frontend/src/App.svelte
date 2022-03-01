<script lang="ts">
  import MainPage from "./routes/MainPage.svelte";
</script>

<MainPage />

<style lang="postcss" global>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;

  :root {
    --grid-column-width: 92px;
    --grid-gutter-width: 30px;
    --grid-column-cnt: 12;
    --scrollbar-width: calc(100vw - 100%);

    --grid-column-1: var(--grid-column-width);
    --grid-column-2: calc(calc(var(--grid-column-width) * 2) + var(--grid-gutter-width));
    --grid-column-3: calc(calc(var(--grid-column-width) * 3) + calc(var(--grid-gutter-width) * 2));
    --grid-column-4: calc(calc(var(--grid-column-width) * 4) + calc(var(--grid-gutter-width) * 3));
    --grid-column-5: calc(calc(var(--grid-column-width) * 5) + calc(var(--grid-gutter-width) * 4));
    --grid-column-6: calc(calc(var(--grid-column-width) * 6) + calc(var(--grid-gutter-width) * 5));
    --grid-column-7: calc(calc(var(--grid-column-width) * 7) + calc(var(--grid-gutter-width) * 6));
    --grid-column-8: calc(calc(var(--grid-column-width) * 8) + calc(var(--grid-gutter-width) * 7));
    --grid-column-9: calc(calc(var(--grid-column-width) * 9) + calc(var(--grid-gutter-width) * 8));
    --grid-column-10: calc(calc(var(--grid-column-width) * 10) + calc(var(--grid-gutter-width) * 9));
    --grid-column-11: calc(calc(var(--grid-column-width) * 11) + calc(var(--grid-gutter-width) * 10));
    --grid-column-12: calc(calc(var(--grid-column-width) * 12) + calc(var(--grid-gutter-width) * 11));
  }
  html {
    @apply overflow-y-scroll;
  }
</style>
