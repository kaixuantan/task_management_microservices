<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { useLayout } from "@/layout/composables/layout";
import axios from "axios";

const { isDarkTheme } = useLayout();

const activities = ref(
    [
        {
            status: "Ben Simmons",
            date: "15/10/2020 10:30",
            task_id: "121",
            task_desc: "fix the bug on the homepage",
            project: "Project Meelo",
            image: "/images/avatars/panda.png",
        },
        {
            status: "John Tan",
            date: "15/10/2020 14:00",
            task_id: "2",
            task_desc: "added paragraph",
            project: "Project Kivu",
            image: "/images/avatars/fox.png",
        },
        {
            status: "Paul Lynette",
            date: "15/10/2020 16:15",
            task_id: "10",
            task_desc: "deleted old design",
            project: "Project Hapara",
            image: "/images/avatars/woman.png",
        },
    ].reverse()
);

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
            <Button label="Add" icon="pi pi-plus" rounded raised />
        </div>
        <!-- 3 cards at the top of the screen -->
        <div class="xl:col-4" v-for="n in 3">
            <Card style="overflow: hidden" class="shadow-2">
                <template #header>
                    <div
                        class="p-4 flex justify-content-between align-items-center"
                    >
                        <div class="flex gap-2 align-items-center">
                            <Avatar
                                :label="communities[n].charAt(0)"
                                class="mr-2"
                                size="large"
                                shape="circle"
                                :style="{
                                    backgroundColor: colors[n % colors.length],
                                }"
                            />
                            <div>
                                <h5 class="mb-1 font-semibold">
                                    Project Meelo
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
                <template #title>Members: </template>
                <template #content>
                    <p class="m-0">Project description</p>
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
export default {
    data() {
        return {
            communities: [
                "ESD",
                "ITSA",
                "MATH",
                "PHYSICS",
                "CHEMISTRY",
                "BIOLOGY",
                "GEOGRAPHY",
                "HISTORY",
                "ENGLISH",
                "FRENCH",
                "SPANISH",
                "GERMAN",
                "ART",
            ],
            colors: [
                "#ece9fc",
                "#dee9fc",
                "#d8e2ef",
                "#e8e9fc",
                "#f2e9fc",
                "#f9e9fc",
                "#fce9f2",
                "#fce9e8",
                "#f9e9e2",
                "#f2e9d8",
            ],
            projects: [],
            enrolled: false,
        };
    },
    async created() {
        try {
            const response = await axios.get(
                "https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup",
                {
                    headers: {
                        "X-SubGroup-AppId": env.X_SubGroup_AppId,
                        "X-SubGroup-Key": env.X_SubGroup_Key,
                        // any other headers you need to set
                    },
                }
            );
            this.projects = response.data.SubGroup;
            console.log(this.projects);
        } catch (error) {
            console.error(error);
        }
    },
};
</script>

<style>
.p-timeline-event-opposite {
    flex: 0;
}
</style>
