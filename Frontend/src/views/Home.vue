<script setup>
import { ref } from "vue";
import { useLayout } from "@/layout/composables/layout";

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
const projects = ref([
    {
        name: "Project Meelo",
        description: "create real estate landing page",
        icon: "pi pi-apple",
    },
    {
        name: "Project Kivu",
        description: "complete leadership assignment",
        icon: "pi pi-bitcoin",
    },
    {
        name: "Project Hapara",
        description: "design a new logo for the company",
        icon: "pi pi-bolt",
    },
]);

const calAttributes = ref([
    {
        highlight: true,
        dates: new Date(),
    },
]);
</script>

<template>
    <div class="grid">
        <div class="col-8">
            <div class="grid">
                <!-- 3 cards at the top of the screen -->
                <div class="col-12 lg:col-6 xl:col-4">
                    <div class="card mb-0 bg-orange-400 shadow-3">
                        <div
                            class="flex justify-content-between align-items-center mb-3"
                        >
                            <div>
                                <span class="text-900 text-2xl font-bold mb-3"
                                    >Tasks in Progress</span
                                >
                            </div>
                            <div
                                class="flex align-items-center justify-content-center bg-orange-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i class="pi pi-chart-bar text-500 text-xl"></i>
                            </div>
                        </div>
                        <span class="text-900 font-bold text-xl block mb-2"
                            >{{ tasks_in_progress.length }}
                        </span>
                    </div>
                </div>
                <div class="col-12 lg:col-6 xl:col-4">
                    <div class="card mb-0 bg-purple-300 shadow-3">
                        <div
                            class="flex justify-content-between align-items-center mb-3"
                        >
                            <div>
                                <span class="text-900 text-2xl font-bold mb-3"
                                    >New Assigned</span
                                >
                            </div>
                            <div
                                class="flex align-items-center justify-content-center bg-purple-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i class="pi pi-plus text-500 text-xl"></i>
                            </div>
                        </div>
                        <span class="text-900 font-bold text-xl block mb-2"
                            >{{ tasks_new.length }}
                        </span>
                    </div>
                </div>
                <div class="col-12 lg:col-6 xl:col-4">
                    <div class="card mb-0 bg-blue-300 shadow-3">
                        <div
                            class="flex justify-content-between align-items-center mb-3"
                        >
                            <div>
                                <span class="text-900 text-2xl font-bold mb-3"
                                    >Completed Tasks</span
                                >
                            </div>
                            <div
                                class="flex align-items-center justify-content-center bg-blue-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i
                                    class="pi pi-check-circle text-500 text-xl"
                                ></i>
                            </div>
                        </div>
                        <span class="text-900 font-bold text-xl block mb-2"
                            >{{ tasks_completed.length }}
                        </span>
                    </div>
                </div>

                <div class="col-12 flex justify-content-between">
                    <h2 class="mb-0 font-semibold">My Tasks</h2>
                </div>
                <div class="col-12">
                    <TabView>
                        <TabPanel header="In progress">
                            <div v-if="tasks_in_progress.length === 0">
                                <h5 class="mb-0 font-semibold">No tasks to show</h5>
                            </div>
                            <div
                                v-for="task in tasks_in_progress.slice(0,3)"
                                class="card shadow-1 flex align-items-center justify-content-between"
                            >
                                <div class="flex">
                                    <Avatar
                                        :label="task.name.charAt(0).toUpperCase()"
                                        class="mr-3"
                                        size="xlarge"
                                    />
                                    <div class="flex align-items-center">
                                        <div>
                                            <h5 class="mb-0 font-semibold">
                                                {{ task.name }}
                                            </h5>
                                            <p>{{ task.subGroupName }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </TabPanel>
                        <TabPanel header="New Assigned">
                            <div v-if="tasks_new.length === 0">
                                <h5 class="mb-0 font-semibold">No tasks to show</h5>
                            </div>
                            <div
                                v-for="task in tasks_new.slice(0,3)"
                                class="card shadow-1 flex align-items-center justify-content-between"
                            >
                                <div class="flex">
                                    <Avatar
                                        :label="task.name.charAt(0).toUpperCase()"
                                        class="mr-3"
                                        size="xlarge"
                                    />
                                    <div class="flex align-items-center">
                                        <div>
                                            <h5 class="mb-0 font-semibold">
                                                {{ task.name }}
                                            </h5>
                                            <p>{{ task.subGroupName }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </TabPanel>
                        <TabPanel header="Completed">
                            <div v-if="tasks_completed.length === 0">
                                <h5 class="mb-0 font-semibold">No tasks to show</h5>
                            </div>
                            <div
                                v-for="task in tasks_completed.slice(0,3)"
                                class="card shadow-1 flex align-items-center justify-content-between"
                            >
                                <div class="flex">
                                    <Avatar
                                        :label="task.name.charAt(0).toUpperCase()"
                                        class="mr-3"
                                        size="xlarge"
                                    />
                                    <div class="flex align-items-center">
                                        <div>
                                            <h5 class="mb-0 font-semibold">
                                                {{ task.name }}
                                            </h5>
                                            <p>{{ task.subGroupName }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </TabPanel>
                    </TabView>
                </div>
            </div>
        </div>
        <div class="col-4">
            <Panel>
                <h5>Communities</h5>
                <div class="flex-auto" v-if="sideMenuActive">
                    <a v-for="(community, index) in communities.slice(0, 5)" :key="index" :href="`/projects?groupId=${community.groupId}`">
                        <Avatar
                            :label="community.name.charAt(0).toUpperCase()"
                            class="mr-2"
                            size="large"
                            shape="circle"
                            :style="{
                                backgroundColor: colors[index % colors.length],
                            }"
                        />
                    </a>
                    <a v-if="communities.length > 5" :href="`/community`">
                        <Avatar
                            :label="`+${communities.length - 5}`"
                            class="mr-2"
                            size="large"
                            shape="circle"
                        />
                    </a>
                </div>
                <div v-else>
                    <a v-for="(community, index) in communities.slice(0, 7)" :key="index" :href="`/projects?groupId=${community.groupId}`">
                        <Avatar
                            :label="community.charAt(0)"
                            class="mr-2"
                            size="large"
                            shape="circle"
                            :style="{
                                backgroundColor: colors[index % colors.length],
                            }"
                        />
                    </a>
                    <a v-if="communities.length > 7" :href="`/community`">
                        <Avatar
                            :label="`+${communities.length - 7}`"
                            class="mr-2"
                            size="large"
                            shape="circle"
                        />
                    </a>
                </div>

                <Divider />
                <div>
                    <h5>Calendar</h5>
                    <!-- <VCalendar
                        view="weekly"
                        title-position="left"
                        expanded
                        :attributes="attributes"
                    /> -->
                    <VCalendar :attributes="calAttributes" expanded />
                </div>

                <!-- <Divider /> -->
                <!-- <div>
                    <div
                        class="flex justify-content-between align-items-center mb-2"
                    >
                        <h5 class="mb-0">Recent Activity</h5>
                        <Button label="View more" text></Button>
                    </div>

                    <Timeline :value="activities" class="w-full">
                        <template #content="slotProps">
                            <Card class="mb-3 surface-50 w-full">
                                <template #title>
                                    <div class="flex align-items-center gap-2">
                                        <Avatar
                                            :image="slotProps.item.image"
                                            class="mr-2"
                                            size="large"
                                            shape="circle"
                                        />
                                        {{ slotProps.item.status }}
                                    </div>
                                </template>
                                <template #subtitle>
                                    {{ slotProps.item.date }}
                                </template>
                                <template #content>
                                    <div class="">
                                        <div class="mb-1">
                                        <span
                                            class="font-bold text-500"
                                            >{{ slotProps.item.project }}</span
                                        >
                                        </div>
                                        <div class="mb-1">
                                            <span class="font-bold">Resolved </span>
                                            <span
                                                class="text-blue-600 font-semibold"
                                                >Task #{{ slotProps.item.task_id }}</span
                                            >
                                        </div>
                                        <span class="font-italic">{{ slotProps.item.task_desc }}</span>
                                    </div>
                                </template>
                            </Card>
                        </template>
                    </Timeline>
                </div> -->
            </Panel>
        </div>
    </div>
</template>

<script>
const { layoutState, layoutConfig } = useLayout();
import axios from "axios";
import sharedMixin from "@/sharedMixin";

export default {
    mixins: [sharedMixin],
    data() {
        return {
            tasks_in_progress: [],
            tasks_new: [],
            tasks_completed: [],
        };
    },
    methods: {

    },
    computed: {
        sideMenuActive() {
            return !(
                layoutState.staticMenuDesktopInactive.value &&
                layoutConfig.menuMode.value === "static"
            );
        },
    },
    async created() {
        window.scrollTo(0, 0);
        await this.fetchUserGroups();
        await this.fetchUserTasks();
        await this.fetchUserData();
        this.sortTasksByStatus(this.tasks);
        // console.log(this.tasks_in_progress);
        // console.log(this.tasks_new);
        // console.log(this.tasks_completed);
    },
};
</script>

<style>
.p-timeline-event-opposite {
    flex: 0;
}
</style>
