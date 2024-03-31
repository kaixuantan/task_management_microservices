<template>
    <div class="grid">
        <Toast />
        <div class="col-12 flex justify-content-between">
            <h2 class="mb-0 font-semibold" v-if="selected_community">All projects ({{
                selected_community.name.toUpperCase() }})</h2>
            <h2 class="mb-0 font-semibold" v-else>Fetching projects</h2>
            <div class="flex gap-3">
                <Dropdown v-model="selected_community" :options="communities" optionLabel="name"
                    placeholder="Selected community" class="w-full md:w-14rem shadow-1" />
                <Button label="Add" icon="pi pi-plus" @click="addProj = true" raised v-if="role === 'admin'"/>
            </div>
        </div>

        <Dialog v-model:visible="addProj" :style="{ width: '450px' }" header="Edit Project" :modal="true"
            class="p-fluid">
            <div class="field">
                <label for="name">Project Name</label>
                <InputText id="name" v-model.trim="addProj_name" required="true" autofocus />
            </div>
            <div class="field">
                <label for="description">Description</label>
                <Textarea id="description" v-model="addProj_description" required="true" rows="3" cols="20" />
            </div>
            <div class="field">
                <label for="size">Size</label>
                <InputNumber id="Size" v-model="addProj_size" required="true" rows="3" cols="20" />
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="addProj = false" />
                <Button label="Save" icon="pi pi-check" text @click="addProject" />
            </template>
        </Dialog>

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

        <div v-if="grp_projects.length == 0 && !loading">
            <div class="col-12">
                <h3 class="font-semibold">No projects to show!</h3>
            </div>
        </div>
        <div class="xl:col-4" v-for="(project, idx) in grp_projects" v-else>
            <Card style="overflow: hidden" class="shadow-2">
                <template #header>
                    <div class="p-4 flex justify-content-between align-items-center">
                        <div class="flex gap-2 align-items-center">
                            <Avatar :label="project.name.charAt(0).toUpperCase()" class="mr-2" size="large"
                                shape="circle" :style="{
                                    backgroundColor:
                                        colors[idx % colors.length],
                                }" />
                            <div>
                                <h5 class="mb-1 font-semibold">
                                    {{ project.name }}
                                </h5>
                            </div>
                        </div>
                        <Button v-if="userrole=='admin'" text rounded @click="editproject(project)">
                            <i class="pi pi-pencil text-500 text-xl"></i>
                        </Button>
                    </div>
                    <img alt="user header" src="https://cdn-icons-png.freepik.com/512/4946/4946348.png"
                        style="width: 50%; height: 50%; object-fit: contain; margin: 0 auto; display: block;" />
                </template>
                <template #title>Members: {{ project.subGroupUsers.length }} / {{ project.size }}</template>
                <template #content>
                    <p class="m-0">
                        <span class="block mb-1">Project description:</span>
                        {{ project.description }}
                    </p>
                </template>
                <template #footer>
                    <div class="flex mt-1 justify-content-between"
                        v-if="!isUserEnrolled(project) && userrole !== 'admin' && project.subGroupUsers.length <project.size">

                        <!-- v-if="!enrolled" -->
                        <AvatarGroup>
                            <!-- can change to name as well if name is filled -->
                            <Avatar v-for="(user,idx2) in project.subGroupUsers.slice(0,3)" :key="user.userId"
                                :label="user.username.charAt(0).toUpperCase()" size="large" shape="circle" :style="{
                                    backgroundColor:
                                        colors[idx2+2 % colors.length],
                                }" />
                            <Avatar :label="`+${project.subGroupUsers.length - 3}`" shape="circle" size="large"
                                v-if="project.subGroupUsers.length > 3" />
                        </AvatarGroup>
                        <Button label="Enrol" @click="enrol(project.subGroupId,userId, selected_community.groupId)" />
                    </div>

                    <div class="flex gap-3 mt-1" v-if="isUserEnrolled(project) && userrole !== 'admin'">
                        <Button label="Leave" severity="secondary" outlined class="w-full" @click="leaveproject" />
                        <Button label="View" class="w-full" @click="viewProject(project.subGroupId)" />
                    </div>

                    <div class="flex gap-3 mt-1" v-if="userrole == 'admin'">
                        <Button label="View" class="w-full" @click="viewProject(project.subGroupId)" />
                    </div>
                </template>
            </Card>
        </div>
    </div>
    <Dialog v-model:visible="editDialog" :style="{ width: '450px' }" header="Edit Project" :modal="true"
        class="p-fluid">
        <div class="field">
            <label for="name">Project Name</label>
            <InputText id="name" v-model.trim="selectedproject.name" required="true" autofocus />
        </div>
        <div class="field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="selectedproject.description" required="true" rows="3" cols="20" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" text @click="editDialog = false" />
            <Button label="Save" icon="pi pi-check" text @click="saveproject" />
        </template>
    </Dialog>
</template>

<script>
import sharedMixin from "@/sharedMixin";
import axios from "axios";
import InputNumber from "primevue/inputnumber";
import { mapState } from 'vuex';

