<style lang="postcss">
  .content-section {
    @apply flex flex-col mt-0 ml-auto mr-auto py-10 gap-y-20;
  }
</style>

<section class="content-section w-[var(--grid-column-12)]">
  <slot />
</section>
