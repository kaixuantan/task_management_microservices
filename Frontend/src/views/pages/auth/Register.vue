<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed } from 'vue';
import AppConfig from '@/layout/AppConfig.vue';
import axios from 'axios';


const { layoutConfig } = useLayout();
const email = ref('');
const username = ref('');
const password = ref('');
const confirmpassword = ref('');
const checked = ref(false);
const selectedRole = ref('user');
const baseURL = 'https://personal-rc7vnnm9.outsystemscloud.com';
const userAppId = env.X_User_AppId 
const userAppKey = env.X_User_Key


const headers = {
  'Content-Type': 'application/json',
  'X-User-AppId': userAppId,
  'X-User-Key': userAppKey}

const handleSubmit = async () => {
  try {
    // Validate the form
    if (!email.value || !username.value || !password.value || !confirmpassword.value) {
      alert('Please fill in all fields');
      return;
    }
    if (password.value !== confirmpassword.value) {
      alert('Passwords do not match');
      return;
    }
    
    // Make the API call
    const userData={
  "username": username.value,
  "password": password.value,
  "email": email.value,
  "role": selectedRole.value,
}
    console.log('Called User API')
    console.log(username.value)
    console.log(selectedRole.value)
    const response = await axios.post(`${baseURL}/UserAPI_REST/rest/v1/user`, userData, { headers });

    
    // Handle the response
    console.log('User added:', response.data);
    return response.data;
  } catch (error) {
    // Handle errors
    console.error('Error adding user:', error);
    throw error;
  }
};

</script>

<template>
    <form @submit.prevent="handleSubmit">
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <img src="/demo/images/TaskMaster.png" alt="Image" height="80" class="mb-3" />
                        <div class="text-900 text-3xl font-medium mb-3">Welcome</div>
                        <span class="text-600 font-medium">Register Here!</span>
                    </div>

                    <div>
                        <label for="email1" class="block text-900 text-xl font-medium mb-2">Email</label>
                        <InputText id="email1" type="text" placeholder="Email address" class="w-full md:w-30rem mb-5" style="padding: 1rem" v-model="email" />
                        
                        <label for="Username" class="block text-900 text-xl font-medium mb-2">Username</label>
                        <InputText id="username" type="text" placeholder="Username" class="w-full md:w-30rem mb-5" style="padding: 1rem" v-model="username" />

                        <label for="password1" class="block text-900 font-medium text-xl mb-2">Password</label>
                        <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true" class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }"></Password>
                        
                        <label for="confirmpassword" class="block text-900 font-medium text-xl mb-2">Confirm Password</label>
                        <Password id="confirmpassword" v-model="confirmpassword" placeholder="Confirm Password" :toggleMask="true" class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }"></Password>

                        <label for="role" class="block text-900 font-medium text-xl mb-2">Role</label>
                        <div>
                        <input type="radio" id="user" name="role" value="user" v-model="selectedRole" checked>
                        <label for="user">User</label>
                        <input type="radio" id="admin" name="role" value="admin" v-model="selectedRole">
                        <label for="admin">Admin</label>
       
                        </div>

                        <Button label="Register" class="w-full p-3 text-xl mt-4" type="submit"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</form>

    <AppConfig simple />
</template>

<style scoped>
.pi-eye {
    transform: scale(1.6);
    margin-right: 1rem;
}

.pi-eye-slash {
    transform: scale(1.6);
    margin-right: 1rem;
}

</style>
