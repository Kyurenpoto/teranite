<script lang="ts">
    let list = [
        { image: 'A', description: 'a' },
        { image: 'B', description: 'b' },
        { image: 'C', description: 'c' },
        { image: 'D', description: 'd' },
        { image: 'E', description: 'e' },
    ];
</script>

<style lang="postcss">
    .button {
        @apply w-[var(--grid-column-1)] h-[var(--grid-column-1)] bg-violet-500 mb-[70px];
    }
</style>

<section class="w-full flex flex-row gap-x-[var(--grid-gutter-width)] items-center justify-between">
    <button class="button">LButton</button>
    <section class="flex flex-row gap-x-[var(--grid-gutter-width)] justify-start">
        {#each list as { image, description }}
            <section class="flex flex-col gap-y-5">
                <div class="w-[var(--grid-column-2)] h-[var(--grid-column-2)] grid place-items-center bg-violet-500">{image}</div>
                <div class="w-[var(--grid-column-2)] h-[50px] grid place-items-center bg-violet-500">{description}</div>
            </section>
        {/each}
    </section>
    <button class="button">RButton</button>
</section>
