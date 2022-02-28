<script lang="ts">
    let class_name = '';
    export { class_name as class };
</script>

<div class="min-h-screen w-[calc(100vw-var(--scrollbar-width))] flex flex-col {class_name}">
    <slot/>
</div>
