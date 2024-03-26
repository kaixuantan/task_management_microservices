<script setup>
import { useRouter } from 'vue-router';

const router = useRouter(); 
const redirectToCreateCommunity = () => {
    router.push({ name: 'create community' });
}
</script>

<template>
    <div class="grid">
        <div class="col-12 flex justify-content-between">
            <h2 class="mb-0 font-semibold">Communities</h2>
            <Button label="Create" icon="pi pi-plus" rounded raised @click="redirectToCreateCommunity"/>
        </div>
        <!-- 3 cards at the top of the screen -->
        <div class="xl:col-4" v-for="n in 3" v-if="communities.length === 0">
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

        <div class="xl:col-4" v-for="(community,idx) in communities" v-else>
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
                        <Button text>
                            <i class="pi pi-pencil text-500 text-xl"></i>
                        </Button>
                    </div>
                    <img
                        alt="user header"
                        src="https://espanol.verizon.com/learning/_next/static/images/87c8be7b206ab401b295fd1d21620b79.jpg"
                        style="width: 100%; height: 100%; object-fit: contain;"
                    />
                </template>
                <template #title>Members: {{ community.size }}</template>
                <template #subtitle>{{ community.description }} Description about community </template>
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
</template>

<script>
import axios from 'axios';
import sharedMixin from "@/sharedMixin";

export default {
    mixins: [sharedMixin],
    data() {
        return {
        };
    },
    methods: {
        viewProjects(groupId) {
            this.$router.push({ name: 'projects', query: { groupId: groupId } });
        }
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
