<section
  class="w-full h-[calc(100vh-240px)] mb-10 flex flex-row gap-x-[var(--grid-gutter-width)] items-center bg-fuchsia-700"
>
  <div class="flex flex-col gap-y-10">
    <div class="w-[var(--grid-column-6)] h-40 bg-red-500 grid place-items-center">cta</div>
    <div class="flex flex-row justify-between">
      <button>Sign up</button>
      <button>Explore Trends</button>
      <button>Search</button>
    </div>
  </div>
  <div class="w-[var(--grid-column-6)] h-[640px] bg-red-500 grid place-items-center">image</div>
</section>

<style lang="postcss">
  button {
    @apply w-[var(--grid-column-2)] h-20 bg-red-500 grid place-items-center;
  }
</style>
