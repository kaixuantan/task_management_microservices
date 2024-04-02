<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed } from 'vue';
import AppConfig from '@/layout/AppConfig.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';


const router = useRouter(); 
const { layoutConfig } = useLayout();
const username = ref('');
const password = ref('');
const checked = ref(false);

const baseURL = 'https://personal-rc7vnnm9.outsystemscloud.com';
const userAppId = env.X_User_AppId 
const userAppKey = env.X_User_Key

const fetchUserData = async (userId) => {
            try{
                console.log(userId)
                let response = await axios.get(
                    `${env.BASE_URL}/UserAPI_REST/rest/v1/user/${userId}/`,
                    {
                        headers: {
                            "X-User-AppId": env.X_User_AppId,
                            "X-User-Key": env.X_User_Key,
                        },
                    }
                );
                if (response.data.Result.Success !== true) {
                    console.error("Error fetching user groups");
                } else {
                    sessionStorage.setItem('email', response.data.User.email)
                    sessionStorage.setItem('role', response.data.User.role)
                }
            }
            catch(error){
                console.error(error);
            }
        }

const handleSubmit = async () => {
  try {
    // Validate the form
    if (!username.value || !password.value) {
      alert('Please fill in all fields');
      return;
    }

    // Make the API call
    const userData={
  "username": username.value,
  "password": password.value,
}
    console.log('Called Login API')
    console.log(username.value)
    const response = await axios.post(`${baseURL}/UserAPI_REST/rest/v1/login`, userData, { headers });

    
    // Handle the response
    if (response.data.Result.Success === false) {
        alert(response.data.Result.ErrorMessage)
    }

    else {
        const user_id = response.data['User']['userId'];
        const email = response.data['User']['email'];
        const role = response.data['User']['role'];
        sessionStorage.setItem('userid', user_id);
        sessionStorage.setItem('username', username.value);
        sessionStorage.setItem('yourKey', env.JWT_SECRET);
        sessionStorage.setItem('email', email);
        sessionStorage.setItem('role', role);
        router.push('/'); 
    }

  } catch (error) {
    // Handle errors
    console.error('Error adding user:', error);
    console.log(response.data.Result.ErrorMessage)
  }
}


const headers = {
  'Content-Type': 'application/json',
  'X-User-AppId': userAppId,
  'X-User-Key': userAppKey}

</script>

<template>
    <form @submit.prevent="handleSubmit">
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <img src="/demo/images/TaskMaster.png" alt="Image" height="120" class="mb-3" />
                        <div class="text-900 text-3xl font-medium mb-3">Welcome</div>
                        <span class="text-600 font-medium">Sign in to continue</span>
                    </div>

                    <div>
                        <label for="username" class="block text-900 text-xl font-medium mb-2">Username</label>
                        <InputText id="username" type="text" placeholder="Enter Username" class="w-full md:w-30rem mb-5" style="padding: 1rem" v-model="username" />

                        <label for="password" class="block text-900 font-medium text-xl mb-2">Password</label>
                        <input type="password" id="password" v-model="password" placeholder="Enter Password" class="w-full mb-3" style="padding: 1rem;">
                        <div class="flex align-items-center justify-content-between mb-5 gap-5">
                            <div class="flex align-items-center">
                                New User?&nbsp 
                                <a href="./register">Register Here!</a>
                            </div>
                            <a class="font-medium no-underline ml-2 text-right cursor-pointer" style="color: var(--primary-color)">Forgot password?</a>
                        </div>
                        <Button label="Sign In" class="w-full p-3 text-xl" type="submit"></Button>
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
