<template>
    <div class="grid">
        <div class="col-12 flex justify-content-between">
            <h2 class="mb-0 font-semibold">Project {{  }}</h2>
            <Dropdown
                    v-model="selected_project"
                    :options="user_projects"
                    optionLabel="name"
                    placeholder="Selected project"
                    class="w-full md:w-14rem shadow-1"
            />
        </div>
        <div class="col-12 py-0">
            <Divider class="text-900"/>
        </div>
        <!-- 3 cards at the top of the screen -->
        <div class="xl:col-4" v-for="n in 3" v-if="loading">
            <div class="border-round border-1 surface-border p-4 surface-card shadow-1">
                <div class="flex mb-3 gap-3">
                    <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
                    <div class="flex align-items-center">
                        <Skeleton width="10rem" height="1.5rem" class="mb-2"></Skeleton>
                    </div>
                </div>
                <Skeleton width="100%" height="20rem" class="mb-3"></Skeleton>
                <div>
                    <Skeleton width="50%" height="1.5rem"></Skeleton>
                </div>
                <div class="flex justify-content-end mt-3">
                    <Skeleton width="4rem" height="2rem"></Skeleton>
                </div>
            </div>
        </div>

        <div class="xl:col-4" v-for="(project, idx) in projects" v-else>
            <Card style="overflow: hidden" class="shadow-2">
                <template #header>
                    <div
                        class="p-4 flex justify-content-between align-items-center"
                    >
                        <div class="flex gap-2 align-items-center">
                            <Avatar
                                :label="project.name.charAt(0).toUpperCase()"
                                class="mr-2"
                                size="large"
                                shape="circle"
                                :style="{
                                    backgroundColor:
                                        colors[idx % colors.length],
                                }"
                            />
                            <div>
                                <h5 class="mb-1 font-semibold">
                                    {{ project.name }}
                                </h5>
                            </div>
                        </div>
                        <Button text rounded>
                            <i class="pi pi-pencil text-500 text-xl"></i>
                        </Button>
                    </div>
                    <img
                        alt="user header"
                        src="https://espanol.verizon.com/learning/_next/static/images/87c8be7b206ab401b295fd1d21620b79.jpg"
                        style="width: 100%; height: 100%; object-fit: contain"
                    />
                </template>
                <template #title>Members: {{ project.size }}</template>
                <template #content>
                    <p class="m-0">
                        {{ project.description }}Project description
                    </p>
                </template>
                <template #footer>
                    <div
                        class="flex mt-1 justify-content-between"
                        v-if="!enrolled"
                    >
                    <!-- v-if="!enrolled" -->
                        <AvatarGroup>
                            <Avatar
                                image="/images/avatars/panda.png"
                                size="large"
                                shape="circle"
                            />
                            <Avatar
                                image="/images/avatars/fox.png"
                                size="large"
                                shape="circle"
                            />
                            <Avatar
                                image="/images/avatars/woman.png"
                                size="large"
                                shape="circle"
                            />
                            <Avatar label="+2" shape="circle" size="large" />
                        </AvatarGroup>
                        <Button label="Enroll" />
                    </div>

                    <!-- v-else -->
                    <div class="flex gap-3 mt-1">
                        <Button
                            label="Leave"
                            severity="secondary"
                            outlined
                            class="w-full"
                        />
                        <Button label="View" class="w-full" />
                    </div>
                </template>
            </Card>
        </div>
    </div>
</template>

<script>
import sharedMixin from "@/sharedMixin";
import axios from "axios";

export default {
    mixins: [sharedMixin],
    data() {
        return {
            selected_project: null,
            enrolled: false,
            loading: true,
        };
    },
    methods: {
    },
    watch: {
        "$route.query.subGroupId": {
            immediate: true,
            async handler(newVal) {
                this.loading = true;
                // await this.fetchUserProjects(this.$route.query.groupId);
                for (const proj of this.user_projects) {
                    if (proj.subGroupId == newVal) {
                        this.selected_project = proj;
                        break;
                    }
                }
                this.loading = false;
                console.log(this.selected_project);
            },
        },
        selected_project: {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                this.$router.push({ query: { subGroupId: newVal.subGroupId } });
                }
            },
        },
    },
};
</script>

<style scoped>
.p-divider {
    border-top: 1px solid 
    #475569;
}
</style>
