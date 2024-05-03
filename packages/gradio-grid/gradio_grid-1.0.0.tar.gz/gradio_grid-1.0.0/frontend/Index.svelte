<script lang="ts">
    import { onMount } from 'svelte';

    export let elem_id: string;
    export let elem_classes: string[] = [];
    export let visible = true;
    export let variant: "default" | "panel" = "default";
    export let columns = 3;
    let gridTemplateColumns = '1fr '.repeat(columns).trim();

    onMount(() => {
        let gridTemplateColumns = '1fr '.repeat(columns).trim() + '!important';
        const style = document.createElement('style');
        document.head.appendChild(style);
        style.innerHTML = `#${elem_id} .form {grid-template-columns: ${gridTemplateColumns};}`;
    });
</script>

<div
    class:panel={variant === "panel"}
    class:hide={!visible}
    id={elem_id}
    class={elem_classes.join(" ")}
>
    <slot class="test" />
</div>

<style>

    div > :global(*) {
        display: grid !important;
        width: var(--size-full) !important;
    }
    
    .hide {
        display: none;
    }
    
    .panel {
        border-radius: var(--container-radius);
        background: var(--background-fill-secondary);
        padding: var(--size-2);
    }
    
    .stretch {
        align-items: stretch;
    }
    
</style>
