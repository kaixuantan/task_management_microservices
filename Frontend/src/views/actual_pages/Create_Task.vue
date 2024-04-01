<script setup>
import { useToast } from 'primevue/usetoast';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Button from 'primevue/button';
import { ref, computed, onMounted } from 'vue';

const multiselectAssignees = ref([]);
const subGroupId = ref('');

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
subGroupId.value = urlParams.get('subGroupId');
console.log(subGroupId.value);
const router = useRouter(); 
onMounted(async () => {
    try {
        const response = await axios.get(`http://localhost:5003/subgroup/${subGroupId.value}`); 
        multiselectAssignees.value = response.data;
    } catch (error) {
        console.error('Error fetching assignees:', error);
    }
});

//Values to pass to task microservice
const multiselectAssignee = ref(null);
const dueDate = ref(new Date());
const currentTime = new Date();
const hours = currentTime.getHours().toString().padStart(2, '0'); // Ensures two digits, padding with 0 if necessary
const minutes = currentTime.getMinutes().toString().padStart(2, '0');
const formattedTime = `${hours}:${minutes}`;
const dueTime = ref(formattedTime);
const taskname = ref('');
const taskdesc = ref('');
const username = ref(sessionStorage.getItem('username') || '');
const userId = ref(sessionStorage.getItem('userid') || '');
//END OF VALUES

const toast = useToast();
const submitted = ref(false);

const handleSubmit = async () => {
    try {
        // Validate the form
        if (!taskname.value || !taskdesc.value || !multiselectAssignee.value || !dueDate.value || !dueTime.value ) {
            alert('Please fill in all fields');
            return;
        }

        const selectedDateTime = new Date(dueDate.value);
        const selectedTime = dueTime.value.split(':');
        selectedDateTime.setHours(selectedTime[0]);
        selectedDateTime.setMinutes(selectedTime[1]);
        selectedDateTime.setSeconds(0); 
        selectedDateTime.setMilliseconds(0); 
        const utcDateTime = new Date(selectedDateTime.getTime() - (selectedDateTime.getTimezoneOffset() * 60000));
        const dueDateTime = utcDateTime.toISOString();

        console.log(multiselectAssignee.value)

        // Make the API call
        const taskData={
            "taskName": taskname.value,
            "taskDesc": taskdesc.value,
            "dueDateTime": dueDateTime,
            "subGroupId": subGroupId.value,
            "assignorUserId": userId.value,
            "assignorUsername": username.value,
            "assignedTo": multiselectAssignee.value,
        }

        // console.log('Called Task API')
        // console.log(taskname.value)
        // console.log(username.value)
        // console.log(multiselectAssignee.value)
        // console.log(dueDate.value)

        const response = await axios.post(`http://localhost:5003/task`, taskData);
        
        // Handle the response
        console.log('Task added:', response.data);
        alert('Task has been created successfully.'); // Show alert message
        router.push({ name: 'project', query: { subGroupId: urlParams.get('subGroupId') } }); // Redirect to the home page with a query parameter        
        return response.data;
        
    } catch (error) {
        // Handle errors
        console.error('Error adding task:', error);
    }
}
//END OF API CALL

</script>


<style>
    .datetime{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-content: center;
    }

    .w49 {
        width: 49%;
        padding-top: 0;
        padding-bottom: 0;
        padding-right: 0;
    }

    #inputTime::-webkit-calendar-picker-indicator {
        background-color: #3B82F6;
        /* filter: invert(1); */
        border: 1px solid #3B82F6;
        transition: background-color 0.2s, color 0.2s, border-color 0.2s, box-shadow 0.2s, outline-color 0.2s;
        border-radius: 0 6px 6px 0;
        outline-color: transparent;
        margin: 0;
    }
</style>

<template>
    <h1>Create New Task</h1>

    <div class="card p-fluid">
        <h4>Task Details</h4>
        <div class="formgrid grid">
            <div class="field col" >
                <label for="name2">Task Title</label>
                <InputText id="name2" type="text" v-model="taskname" />
            </div>
            <div class="field col" v-if="username">
                <label for="username">Assigned By</label>
                <InputText id="username" type="" v-model="username" disabled/>
            </div>
        </div>


        <label for="desc">Task Description</label>
        <Textarea style="margin-top: 7px;" id="desc" placeholder="Your Message" :autoResize="true" rows="3"cols="100" v-model="taskdesc" />
    </div>
    <div class="flex">
        <div class="col-12 md:col-6 px-0">
            <div class="card">
                <h5>Assign Members</h5>
                <MultiSelect v-model="multiselectAssignee" :options="multiselectAssignees" optionLabel="name"
                    placeholder="Select Members" :filter="true" class="w-full">
                    <template #value="slotProps">
                        <div class="inline-flex align-items-center py-1 px-2 bg-primary text-primary border-round mr-2"
                            v-for="option of slotProps.value" :key="option.assigneeUserId">
                            <!-- <span :class="'mr-2 flag flag-' + option.userId.toLowerCase()"
                                style="width: 18px; height: 12px" /> -->
                            <div>{{ option.assigneeUsername }}</div>
                        </div>
                        <template v-if="!slotProps.value || slotProps.value.length === 0">
                            <div class="p-1">Select Members</div>
                        </template>
                    </template>
                    <template #option="slotProps">
                        <div class="flex align-items-center">
                            <!-- <span :class="'mr-2 flag flag-' + slotProps.option.userId.toLowerCase()"
                                style="width: 18px; height: 12px" /> -->
                            <div>{{ slotProps.option.assigneeUsername }}</div>
                        </div>
                    </template>
                </MultiSelect>
                <!-- <div>{{ multiselectAssignee}}</div> -->
            </div>
        </div>
        <div class="col-12 md:col-6">
        <div class="card">
            <h5>Due Date and Time</h5>
            <div class="datetime">
                <div class="w49">
                    <Calendar v-model="dueDate" :inputStyle="{ width: '100%' }" :showIcon="true" class="w-full" />
                </div>
                <input type="time" id="inputTime" class="p-inputtext p-component w49" v-model="dueTime">
            </div>
           <!--  <span class="p-calendar p-component p-inputwrapper p-calendar-w-btn p-inputwrapper-filled w-full" data-pc-section="root" id="pv_id_182">
                <input type="time" v-model="dueTime" role="combobox" class="p-inputtext p-component" autocomplete="off" aria-autocomplete="none" aria-haspopup="dialog" aria-expanded="false" aria-controls="pv_id_182_panel" inputmode="none" tabindex="0" data-pc-section="input" style="width: 100%;">
            </span> -->
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
    }
}
</script>
