<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { useLayout } from "@/layout/composables/layout";
import axios from "axios";

const { isDarkTheme } = useLayout();

const lineOptions = ref(null);
const applyLightTheme = () => {
    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: "#495057",
                },
            },
        },
        scales: {
            x: {
                ticks: {
                    color: "#495057",
                },
                grid: {
                    color: "#ebedef",
                },
            },
            y: {
                ticks: {
                    color: "#495057",
                },
                grid: {
                    color: "#ebedef",
                },
            },
        },
    };
};

watch(
    isDarkTheme,
    (val) => {
        if (val) {
            applyDarkTheme();
        } else {
            applyLightTheme();
        }
    },
    { immediate: true }
);
</script>

<template>
    <div class="grid">
        <div class="col-12 flex justify-content-between">
            <h2 class="mb-0 font-semibold">Projects</h2>
            <div class="flex gap-3">
                <Dropdown
                    v-model="selected_community"
                    :options="communities"
                    optionLabel="name"
                    placeholder="Selected community"
                    class="w-full md:w-14rem"
                />
                <Button label="Add" icon="pi pi-plus" rounded raised />
            </div>
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

                    <div class="flex gap-3 mt-1" v-else>
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

export default {
    mixins: [sharedMixin],
    data() {
        return {
            projects: [],
            selected_community: null,
            enrolled: false,
            loading: true,
        };
    },
    methods: {
        async fetchUserProjects(groupId) {
            try {
                const response = await axios.get(
                    `${env.BASE_URL}/SubGroupAPI_REST/rest/v1/subgroup/groupsubgroup/${groupId}`,
                    {
                        headers: {
                            "X-SubGroup-AppId": env.X_SubGroup_AppId,
                            "X-SubGroup-Key": env.X_SubGroup_Key,
                        },
                    }
                );
                this.projects = response.data.GroupSubGroup.subGroups;
                // console.log(this.projects);
            } catch (error) {
                console.error(error);
            }
        },
    },
    watch: {
        "$route.query.groupId": {
            immediate: true,
            async handler(newVal) {
                this.loading = true;
                await this.fetchUserProjects(this.$route.query.groupId);
                for (const community of this.communities) {
                    if (community.groupId == newVal) {
                        this.selected_community = community;
                        break;
                    }
                }
                this.loading = false;
                console.log(this.selected_community);
            },
        },
        selected_community: {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                this.$router.push({ query: { groupId: newVal.groupId } });
                }
            },
        },
    },
};
</script>

<style>
.p-timeline-event-opposite {
    flex: 0;
}
</style>
