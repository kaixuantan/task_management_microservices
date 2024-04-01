<script setup>
import { useRouter } from 'vue-router';

const router = useRouter(); 
const redirectToCreateCommunity = () => {
    router.push({ name: 'create community' });
}
const userole= sessionStorage.getItem('role');
console.log(userole)
</script>

<template>
    <div class="grid">
        <div class="col-12 flex justify-content-between">
            <h2 class="mb-0 font-semibold">Communities</h2>
            <Button v-if="userole == 'admin'" label="Create" icon="pi pi-plus" rounded raised @click="redirectToCreateCommunity"/>
        </div>
        
        <!-- Display message when there are no communities -->
        <div class="col-12" v-if="communities.length === 0">
        <p class="text-center text-gray-500">No communities to display</p>
        <div class="flex justify-content-center">
        <img src="/demo/images/No-result-found.png" alt="No results found" style="max-width: 300px; height: auto;"/>
        </div>
        </div>

        <div class="xl:col-4" v-else v-for="(community,idx) in communities">
            <Card style="overflow: hidden" class="shadow-2">
                <template #header>
                    <div class="p-4 flex justify-content-between align-items-center">
                        <div class="flex gap-2 align-items-center">
                            <Avatar
                            :label="community.name.charAt(0).toUpperCase()"
                            class="mr-2"
                            size="large"
                            shape="circle"
                            :style="{
                                backgroundColor: colors[idx % colors.length],
                            }"
                            />
                            <div>
                                <h5 class="mb-1 font-semibold">{{ community.name }}</h5>
                                <!-- <p class="m-0 text-500">Organisation</p> -->
                            </div>
                        </div>
                        <Button v-if="userole == 'admin'" text @click="editcommunity(community)" >
                            <i class="pi pi-pencil text-500 text-xl"></i>
                        </Button>
                    </div>
                    <img alt="user header" src="https://cdn-icons-png.freepik.com/512/2592/2592465.png" style="width: 50%; height: 50%; object-fit: contain; margin: 0 auto; display: block;" />
                </template>
                <template #title>Community Size: {{ community.size }}</template>
                <template #subtitle>
                    <span class="block mb-1">Community Description:</span> 
                    {{ community.description }} 
                </template>
                <!-- <template #content>
                    <p class="m-0">
                        Description about community
                    </p>
                </template> -->
                <template #footer>
                    <div class="flex mt-1 justify-content-end">
                        <Button label="View" @click="viewProjects(community.groupId)"/>
                    </div>
                </template>
            </Card>
        </div>
    </div>


    <Dialog v-model:visible="editDialog" :style="{ width: '450px' }" header="Edit Community" :modal="true" class="p-fluid">
  <div class="field">
    <label for="name">Community Name</label>
    <InputText id="name" v-model.trim="selectedCommunity.name" required="true" autofocus />
  </div>
  <div class="field">
    <label for="description">Description</label>
    <Textarea id="description" v-model="selectedCommunity.description" required="true" rows="3" cols="20" />
  </div>
  <template #footer>
    <Button label="Cancel" icon="pi pi-times" text @click="editDialog = false" />
    <Button label="Save" icon="pi pi-check" text @click="saveCommunity" />
  </template>
</Dialog>
</template>

<script>
import axios from 'axios';
import sharedMixin from "@/sharedMixin";

export default {
    mixins: [sharedMixin],
    data() {
        return {
    editDialog: false,
    selectedCommunity: null,
        };
    },
    methods: {
        viewProjects(groupId) {
            this.$router.push({ name: 'projects', query: { groupId: groupId } });
        },
        editcommunity(community){
            this.selectedCommunity = { ...community, groupId: community.groupId };
            this.editDialog = true;
        },
        async saveCommunity() {
  try {
    // Update the community
    console.log(this.selectedCommunity)
    let response = await axios.put(
      `${env.BASE_URL}/GroupAPI_REST/rest/v1/group/${this.selectedCommunity.groupId}`,
      {
        createdById: this.selectedCommunity.createdById,
        name: this.selectedCommunity.name,
        createdDateTime: this.selectedCommunity.createdDateTime,
        description: this.selectedCommunity.description,
        size: this.selectedCommunity.size,

      },
      {
        headers: {
          "X-Group-AppId": env.X_Group_AppId,
          "X-Group-Key": env.X_Group_Key,
        },
      }
    );
    console.log(response.data);
    
    // Close the edit dialog
    this.editDialog = false;
    
    // Refresh the list of communities
    await this.fetchUserGroups();
    
    // Show a success toast message
    this.$toast.add({ severity: 'success', summary: 'Successful', detail: 'Community updated', life: 3000 });
  } 
  catch (error) {
    console.error('Error updating community:', error);
    // Show an error toast message
    this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update community', life: 3000 });
  }
},
    },
    async created() {
        await this.fetchUserGroups();
    },


};
</script>

<style>
.p-timeline-event-opposite {
    flex: 0;
}
</style>
