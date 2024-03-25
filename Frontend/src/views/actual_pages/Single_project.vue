<template>
    <div class="grid">
        <div class="col-12 flex justify-content-between pb-0">
            <h2 class="mb-0 font-semibold">{{ selected_project.name }}</h2>
            <Dropdown
                v-model="selected_project"
                :options="user_projects"
                optionLabel="name"
                placeholder="Selected project"
                class="w-full md:w-14rem shadow-1"
            />
        </div>
        <div class="col-12 py-0">
            <Divider />
        </div>
        <div class="col-8">
            <div class="flex justify-content-between align-items-center">
                <h3 class="font-semibold m-0">Tasks</h3>
                <Button label="Add" icon="pi pi-plus" rounded />
            </div>
            <Divider />
            <Accordion :activeIndex="0" :multiple="true">
                <AccordionTab header="New">
                    <div class="grid">
                        <div class="col-12" v-if="tasks_new.length === 0">
                            <p class="font-medium">No tasks to show!</p>
                        </div>
                        <div class="col-4" v-for="task in tasks_new">
                            <div class="card shadow-1 p-3">
                                <h6 class="font-semibold m-0">
                                    {{ task.name.toUpperCase() }}
                                </h6>
                                <p class="font-medium text-500">
                                    {{ task.createdByUsername }}
                                </p>
                                <p class="font-semibold mb-0">Description:</p>
                                <p class="text-justify">
                                    {{ task.description }}
                                </p>
                                <div class="mb-2">
                                    <span class="font-semibold">Due: </span
                                    ><span>{{
                                        this.formatDate(task.dueDateTime)
                                    }}</span>
                                </div>
                                <div class="mb-3">
                                    <span class="font-semibold block">Assigned: </span
                                    >
                                    <span v-for="(user,idx) in task.assignedUsers" >
                                        {{ user.assigneeUsername }}<span v-if="idx !== task.assignedUsers.length - 1">, </span>
                                    </span>
                                    
                                </div>
                                <div class="flex justify-content-end">
                                    <Button
                                        label="View"
                                        icon="pi pi-pencil"
                                        outlined
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </AccordionTab>
                <AccordionTab header="In progress">
                    <div class="grid">
                        <div
                            class="col-12"
                            v-if="tasks_in_progress.length === 0"
                        >
                            <p class="font-medium">No tasks to show!</p>
                        </div>
                        <div class="col-4" v-for="task in tasks_in_progress">
                            <div class="card shadow-1 p-3">
                                <h6 class="font-semibold m-0">
                                    {{ task.name.toUpperCase() }}
                                </h6>
                                <p class="font-medium text-500">
                                    {{ task.createdByUsername }}
                                </p>
                                <p class="font-semibold mb-0">Description:</p>
                                <p class="text-justify">
                                    {{ task.description }}
                                </p>
                                <div class="mb-2">
                                    <span class="font-semibold">Due: </span
                                    ><span>{{
                                        this.formatDate(task.dueDateTime)
                                    }}</span>
                                </div>
                                <div class="mb-3">
                                    <span class="font-semibold block">Assigned: </span
                                    >
                                    <span v-for="(user,idx) in task.assignedUsers">
                                        {{ user.assigneeUsername }} 
                                        <span v-if="idx !== task.assignedUsers.length - 1">, </span>
                                    </span>
                                    
                                </div>
                                <div class="flex justify-content-end">
                                    <Button
                                        label="View"
                                        icon="pi pi-pencil"
                                        outlined
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </AccordionTab>
                <AccordionTab header="Completed">
                    <div class="grid">
                        <div class="col-12" v-if="tasks_completed.length === 0">
                            <p class="font-medium">No tasks to show!</p>
                        </div>
                        <div class="col-4" v-for="task in tasks_completed">
                            <div class="card shadow-1 p-3">
                                <h6 class="font-semibold m-0">
                                    {{ task.name.toUpperCase() }}
                                </h6>
                                <p class="font-medium text-500">
                                    {{ task.createdByUsername }}
                                </p>
                                <p class="font-semibold mb-0">Description:</p>
                                <p class="text-justify">
                                    {{ task.description }}
                                </p>
                                <div class="mb-2">
                                    <span class="font-semibold">Due: </span
                                    ><span>{{
                                        this.formatDate(task.dueDateTime)
                                    }}</span>
                                </div>
                                <div class="mb-3">
                                    <span class="font-semibold block">Assigned: </span
                                    >
                                    <span v-for="(user,idx) in task.assignedUsers">
                                        {{ user.assigneeUsername }} 
                                        <span v-if="idx !== task.assignedUsers.length - 1">, </span>
                                    </span>
                                    
                                </div>
                                <div class="flex justify-content-end">
                                    <Button
                                        label="View"
                                        icon="pi pi-pencil"
                                        outlined
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </AccordionTab>
            </Accordion>
        </div>
        <div class="col-4">
            <div class="card shadow-1">
                <div
                    class="flex justify-content-between align-items-center mb-3"
                >
                    <h3 class="font-semibold m-0">About</h3>
                    <Button text rounded>
                        <i class="pi pi-pencil text-500 text-xl"></i>
                    </Button>
                </div>
                <p class="font-medium text-justify">
                    {{ selected_project.description }}
                </p>
                <h3 class="font-semibold mt-0">Members</h3>
                <div class="flex align-items-center gap-3" v-for="(user,idx) in selected_project.subGroupUsers">
                    <!-- image="/images/avatars/panda.png" -->
                    <span class="font-medium text-lg">{{ idx+1 }}. {{ user.username.toUpperCase() }}</span>
                </div>
            </div>

            <div class="card shadow-1">
                <div class="mb-3">
                    <div class="mb-3">
                        <h3 class="font-semibold inline">Ideas&nbsp</h3>
                        <span class="text-500"
                            >Powered by Gemini
                            <img
                                src="/icons/google-gemini-icon.png"
                                height="14px"
                                alt=""
                        /></span>
                    </div>
                    <FileUpload
                        name="demo[]"
                        url="/api/upload"
                        @upload="onAdvancedUpload($event)"
                        accept="application/pdf"
                        :maxFileSize="1000000"
                        :auto="true"
                        :showUploadButton="false"
                    >
                        <template #empty>
                            <p>Drag and drop project PDF here</p>
                        </template>
                    </FileUpload>
                </div>
                <div>
                    <h3 class="font-semibold">
                        Individual Contribution Report
                    </h3>
                    <Button
                        label="Generate"
                        icon="pi pi-file"
                        @click="viewProjects(community.groupId)"
                    />
                </div>
            </div>
        </div>
        <!-- 3 cards at the top of the screen -->
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
            proj_tasks: [],
            tasks_in_progress: [],
            tasks_new: [],
            tasks_completed: [],
        };
    },
    methods: {
        async fetchProjectTasks(subGroupId) {
            try {
                const response = await axios.get(
                    `${env.BASE_URL}/TaskAPI_REST/rest/v1/task/subgroup/${subGroupId}`,
                    {
                        headers: {
                            "X-Task-AppId": env.X_Task_AppId,
                            "X-Task-Key": env.X_Task_Key,
                        },
                    }
                );
                this.proj_tasks = response.data.TaskAPI;
                // console.log(this.projects);
            } catch (error) {
                console.error(error);
            }
        },
    },
    watch: {
        "$route.query.subGroupId": {
            immediate: true,
            async handler(newVal) {
                this.loading = true;
                for (const proj of this.user_projects) {
                    if (proj.subGroupId == newVal) {
                        this.selected_project = proj;
                        break;
                    }
                }
                await this.fetchProjectTasks(this.$route.query.subGroupId);
                this.tasks_in_progress = [];
                this.tasks_new = [];
                this.tasks_completed = [];
                this.sortTasksByStatus(this.proj_tasks);
                this.loading = false;
                console.log(this.selected_project);
                console.log(this.user_projects);
            },
        },
        selected_project: {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                    this.$router.push({
                        query: { subGroupId: newVal.subGroupId },
                    });
                }
            },
        },
    },
};
</script>

<style scoped>
.p-divider {
    border-top: 1px solid #475569;
}
</style>
