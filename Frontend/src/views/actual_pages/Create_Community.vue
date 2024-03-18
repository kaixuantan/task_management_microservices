<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import AppConfig from '@/layout/AppConfig.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import { watch } from 'vue';




//TO EDIT WITH ACTUAL USER VALUES
const multiselectValues = ref([
    { name: 'Australia', code: 'AU' },
    { name: 'Brazil', code: 'BR' },
    { name: 'China', code: 'CN' },
    { name: 'Egypt', code: 'EG' },
    { name: 'France', code: 'FR' },
    { name: 'Germany', code: 'DE' },
    { name: 'India', code: 'IN' },
    { name: 'Japan', code: 'JP' },
    { name: 'Spain', code: 'ES' },
    { name: 'United States', code: 'US' }
]);
const multiselectValue = ref(null);
const multiselectValue2 = ref(null);
const subgroups = ref([]);
const subgroupsKey = ref(0);
watch(subgroups, () => {
            subgroupsKey.value++;
        });

const toast = useToast();
const communities = ref([]);
const selectedCommunities = ref(null);
const communityDialog = ref(false);
const deleteCommunityDialog = ref(false);
const community = ref({
    name: '',
    description: '',
    members: [],
    capacity: null
});
const submitted = ref(false);

const openNew = () => {
    community.value = {};
    submitted.value = false;
    communityDialog.value = true;
};

const hideCommunityDialog = () => {
    communityDialog.value = false;
    submitted.value = false;
};

const saveCommunity = () => {
    submitted.value = true;
    if (community.value.name && community.value.name.trim() && community.value.description) {
        if (community.value.id) {
            // Update existing community
            const index = communities.value.findIndex(c => c.id === community.value.id);
            communities.value[index] = { ...community.value };

            // Update existing subgroup
            const subgroupIndex = subgroups.value.findIndex(c => c.id === community.value.id);
            subgroups.value[subgroupIndex] = { ...community.value };

            toast.add({ severity: 'success', summary: 'Successful', detail: 'Community Updated', life: 3000 });
        } else {
            // Create new community
            const newCommunity = { ...community.value, id: createId() };
            console.log(newCommunity.id);
            communities.value.push(newCommunity);
            console.log(communities.value);
            subgroups.value.push({ ...newCommunity });
            console.log(subgroups.value);
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Community Created', life: 3000 });
        }
        
        communityDialog.value = false;
        community.value = {};
    }
};

const editCommunity = (communitydata) => {
    subgroups.value = subgroups.value.filter(c => c.id !== communitydata);
    communities.value = communities.value.filter(c => c.id !== communitydata);
    communityDialog.value = true;
    community.value = { ...communitydata };
};

const confirmDeleteCommunity = (community) => {
    community.value = community;
    console.log(community.value)
    deleteCommunityDialog.value = true;
};

const deleteCommunity = (datatodelete) => {
    console.log(datatodelete.id)
    subgroups.value = subgroups.value.filter(c => c.id !== datatodelete.id);
    communities.value = communities.value.filter(c => c.id !== community.value.id);
    deleteCommunityDialog.value = false;

    community.value = {};
    toast.add({ severity: 'success', summary: 'Successful', detail: 'Subgroup Deleted', life: 3000 });
};

const confirmDeleteSelected = () => {
    deleteCommunityDialog.value = true;
};

const deleteSelectedCommunities = () => {
    communities.value = communities.value.filter(c => !selectedCommunities.value.includes(c));
    deleteCommunityDialog.value = false;
    selectedCommunities.value = null;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'Communities Deleted', life: 3000 });
};

const createId = () => {
    let id = '';
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 5; i++) {
        id += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return id;
};




//END OF EDIT
</script>




