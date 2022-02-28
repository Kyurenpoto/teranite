<script lang="ts">
    const scrollSize = (parseInt(getComputedStyle(document.documentElement).getPropertyValue('--grid-column-width')) +
                        parseInt(getComputedStyle(document.documentElement).getPropertyValue('--grid-gutter-width'))) * 2;
    let list = [
        { image: 'A', description: 'a' },
        { image: 'B', description: 'b' },
        { image: 'C', description: 'c' },
        { image: 'D', description: 'd' },
        { image: 'E', description: 'e' },
        { image: 'F', description: 'f' },
    ];
    let idx = 0;
    let scrollable: HTMLElement;
</script>

<style lang="postcss">
    .button {
        @apply w-[var(--grid-column-1)] h-[var(--grid-column-1)] bg-violet-500 mb-[70px];
    }
</style>

<section class="w-full flex flex-row gap-x-[var(--grid-gutter-width)] items-center justify-between">
    <button class="button" on:click="{()=>{scrollable.scrollLeft-=scrollSize; idx-=1;}}" disabled="{idx==0}">LButton</button>
    <section class="w-[var(--grid-column-10)] flex flex-row gap-x-[var(--grid-gutter-width)] justify-start overflow-hidden" bind:this="{scrollable}">
        {#each list as { image, description }}
            <section class="flex flex-col gap-y-5">
                <div class="w-[var(--grid-column-2)] h-[var(--grid-column-2)] grid place-items-center bg-violet-500">{image}</div>
                <div class="w-[var(--grid-column-2)] h-[50px] grid place-items-center bg-violet-500">{description}</div>
            </section>
        {/each}
    </section>
    <button class="button" on:click="{()=>{scrollable.scrollLeft+=scrollSize; idx+=1;}}" disabled="{idx+5==list.length}">RButton</button>
</section>
