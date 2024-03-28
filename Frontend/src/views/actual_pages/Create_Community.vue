<script setup>
import { ref, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import axios from 'axios';
import { useRouter } from 'vue-router';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import { watch } from 'vue';
import router from '../../router';




const baseURL = 'https://personal-rc7vnnm9.outsystemscloud.com';
const postURL = 'http://localhost:5100';
const userAppId = env.X_User_AppId 
const userAppKey = env.X_User_Key
const headers = {
  'Content-Type': 'application/json',
  'X-User-AppId': userAppId,
  'X-User-Key': userAppKey,
  'X-Group-AppId': env.X_Group_AppId,
  'X-Group-Key': env.X_Group_Key,
  'X_SubGroup_AppId': env.X_SubGroup_AppId,
  'X_SubGroup_Key': env.X_SubGroup_Key,
};


//Fecth User Values
const fetchUsers = async () => {
  try {
    const response = await axios.get(`${baseURL}/UserAPI_REST/rest/v1/user/`,{ headers });
    console.log(response.data)
    users.value = response.data.User.map(user => ({
      name: user.username,
      userId: user.userId.toString(),
      email: user.email
    }));
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

//Users fetched from UserAPI
const users = ref([]);
//

//Option values for checkbox
const listofusers_forcheckbox = computed(() => users.value);
//

//Option values for subgroup checkbox
const listofusers_forsubgrpcheckbox = computed(() => {
  if (communitymembers.value) {
    return users.value.filter(user => communitymembers.value.some(member => member.userId === user.userId));
  }
  return [];
});
//



var groupid_toadd=0
const subgrpmembers= ref(null);
const createdById= sessionStorage.getItem('userid');
const createdByUsername= sessionStorage.getItem('username');
//VALUES TO SUBMIT
const groupdetails_submit={}
const subgroup_submit = ref([]);
const communitymembers= ref(null);
//



const toast = useToast();

const comname = ref('');
const comsize = ref(null);
const comdesc = ref('');
const communities = ref([]);
const subgrp_popup = ref(false);
const deletesubgrp_popup = ref(false);
const subgrp = ref({
    name: '',
    description: '',
    members: [],
    capacity: null
});
const submitted = ref(false);
const subsubmitted = ref(false);

const openNew = () => {
    subgrp.value = {};
    subsubmitted.value = false;
    subgrp_popup.value = true;
};

const hidesubgrp_popup = () => {
    subgrp_popup.value = false;
    subsubmitted.value = false;
};

const savesubgrp = () => {  
    console.log(subgrpmembers)
  subsubmitted.value = true;
  if (subgrp.value.name && subgrp.value.name.trim() && subgrp.value.capacity) {
      const formattedSubgroup = {
      name: subgrp.value.name,
      description: subgrp.value.description,
      size: subgrp.value.capacity,
      subGroupUsers: subgrpmembers.value!=null ? subgrpmembers.value.map(member => ({
        userId: parseInt(member.userId),
        username: member.name,
        email: member.email
      })) : []
    };
    

    if (subgrp.value.id) {
      // Update existing subgroup
      console.log('editing');
      const index = subgroup_submit.value.findIndex(c => c.id === subgrp.value.id);
      subgroup_submit.value[index] = formattedSubgroup;
      toast.add({ severity: 'success', summary: 'Successful', detail: 'Subgroup Updated', life: 3000 });
    } else {
      // Create new subgroup
      const newSubgroupId = groupid_toadd += 1;
      const newSubgroup = { ...formattedSubgroup, subGroupId: newSubgroupId, id: newSubgroupId };
      subgroup_submit.value.push(newSubgroup);
      console.log(subgroup_submit.value);
      toast.add({ severity: 'success', summary: 'Successful', detail: 'Subgroup Created', life: 3000 });
    }

    subgrp_popup.value = false;
    subgrp.value = {};
    subgrpmembers.value = [];

  }
};
    
const editsubgrp = (subgrpdata) => {
    subgrp.value = { ...subgrpdata };
    subgrp_popup.value = true;
};


const deletesubgrp = (datatodelete) => {
    console.log(datatodelete.id);
    subgroup_submit.value = subgroup_submit.value.filter(c => c.id !== datatodelete.id);
    deletesubgrp_popup.value = false;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'Subgroup Deleted', life: 3000 });
};




const submitform = async () => {
    if(!comname.value || !comsize.value || (communitymembers.value && comsize < communitymembers.value.length || !communitymembers.value)){
        submitted.value = true;
        return;
    }
  const groupdetails_submit = {
    name: comname.value,
    description: comdesc.value,
    size: comsize.value,
    createdById: createdById,
    createdByUsername: createdByUsername,
    createdDateTime: new Date().toISOString(),
    groupUsers: communitymembers.value.map(member => ({
    userId: parseInt(member.userId),
    username: member.name,
    email: member.email
    }))
  };
  console.log('communityy details to submit')
  console.log(groupdetails_submit)
  const groupUsers = communitymembers.value.map(member => parseInt(member.userId));

if(subgroup_submit.value.length==0){
    /* To update complex microservice if want to allow no subgroups
    try {
    const response = await axios.post(`${postURL}/groupcreation`, [
  groupdetails_submit,
  groupUsers
], {
  headers: {
    'Content-Type': 'application/json',
    'X-User-AppId': userAppId,
    'X-User-Key': userAppKey,
    'X-Group-AppId': env.X_Group_AppId,
    'X-Group-Key': env.X_Group_Key,
  }
});

    console.log('Response:', response.data);
    alert('Community Created Successfully')
    router.push('/community');
    // Handle the response as needed (e.g., show success message, redirect, etc.)

  } catch (error) {
    
    console.error('Error:', error);
    alert('Error creating community', error.message)
    // Handle the error (e.g., show error message)
  } */
  alert('Please add at least one subgroup')
  return
  }

  const subgroup_submit_formatted = subgroup_submit.value.map(subgroup => ({
    name: subgroup.name,
    description: subgroup.description,
    picture: subgroup.picture,
    size: subgroup.size,
    subGroupUsers: subgroup.subGroupUsers
  }));


  try {
    const response = await axios.post(`${postURL}/groupcreation`, [
  groupdetails_submit,
  subgroup_submit_formatted,
  groupUsers
], {
  headers: {
    'Content-Type': 'application/json',
    'X-User-AppId': userAppId,
    'X-User-Key': userAppKey,
    'X-Group-AppId': env.X_Group_AppId,
    'X-Group-Key': env.X_Group_Key,
    'X-SubGroup-AppId': env.X_SubGroup_AppId,
    'X-SubGroup-Key': env.X_SubGroup_Key,
  }
});

    console.log('Response:', response.data);
    alert('Community Created Successfully')
    router.push('/community');
    // Handle the response as needed (e.g., show success message, redirect, etc.)

  } catch (error) {
    
    console.error('Error:', error);
    alert('Error creating community', error.message)
    // Handle the error (e.g., show error message)
  }
};


fetchUsers();


//END OF EDIT
</script>




<template>
    <h1>Create New Community</h1>

    <div class="card p-fluid">
        <h4>Community Details</h4>
        <div class="formgrid grid">
            <div class="field col">
                <label for="comname">Community Name</label>
                <InputText id="comname" type="text" :comname v-model="comname"/>
                <small class="p-invalid"style="color:red"  v-if="submitted & !comname">Community Name is required.</small>
            </div>
            <div class="field col">
                <label for="comsize">Community Size</label>
                <InputText id="comsize" type="number" v-model="comsize" />
                <small class="p-invalid"style="color:red"  v-if="submitted & !comsize">Community Size is required.</small>
            </div>
        </div>


        <label for="comdesc">Community Description</label>
        <Textarea style="margin-top: 7px;" id="comdesc" placeholder="Your Message" :autoResize="true" rows="3"
            cols="100" v-model="comdesc"/>
    </div>
    

    <!--Select members for community-->
    <div class="flex">
        <div class="col-12 md:col-6">
            <div class="card">
                <h5>Add Members</h5>
                <MultiSelect v-model="communitymembers" :options="listofusers_forcheckbox" optionLabel="name"
                    placeholder="Select Members" :filter="true" class="w-full">
                    <template #value="slotProps">
                        <div class="inline-flex align-items-center py-1 px-2 bg-primary text-primary border-round mr-2"
                            v-for="option of slotProps.value" :key="option.userId">
                            <span :class="'mr-2 flag flag-' + option.userId.toLowerCase()"
                                style="width: 18px; height: 12px" />
                            <div>{{ option.name }}</div>
                        </div>
                        <template v-if="!slotProps.value || slotProps.value.length === 0">
                            <div class="p-1">Select Members</div>
                        </template>
                    </template>
                    <template #option="slotProps">
                        <div class="flex align-items-center">
                            <span :class="'mr-2 flag flag-' + slotProps.option.userId.toLowerCase()"
                                style="width: 18px; height: 12px" />
                            <div>{{ slotProps.option.name }}</div>
                        </div>
                    </template>
                </MultiSelect>
                <small class="p-invalid"style="color:red"  v-if="submitted && communitymembers==null">Please select at least one member.</small>
            </div>
        </div>



        <!--CODE FOR SUBGROUP TABLE-->
        <div class="col-12 md:col-6">
            <div class="card">
                <Button label="New Subgroup" icon="pi pi-plus" class="mr-2 mb-4" severity="success" @click="openNew" />
                <div class="card">
                    <h5>Existing Subgroups</h5>
                    <DataTable :value="subgroup_submit">
                        <Column field="name" header="Name"></Column>
                        <Column field="description" header="Description"></Column>
                        <Column field="members" header="Members">
                            <template #body="slotProps">
                            <div v-for="member in slotProps.data.subGroupUsers" :key="member.userId">{{ member.username }}</div>
                            </template>
                        </Column>
                        <Column field="size" header="Capacity"></Column>
                        <Column>
                            <template #body="slotProps">
                                <Button icon="pi pi-pencil" class="mr-2" severity="success" rounded
                                    @click="editsubgrp(slotProps.data)" />
                            </template>
                        </Column>
                        <Column>
                            <template #body="slotProps">
                                <Button icon="pi pi-trash" severity="danger" rounded
                                    @click="deletesubgrp(slotProps.data)" />
                            </template>
                        </Column>
                    </DataTable>
                </div>



                <!--Create SubGroup Dialog-->
                <Dialog v-model:visible="subgrp_popup" :style="{ width: '450px' }" header="Subgroup Details"
                    :modal="true" class="p-fluid">
                    <div class="field">
                        <label for="name">Subgroup Name</label>
                        <InputText id="name" v-model.trim="subgrp.name" required="true" autofocus
                            :invalid="subsubmitted && !subgrp.name" />
                        <small class="p-invalid" v-if="subsubmitted && !subgrp.name">Name is required.</small>
                    </div>
                    <div class="field">
                        <label for="description">Description</label>
                        <Textarea id="description" v-model="subgrp.description" required="true" rows="3" cols="20" />
                    </div>


                <!--Code to add subgroup members to subgroup-->
                    <div class="field">
                        <label for="members">Subgroup Members</label>
                        <MultiSelect v-model="subgrpmembers" :options="listofusers_forsubgrpcheckbox" optionLabel="name"
                            placeholder="Select Members" :filter="true" class="w-full">
                            <template #value="slotProps">
                                <div class="inline-flex align-items-center py-1 px-2 bg-primary text-primary border-round mr-2"
                                    v-for="option of slotProps.value" :key="option.userId">
                                    <span :class="'mr-2 flag flag-' + option.userId.toLowerCase()"
                                        style="width: 18px; height: 12px" />
                                    <div>{{ option.name }}</div>
                                </div>
                                <template v-if="!slotProps.value || slotProps.value.length === 0">
                                    <div class="p-1">Select Members</div>
                                </template>
                            </template>
                            <template #option="slotProps">
                                <div class="flex align-items-center">
                                    <span :class="'mr-2 flag flag-' + slotProps.option.userId.toLowerCase()"
                                        style="width: 18px; height: 12px" />
                                    <div>{{ slotProps.option.name }}</div>
                                </div>
                            </template>
                        </MultiSelect>
                    </div>

                    <div class="field">
                        <label for="capacity">Subgroup Capacity</label>
                        <InputNumber id="capacity" v-model="subgrp.capacity" integeronly required="True" />
                        <small class="p-invalid"style="color:red"  v-if="subsubmitted & subgrp.capacity>comsize">Subgroup Capacity cannot exceed Community Size.</small>
                        <small class="p-invalid"style="color:red"  v-if="subsubmitted & !subgrp.capacity">Subgroup Capacity is required.</small>
                    </div>

                    <template #footer>
                        <Button label="Cancel" icon="pi pi-times" text="" @click="hidesubgrp_popup" />
                        <Button label="Save" icon="pi pi-check" text="" @click="savesubgrp" />
                    </template>
                </Dialog>

                <Dialog v-model:visible="deletesubgrp_popup" :style="{ width: '450px' }" header="Confirm"
                    :modal="true">
                    <div class="flex align-items-center justify-content-center">
                        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
                        <span v-if="community">Are you sure you want to delete <b>{{ subgrp.name }}</b>?</span>
                    </div>
                    <template #footer>
                        <Button label="No" icon="pi pi-times" text @click="deletesubgrp_popup = false" />
                        <Button label="Yes" icon="pi pi-check" text @click="deletesubgrp" />
                    </template>
                </Dialog>
            </div>
        </div>
    </div>
    <div class="flex justify-content-center align-items-center mt-8">
    <Button label="Submit" class="mr-2 mb-2" @click="submitform"></Button>
    </div>

</template>

<script>
export default {
    components: {
        DataTable,
        Column,
        Button,
    },
}</script>
