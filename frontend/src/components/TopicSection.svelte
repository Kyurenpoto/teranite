<script lang="ts">
    let class_name = '';
    let title = '';
    export { class_name as class, title };
</script>

<style lang="postcss">
    .topic-section {
        @apply w-full flex flex-col mt-0 mb-auto gap-y-5;
    }
    .title {
        --title-height: 100px;
        @apply grid place-items-center bg-red-500 h-[var(--title-height)] ;
    }
</style>

<section class="topic-section {class_name}">
    <div class="title w-[var(--grid-column-4)]">
        <h2>{title}</h2>
    </div>
    <slot/>
</section>