export default {
    mixins: [sharedMixin],
    data() {
        return {
            grp_projects: [],
            selected_community: null,
            enrolled: false,
            loading: true,
            userrole: sessionStorage.getItem('role'), 
            editDialog: false,
            selectedproject: null,
            addProj: false,
            addProj_name: null,
            addProj_description: null,
            addProj_size: null,
        };
    },
    computed: {
        ...mapState([
        'first_user_project'
    ])
    },
    methods: {
        async fetchGroupProjects(groupId) {
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
                if (response.data.Result.Success) {
                    this.grp_projects = response.data.GroupSubGroup.subGroups;
                }
                // console.log(this.projects);
            } catch (error) {
                console.error(error);
            }
        },
        viewProject(subGroupId) {
            this.$router.push({ name: 'project', query: { subGroupId: subGroupId } });
        },
        async addProject(){
            const data = {
                "groupId": this.$route.query.groupId,
                "name": this.addProj_name,
                "description": this.addProj_description,
                "size": this.addProj_size,
            }
            try {
                const response = await axios.post(
                    "https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup/", data,
                    {
                        headers: {
                            "X-SubGroup-AppId": env.X_SubGroup_AppId,
                            "X-SubGroup-Key": env.X_SubGroup_Key,
                        },
                    }
                );
                if (response.data.Result.Success) {
                    await this.fetchGroupProjects(this.$route.query.groupId);
                    this.addProj = false;
                    this.$toast.add({ severity: 'success', summary: 'Successful', detail: 'Project added', life: 3000 });
                }
            } catch (error) {
                console.error(error);
            }
        },
        async enrol(subGroupId, userId, groupId) {
            console.log(subGroupId, parseInt(userId), groupId);
            const email = sessionStorage.getItem("email");
            const username= sessionStorage.getItem("username");
            console.log(email, username);
            try {
                const response= await axios.post(
                    `http://localhost:5002/enrollment`,
                    {
                        subGroupId: subGroupId,
                        userId: parseInt(userId),
                        email: email,
                        username: username,

                    },
                    {
                        headers: {
                            "X-SubGroup-AppId": env.X_SubGroup_AppId,
                            "X-SubGroup-Key": env.X_SubGroup_Key,
                        },
                    }
                );
                console.log(response.data);
                await this.fetchGroupProjects(groupId);
                if (this.first_user_project === null) {
                    this.$store.commit('setFirstUserProject', subGroupId);
                }
                alert("Enrolled successfully")
            } catch (error) {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to enrol', life: 3000 });
            }
        },
        isUserEnrolled(project) {
        const userId = sessionStorage.getItem("userid");
        return project.subGroupUsers.some(user => user.userId === parseInt(userId));
    },
    async leaveproject(subGroupId) {
        console.log(subGroupId);
        const userId = sessionStorage.getItem("userid");
    try {
        console.log(subGroupId);
        console.log(userId)
        console.log(env.X_SubGroup_AppId)
        console.log(env.X_SubGroup_Key)
        const response = await axios.put(
            `https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup/unenrol/${subGroupId}`,
            {
                headers: {
                    "X-SubGroup-AppId": env.X_SubGroup_AppId,
                    "X-SubGroup-Key": env.X_SubGroup_Key,
                    "userId":userId
                },
            }
        );
        console.log(response.data);
        this.$toast.add({ severity: 'success', summary: 'Successful', detail: 'Left project', life: 3000 });
        // Refresh the list of projects after leaving
        await this.fetchGroupProjects(this.selected_community.groupId);
    } catch (error) {
        console.error('Error leaving project:', error);
        this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to leave project', life: 3000 });
    }},

    editproject(project){
        console.log(project)
        this.selectedproject = { ...project, projectId: project.subGroupId, name: project.name, description: project.description};
        this.editDialog = true;
        },
        async saveproject() {
  try {
    // Update the community
    console.log(this.selectedproject)
    console.log(this.selectedproject.projectId)
    console.log(this.selectedproject.name)
    console.log(this.selectedproject.description)
    console.log(this.selectedproject.size)
    console.log(this.selectedproject.subGroupUsers)
    let response = await axios.put(
      `${env.BASE_URL}/SubGroupAPI_REST/rest/v1/subgroup/${this.selectedproject.projectId}`,
      {
        name: this.selectedproject.name,
        groupId: this.selectedproject.groupId,
        description: this.selectedproject.description,
        size: this.selectedproject.size,
        subGroupUsers: this.selectedproject.subGroupUsers,
      },
      {
        headers: {
          "X-SubGroup-AppId": env.X_SubGroup_AppId,
          "X-SubGroup-Key": env.X_SubGroup_Key,
        },
      }
    );
    console.log(response.data);
    
    // Refresh the list of projects
    await this.fetchGroupProjects(this.selected_community.groupId);
    // alert("Project updated successfully")
    
    this.editDialog = false;

    // Show a success toast message
    this.$toast.add({ severity: 'success', summary: 'Successful', detail: 'Project updated', life: 3000 });
  } 
  catch (error) {
    console.error('Error updating Project:', error);
    // Show an error toast message
    this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to enrol', life: 3000 });
    await this.fetchGroupProjects(this.selected_community.groupId);

  }
},
    },
    watch: {
        "$route.query.groupId": {
            immediate: true,
            async handler(newVal) {
                this.loading = true;
                await this.fetchUserGroups();
                await this.fetchGroupProjects(this.$route.query.groupId);
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
