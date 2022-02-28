<script lang="ts">
  import TopicSection from "./TopicSection.svelte";

  const boxes = [
    { name: "Daily", link: "/daily" },
    { name: "Weekly", link: "/weekly" },
    { name: "Monthly", link: "/monthly" },
  ];
</script>

<TopicSection class="bg-amber-500" title="Recently">
  <div class="flex flex-row gap-x-[var(--grid-gutter-width)]">
    {#each boxes as { name, link }}
      <a href="{link}">
        <div class="box w-[var(--grid-column-4)]">
          <h2>{name}</h2>
        </div>
      </a>
    {/each}
  </div>
</TopicSection>

<style lang="postcss">
  .box {
    --box-height: 360px;
    @apply grid place-items-center bg-fuchsia-400 h-[var(--box-height)];
  }
</style>
