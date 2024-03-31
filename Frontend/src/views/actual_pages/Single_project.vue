<template>
    <div class="grid">
        <Toast position="bottom-right" group="br" />
        <div class="col-12 flex justify-content-between pb-0">
            <h2 class="mb-0 font-semibold" v-if="selected_project">{{ selected_project.name }}</h2>
            <h2 class="mb-0 font-semibold" v-else>Fetching project...</h2>
            <Dropdown
                v-if = "role === 'user'"
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
            <div class="flex justify-content-between align-items-center mb-3">
                <h3 class="font-semibold m-0">Tasks</h3>
                <Button label="Add" icon="pi pi-plus" rounded @click="redirectToCreateTask(this.$route.query.subGroupId)"/>
            </div>
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
                                <div class="text-justify overflow-hidden text-overflow-ellipsis mb-2">
                                    {{ task.description }}
                                </div>
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
                                    <Button @click="edittask(task)"
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
                                <div class="text-justify overflow-hidden text-overflow-ellipsis mb-2">
                                    {{ task.description }}
                                </div>
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
                                <div class="text-justify overflow-hidden text-overflow-ellipsis mb-2">
                                    {{ task.description }}
                                </div>
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

            <div class="card shadow-1 mt-5">
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
                        @uploader="onUpload($event)"
                        accept="application/pdf"
                        :customUpload="true"
                        :fileLimit="1"
                    >
                        <template #empty>
                            <p>Drag and drop project PDF here</p>
                        </template>
                    </FileUpload>
                </div>
                <div>
                    <h3 class="font-semibold">
                        Project summary & Ideas
                    </h3>
                    <div v-html="gemini_response" v-if="gemini_response" class="text-lg"></div>
                    <p class="font-medium" v-else>No PDF uploaded yet!</p> 
                </div>
            </div>
        </div>
        <div class="col-4">
            <div class="card shadow-1">
                <div
                    class="flex justify-content-between align-items-center mb-3"
                >
                    <h3 class="font-semibold m-0">About</h3>
                    <Button text rounded @click="editproject">
                        <i class="pi pi-pencil text-500 text-xl"></i>
                    </Button>
                </div>
                <div v-if="selected_project">
                    <p class="font-medium text-justify">
                        {{ selected_project.description }}
                    </p>
                    <h3 class="font-semibold mt-0">Members</h3>
                    <div class="flex align-items-center gap-3" v-for="(user,idx) in selected_project.subGroupUsers">
                        <!-- image="/images/avatars/panda.png" -->
                        <span class="font-medium text-lg">{{ idx+1 }}. {{ user.username.toUpperCase() }}</span>
                    </div>
                </div>
                <div v-else>
                    <p class="font-medium">Fetching project...</p>
                </div>
            </div>
        </div>
        <!-- 3 cards at the top of the screen -->
    </div>


    <Dialog v-model:visible="editDialog" :style="{ width: '450px' }" header="Edit Community" :modal="true" class="p-fluid">
  <div class="field">
    <label for="name">Task Name</label>
    <InputText id="name" v-model.trim="task.name" required="true" autofocus :disabled="!isCreatedByUser" />
  </div>
  <div class="field">
    <label for="description">Task Description</label>
    <Textarea id="description" v-model="task.description" required="true" rows="3" cols="20" :disabled="!isCreatedByUser" />
  </div>


  <div class="field">
    <label for="assignedUsers">Assigned Members</label>
    <MultiSelect
    v-model="selectedMembers"
    :options="projectMembers"
    optionLabel="username"
    placeholder="Select Members"
    :filter="true"
    class="w-full"
>
  <template #value="slotProps">
    <div
      class="inline-flex align-items-center py-1 px-2 bg-primary text-primary border-round mr-2"
      v-for="member in slotProps.value"
      :key="member.userId"
    >
      <div>{{ member.username}}</div>
    </div>
    <template v-if="!slotProps.value || slotProps.value.length === 0">
      <div class="p-1">Select Members</div>
    </template>
  </template>
  <template #option="slotProps">
    <div class="flex align-items-center">
      <div>{{ slotProps.option.username }}</div>
    </div>
  </template>
</MultiSelect>

<div class="field">
    <label for="status">Status</label>
    <Dropdown
        id="status"
        v-model="task.status"
        :options="statusOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="Select Status"
        class="w-full"
    />
</div>
  </div>


  <template #footer>
    <Button label="Cancel" icon="pi pi-times" text @click="editDialog = false" />
    <Button label="Save" icon="pi pi-check" text @click="savetask" />
  </template>