<template>
    <h1>Create New Community</h1>

    <div class="card p-fluid">
        <h4>Community Details</h4>
        <div class="formgrid grid">
            <div class="field col">
                <label for="name2">Community Name</label>
                <InputText id="name2" type="text" />
            </div>
            <div class="field col">
                <label for="email2">Community Size</label>
                <InputText id="email2" type="" />
            </div>
        </div>


        <label for="desc">Community Description</label>
        <Textarea style="margin-top: 7px;" id="desc" placeholder="Your Message" :autoResize="true" rows="3"
            cols="100" />
    </div>
    
    <div class="flex">
        <div class="col-12 md:col-6">
            <div class="card">
                <h5>Add Members</h5>
                <MultiSelect v-model="multiselectValue" :options="multiselectValues" optionLabel="name"
                    placeholder="Select Members" :filter="true" class="w-full">
                    <template #value="slotProps">
                        <div class="inline-flex align-items-center py-1 px-2 bg-primary text-primary border-round mr-2"
                            v-for="option of slotProps.value" :key="option.code">
                            <span :class="'mr-2 flag flag-' + option.code.toLowerCase()"
                                style="width: 18px; height: 12px" />
                            <div>{{ option.name }}</div>
                        </div>
                        <template v-if="!slotProps.value || slotProps.value.length === 0">
                            <div class="p-1">Select Members</div>
                        </template>
                    </template>
                    <template #option="slotProps">
                        <div class="flex align-items-center">
                            <span :class="'mr-2 flag flag-' + slotProps.option.code.toLowerCase()"
                                style="width: 18px; height: 12px" />
                            <div>{{ slotProps.option.name }}</div>
                        </div>
                    </template>
                </MultiSelect>

            </div>
        </div>

        <!--CODE FORSUBGROUP POPUP-->
        <div class="col-12 md:col-6">
            <div class="card">
                <Button label="New Subgroup" icon="pi pi-plus" class="mr-2 mb-4" severity="success" @click="openNew" />
                <div class="card">
                    <h5>Existing Subgroups</h5>
                    <DataTable :value="subgroups" :key="subgroupsKey">
                        <Column field="name" header="Name"></Column>
                        <Column field="description" header="Description"></Column>
                        <Column field="members" header="Members">
                            <template #body="slotProps">
                                <div v-for="member in slotProps.data.members" :key="member.code">{{ member.name }}</div>
                            </template>
                        </Column>
                        <Column field="capacity" header="Capacity"></Column>
                        <Column>
                            <template #body="slotProps">
                                <Button icon="pi pi-pencil" class="mr-2" severity="success" rounded
                                    @click="editCommunity(slotProps.data)" />
                            </template>
                        </Column>
                        <Column>
                            <template #body="slotProps">
                                <Button icon="pi pi-trash" severity="danger" rounded
                                    @click="deleteCommunity(slotProps.data)" />
                            </template>
                        </Column>
                    </DataTable>
                </div>
                <Dialog v-model:visible="communityDialog" :style="{ width: '450px' }" header="Subgroup Details"
                    :modal="true" class="p-fluid">
                    <div class="field">
                        <label for="name">Subgroup Name</label>
                        <InputText id="name" v-model.trim="community.name" required="true" autofocus
                            :invalid="submitted && !community.name" />
                        <small class="p-invalid" v-if="submitted && !community.name">Name is required.</small>
                    </div>
                    <div class="field">
                        <label for="description">Description</label>
                        <Textarea id="description" v-model="community.description" required="true" rows="3" cols="20" />
                    </div>

                    <div class="field">
                        <label for="members">Subgroup Members</label>
                        <!-- Add MultiSelect or other component to handle members -->
                        <MultiSelect v-model="multiselectValue2" :options="multiselectValues" optionLabel="name"
                            placeholder="Select Countries" :filter="true" class="w-full">
                            <template #value="slotProps">
                                <div class="inline-flex align-items-center py-1 px-2 bg-primary text-primary border-round mr-2"
                                    v-for="option of slotProps.value" :key="option.code">
                                    <span :class="'mr-2 flag flag-' + option.code.toLowerCase()"
                                        style="width: 18px; height: 12px" />
                                    <div>{{ option.name }}</div>
                                </div>
                                <template v-if="!slotProps.value || slotProps.value.length === 0">
                                    <div class="p-1">Select Countries</div>
                                </template>
                            </template>
                            <template #option="slotProps">
                                <div class="flex align-items-center">
                                    <span :class="'mr-2 flag flag-' + slotProps.option.code.toLowerCase()"
                                        style="width: 18px; height: 12px" />
                                    <div>{{ slotProps.option.name }}</div>
                                </div>
                            </template>
                        </MultiSelect>
                    </div>

                    <div class="field">
                        <label for="capacity">Subgroup Capacity</label>
                        <InputNumber id="capacity" v-model="community.capacity" integeronly />
                    </div>

                    <template #footer>
                        <Button label="Cancel" icon="pi pi-times" text="" @click="hideCommunityDialog" />
                        <Button label="Save" icon="pi pi-check" text="" @click="saveCommunity" />
                    </template>
                </Dialog>

                <Dialog v-model:visible="deleteCommunityDialog" :style="{ width: '450px' }" header="Confirm"
                    :modal="true">
                    <div class="flex align-items-center justify-content-center">
                        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
                        <span v-if="community">Are you sure you want to delete <b>{{ community.name }}</b>?</span>
                    </div>
                    <template #footer>
                        <Button label="No" icon="pi pi-times" text @click="deleteCommunityDialog = false" />
                        <Button label="Yes" icon="pi pi-check" text @click="deleteCommunity" />
                    </template>
                </Dialog>
            </div>
        </div>
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
