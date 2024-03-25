<script setup>
import AppMenuItem from "./AppMenuItem.vue";
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item
                v-if="!item.separator"
                :item="item"
                :index="i"
            ></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>

<script>
import AppMenuItem from "./AppMenuItem.vue";
import sharedMixin from "@/sharedMixin";

export default {
    mixins: [sharedMixin],
    data() {
        return {
            first_user_project: null,
        }
    },
    computed: {
        model() {
            return [
                {
                    label: "Pages",
                    items: [
                        { label: "Home", icon: "pi pi-fw pi-home", to: "/" },
                        {
                            label: "Community",
                            icon: "pi pi-fw pi-users",
                            to: "/community",
                        },
                        {
                            label: "Projects",
                            icon: "pi pi-fw pi-book",
                            to: "/project",
                            query: { subGroupId: this.first_user_project },
                        },
                    ],
                },
            ]
        },
    },
    async created() {
        await this.fetchUserProjects();
        if (this.user_projects && this.user_projects.length > 0) {
            this.first_user_project = this.user_projects[0].subGroupId;
        } else {
            console.log('No user projects found');
        }
        
    }
}
</script>
