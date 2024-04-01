<script setup>
import { useLayout } from '@/layout/composables/layout';
import { computed } from 'vue';

const { layoutConfig } = useLayout();

const logoUrl = computed(() => {
    return `/logo-dark.svg`;
});
</script>

<template>
    <div class="layout-footer">
        <img src="/demo/images/TaskMaster.png" alt="Logo" height="40" class="mr-2" />
        <span class="font-medium ml-2">TaskMaster</span>
    </div>
</template>
<style lang="scss" scoped></style>