</Dialog>

<Dialog v-model:visible="editprojDialog" :style="{ width: '450px' }" header="Edit Project" :modal="true" class="p-fluid">
    <div class="field">
        <label for="name">Project Name</label>
        <InputText id="name" v-model.trim="newname" required="true" autofocus />
    </div>
    <div class="field">
        <label for="description">Description</label>
        <Textarea id="description" v-model="newdesc" required="true" rows="3" cols="20" />
    </div>
    <div class="field">
        <label for="capacity">Capacity</label>
        <InputText type="number" id="capacity" v-model="newcapacity" required="true" rows="3" cols="20" />
    </div>
    <template #footer>
        <Button label="Cancel" icon="pi pi-times" text @click="editprojDialog = false" />
        <Button label="Save" icon="pi pi-check" text @click="saveproject" />
    </template>
</Dialog>
</template>

<script>
import sharedMixin from "@/sharedMixin";
import axios from "axios";
import { marked } from "marked";
import DOMPurify from 'dompurify';

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
            gemini_response: "",
            editDialog: false,
            task: {},
            selectedMembers: [],
            projectMembers: [],
            selectedStatus: null,
            newname: "",
            newdesc: "",
            newcapacity: "",
            projtoedit:null,
            statusOptions: [
            { label: 'New', value: 'new' },
            { label: 'In Progress', value: 'in_progress' },
            { label: 'Completed', value: 'completed' },
        ],
            editprojDialog: false,

        };
    },
    mounted() {
        window.scrollTo(0, 0);

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
            } catch (error) {
                console.error(error);
            }
        },
        redirectToCreateTask(subGroupId) {
            this.$router.push({
                                path: '/create-task',
                                query: {
                                    "subGroupId": subGroupId,
                                }
                            });
        },
        async onUpload(event) {
            console.log(event);
            const file = event.files[0]; // Get the uploaded file
            try {
                const base64String = await this.processFile(file);
                const response = await this.uploadFile(base64String);
                 
                console.log(response);
                if (response.Result.Success) {
                    this.send_gemini();
                    this.$toast.add({
                        severity: "success",
                        summary: "Success",
                        detail: "File uploaded successfully.\nAn email will be sent once the document is processed.",
                        group: 'br',
                    });
                } else {
                    this.$toast.add({
                        severity: "error",
                        summary: "Error",
                        detail: "File upload failed",
                        life: 3000,
                        group: 'br',
                    });
                }
            } catch (error) {
                console.error(error);
            }
        },
        processFile(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = function() {
                    let base64String = this.result;
                    base64String = base64String.replace('data:application/pdf;base64,', ''); // Remove the prefix
                    resolve(base64String);
                }
                reader.onerror = reject;
                reader.readAsDataURL(file); // Read the file as a base64 string
            });
        },
        async uploadFile(base64String) {
            const data = {
                document: base64String,
                subGroupId: parseInt(this.$route.query.subGroupId),
                type: "pdf",
            };
            try {
                let response = await axios.post(`http://localhost:5000/ideas/upload`, data, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                return response.data;
            } catch (error) {
                console.error(error);
            }
        },
        send_gemini() {
            try {
                let response = axios.get(`http://localhost:5000/ideas/generate/${this.$route.query.subGroupId}/${this.userId}`, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => {
                    console.log(response.data);
                })
            } catch (error) {
                console.error(error);
            }
        },
        async fetch_gemini_response() {
            try {
                let response = await axios.get(`${env.BASE_URL}/DocAPI_REST/rest/v1/doc/subgrouptype/${this.$route.query.subGroupId}`, {
                    headers: {
                        "Content-Type": "application/json",
                        "X-Doc-AppId": env.X_Doc_AppId,
                        "X-Doc-Key": env.X_Doc_Key,
                        "type": "md",
                    }
                });
                console.log(response);
                if (response.data.Result.Success) {
                    const md_text = response.data.DocAPI.document;
                    const formatted_html = DOMPurify.sanitize(marked(md_text));
                    this.gemini_response = formatted_html;
                }
            } catch (error) {
                console.error(error);
            }
        },
        edittask(task) {
            this.task = { ...task };
            this.task.createdById = task.createdById;
            this.editDialog = true;
            console.log(this.task)
            if (task.status === 'New') {
            this.task.status = 'new';
        } else if (task.status === 'In Progress') {
            this.task.status = 'in_progress';
        } else if (task.status === 'Completed') {
            this.task.status = 'completed';
        }
        

        },
         editproject(project) {
            this.projtoedit = { ...project };
            this.newname = this.selected_project.name;
            this.newdesc = this.selected_project.description;
            this.newcapacity = this.selected_project.size;
            this.editprojDialog = true;
        },
        
        
        async saveproject() {
    try {
        // Update the project
        console.log(this.newname, this.newdesc, this.newcapacity)
        console.log(this.selected_project.groupId)
        console.log(this.selected_project.subGroupId)
        console.log(this.selected_project.subGroupUsers)
        if(this.newcapacity<1 || this.projectMembers.length>this.newcapacity){
            this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Capacity cannot be less than number of existing members or 0', life: 3000 });
            return;
        }
        let response = await axios.put(
            `${env.BASE_URL}/SubGroupAPI_REST/rest/v1/subgroup/${this.selected_project.subGroupId}`,
            {
                name: this.newname,
                groupId: this.selected_project.groupId,
                description: this.newdesc,
                size: this.newcapacity,
                subGroupUsers: this.selected_project.subGroupUsers,
            },
            {
                headers: {
                    "X-SubGroup-AppId": env.X_SubGroup_AppId,
                    "X-SubGroup-Key": env.X_SubGroup_Key,
                },
            }
        );
        console.log(response.data);

        // Close the edit dialog
        this.editprojDialog = false;

        // Refresh the project details
        await this.fetchUserProjects();
        for (const proj of this.user_projects) {
            if (proj.subGroupId == this.$route.query.subGroupId) {
                this.selected_project = proj;
                break;
            }
        }

        // Show a success toast message
        this.$toast.add({ severity: 'success', summary: 'Successful', detail: 'Project updated', life: 3000 });
    } catch (error) {
        console.error('Error updating project:', error);
        // Show an error toast message
        this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update project', life: 3000 });
    }
},
       async savetask(){
            try {

                // Update the task
                this.task.assignedUsers = this.selectedMembers;
                console.log(this.task)

                let response = await axios.put(
                    `${env.BASE_URL}/TaskAPI_REST/rest/v1/task/${this.task.taskId}`,
                    {
                        name: this.task.name,
                        description: this.task.description,
                        dueDateTime: this.task.dueDateTime,
                        subGroupId: this.task.subGroupId,
                        assignedUsers: this.selectedMembers,
                    },
                    {
                        headers: {
                            "X-Task-AppId": env.X_Task_AppId,
                            "X-Task-Key": env.X_Task_Key,
                        },
                    }
                );
                console.log(response.data);
                
                // Close the edit dialog
                this.editDialog = false;
                
                // Refresh the list of tasks
                await this.fetchProjectTasks(this.$route.query.subGroupId);
                
                // Show a success toast message
                this.$toast.add({ severity: 'success', summary: 'Successful', detail: 'Task updated', life: 3000 });
            } 
            catch (error) {
                console.error('Error updating task:', error);
                // Show an error toast message
                this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update task', life: 3000 });
            }
        },
        async fetchProject() {
            try {
                let response = await axios.get(
                    `${env.BASE_URL}/SubGroupAPI_REST/rest/v1/subgroup/${this.$route.query.subGroupId}`,
                    {
                        headers: {
                            "X-SubGroup-AppId": env.X_SubGroup_AppId,
                            "X-SubGroup-Key": env.X_SubGroup_Key,
                        },
                    }
                );
                if (response.data.Result.Success !== true) {
                    console.error("Error fetching project");
                } else {
                    this.selected_project = response.data.SubGroup
                }
            } catch (error) {
                console.error(error);
            }
        },
    },
    computed: {
    isCreatedByUser() {
        return this.task.createdById === parseInt(sessionStorage.getItem('userId'));
    },
},
    watch: {
        "$route.query.subGroupId": {
            immediate: true,
            async handler(newVal) {
                this.loading = true;
                if (this.role === "user") {
                    await this.fetchUserProjects();
                    for (const proj of this.user_projects) {
                        if (proj.subGroupId == newVal) {
                            this.selected_project = proj;
                            this.projectMembers= this.selected_project.subGroupUsers;
                            console.log(this.selected_project);
                            console.log(this.selected_project.subGroupUsers)
                            break;
                        }
                    }
                } else if (this.role === "admin") {
                    await this.fetchProject();
                }
                
                await this.fetchProjectTasks(this.$route.query.subGroupId);
                await this.fetch_gemini_response();
                this.tasks_in_progress = [];
                this.tasks_new = [];
                this.tasks_completed = [];
                this.sortTasksByStatus(this.proj_tasks);
                this.loading = false;
                // console.log(this.selected_project);
                // console.log(this.user_projects);
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
