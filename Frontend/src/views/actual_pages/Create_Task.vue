<script setup>
import { useLayout } from '@/layout/composables/layout';
import { useToast } from 'primevue/usetoast';
import AppConfig from '@/layout/AppConfig.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Button from 'primevue/button';
import { ref, computed, onMounted } from 'vue';




//TO EDIT WITH ACTUAL USER VALUES PULLED FROM SUBGROUP
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
//End of edit


//Values to pass to task microservice
const multiselectValue = ref(null);
const date1 = ref(null);
const taskname = ref('');
const task_desc = ref('');
const assignedBy = ref('');
//END OF VALUES


const toast = useToast();
const submitted = ref(false);

//For calling API
const baseURL = 'https://personal-rc7vnnm9.outsystemscloud.com';
const userAppId = env.X_User_AppId 
const userAppKey = env.X_User_Key
const headers = {
  'Content-Type': 'application/json',
  'X-User-AppId': userAppId,
  'X-User-Key': userAppKey}

assignedBy.value = sessionStorage.getItem('username');
//END OF API CALL

</script>




<template>
    <h1>Create New Task</h1>

    <div class="card p-fluid">
        <h4>Task Details</h4>
        <div class="formgrid grid">
            <div class="field col" >
                <label for="name2">Task Title</label>
                <InputText id="name2" type="text" v-model="taskname" />
            </div>
            <div class="field col" v-if="assignedBy">
                <label for="assignedby">Assigned By</label>
                <InputText id="assignedby" type="" v-model="assignedBy" disabled/>
            </div>
        </div>


        <label for="desc">Task Description</label>
        <Textarea style="margin-top: 7px;" id="desc" placeholder="Your Message" :autoResize="true" rows="3"cols="100" v-model="task_desc" />
    </div>
    <div class="flex">
        <div class="col-12 md:col-6">
            <div class="card">
                <h5>Assign Members</h5>
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
        <div class="col-12 md:col-6">
        <div class="card">
            <h5>Due Date</h5>
            <Calendar v-model="date1" :inputStyle="{ width: '100%' }" :showIcon="true" class="w-full" />
        </div>
    </div>
    </div>

    <div class="flex justify-content-center">
        <Button class='mt-8' label="Create Task" @click="handleSubmit" />
    </div>


</template>

<script>
export default {
    components: {
        Button,
    },
}</script>
