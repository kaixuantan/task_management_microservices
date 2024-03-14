<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import ProductService from "@/service/ProductService";
import { useLayout } from "@/layout/composables/layout";

const { isDarkTheme } = useLayout();

const products = ref(null);
const lineData = reactive({
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "First Dataset",
            data: [65, 59, 80, 81, 56, 55, 40],
            fill: false,
            backgroundColor: "#2f4860",
            borderColor: "#2f4860",
            tension: 0.4,
        },
        {
            label: "Second Dataset",
            data: [28, 48, 40, 19, 86, 27, 90],
            fill: false,
            backgroundColor: "#00bb7e",
            borderColor: "#00bb7e",
            tension: 0.4,
        },
    ],
});


const activities = ref(
    [
        {
            status: "Ben Simmons",
            date: "15/10/2020 10:30",
            task_id: "121",
            task_desc: "fix the bug on the homepage",
            project: "Project Meelo",
            image: "/images/avatars/panda.png",

        },
        {
            status: "John Tan",
            date: "15/10/2020 14:00",
            task_id: "2",
            task_desc: "added paragraph",
            project: "Project Kivu",
            image: "/images/avatars/fox.png",
        },
        {
            status: "Paul Lynette",
            date: "15/10/2020 16:15",
            task_id: "10",
            task_desc: "deleted old design",
            project: "Project Hapara",
            image: "/images/avatars/woman.png",
        },
    ].reverse()
);
const projects = ref(
    [
        {
            name: "Project Meelo",
            description: "create real estate landing page",
            icon: "pi pi-apple"
        },
        {
            name: "Project Kivu",
            description: "complete leadership assignment",
            icon: "pi pi-bitcoin"
        },
        {
            name: "Project Hapara",
            description: "design a new logo for the company",
            icon: "pi pi-bolt"
        },
    ]
)

const lineOptions = ref(null);
const productService = new ProductService();

onMounted(() => {
    productService.getProductsSmall().then((data) => (products.value = data));
});

const attributes = ref([
    {
        highlight: true,
        dates: new Date(),
    },
]);

const formatCurrency = (value) => {
    return value.toLocaleString("en-US", {
        style: "currency",
        currency: "USD",
    });
};
const applyLightTheme = () => {
    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: "#495057",
                },
            },
        },
        scales: {
            x: {
                ticks: {
                    color: "#495057",
                },
                grid: {
                    color: "#ebedef",
                },
            },
            y: {
                ticks: {
                    color: "#495057",
                },
                grid: {
                    color: "#ebedef",
                },
            },
        },
    };
};

// const applyDarkTheme = () => {
//     lineOptions.value = {
//         plugins: {
//             legend: {
//                 labels: {
//                     color: '#ebedef'
//                 }
//             }
//         },
//         scales: {
//             x: {
//                 ticks: {
//                     color: '#ebedef'
//                 },
//                 grid: {
//                     color: 'rgba(160, 167, 181, .3)'
//                 }
//             },
//             y: {
//                 ticks: {
//                     color: '#ebedef'
//                 },
//                 grid: {
//                     color: 'rgba(160, 167, 181, .3)'
//                 }
//             }
//         }
//     };
// };

watch(
    isDarkTheme,
    (val) => {
        if (val) {
            applyDarkTheme();
        } else {
            applyLightTheme();
        }
    },
    { immediate: true }
);
</script>

<template>
    <div class="grid">
        <div class="col-8">
            <div class="grid">
                <!-- 3 cards at the top of the screen -->
                <div class="col-12 lg:col-6 xl:col-4">
                    <div class="card mb-0 bg-orange-400 shadow-3">
                        <div
                            class="flex justify-content-between align-items-center mb-3"
                        >
                            <div>
                                <span class="text-900 text-2xl font-bold mb-3"
                                    >Tasks in Progress</span
                                >
                            </div>
                            <div
                                class="flex align-items-center justify-content-center surface-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i class="pi pi-chart-bar text-500 text-xl"></i>
                            </div>
                        </div>
                        <span class="text-900 font-semibold text-xl block mb-2"
                            >24
                        </span>
                        <span class="text-800 font-medium"
                            >+12% From Yesterday</span
                        >
                    </div>
                </div>
                <div class="col-12 lg:col-6 xl:col-4">
                    <div class="card mb-0 bg-purple-300 shadow-3">
                        <div
                            class="flex justify-content-between align-items-center mb-3"
                        >
                            <div>
                                <span class="text-900 text-2xl font-bold mb-3"
                                    >New Assigned</span
                                >
                            </div>
                            <div
                                class="flex align-items-center justify-content-center surface-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i class="pi pi-plus text-500 text-xl"></i>
                            </div>
                        </div>
                        <span class="text-900 font-semibold text-xl block mb-2"
                            >24
                        </span>
                        <span class="text-800 font-medium"
                            >+12% From Yesterday</span
                        >
                    </div>
                </div>
                <div class="col-12 lg:col-6 xl:col-4">
                    <div class="card mb-0 bg-blue-300 shadow-3">
                        <div
                            class="flex justify-content-between align-items-center mb-3"
                        >
                            <div>
                                <span class="text-900 text-2xl font-bold mb-3"
                                    >Completed Tasks</span
                                >
                            </div>
                            <div
                                class="flex align-items-center justify-content-center surface-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i
                                    class="pi pi-check-circle text-500 text-xl"
                                ></i>
                            </div>
                        </div>
                        <span class="text-900 font-semibold text-xl block mb-2"
                            >24
                        </span>
                        <span class="text-800 font-medium"
                            >+12% From Yesterday</span
                        >
                    </div>
                </div>

                <div class="col-12 flex justify-content-between">
                    <h2 class="mb-0 font-semibold">My Tasks</h2>
                    <Button label="Add task" icon="pi pi-plus" rounded />
                </div>
                <div class="col-12">
                    <TabView>
                        <TabPanel header="In progress">
                            <div v-for="project in projects" class="card shadow-1 flex align-items-center justify-content-between">
                                <div class="flex">
                                    <Avatar :icon="project.icon" class="mr-3" size="xlarge" />
                                    <div class="flex align-items-center">
                                        <div>
                                            <h5 class="mb-0 font-semibold">{{ project.name }}</h5>
                                            <p>{{ project.description }}</p>
                                        </div>    
                                    </div>
                                </div>
                                <div>
                                    <AvatarGroup>
                                        <Avatar image="/images/avatars/panda.png" size="large" shape="circle" />
                                        <Avatar image="/images/avatars/fox.png" size="large" shape="circle" />
                                        <Avatar image="/images/avatars/woman.png" size="large" shape="circle" />
                                        <Avatar label="+2" shape="circle" size="large" />
                                    </AvatarGroup>
                                </div>

                            </div>
                        </TabPanel>
                        <TabPanel header="New Assigned">
                            <p class="m-0">
                                Sed ut perspiciatis unde omnis iste natus error
                                sit voluptatem accusantium doloremque
                                laudantium, totam rem aperiam, eaque ipsa quae
                                ab illo inventore veritatis et quasi architecto
                                beatae vitae dicta sunt explicabo. Nemo enim
                                ipsam voluptatem quia voluptas sit aspernatur
                                aut odit aut fugit, sed quia consequuntur magni
                                dolores eos qui ratione voluptatem sequi
                                nesciunt. Consectetur, adipisci velit, sed quia
                                non numquam eius modi.
                            </p>
                        </TabPanel>
                        <TabPanel header="Completed">
                            <p class="m-0">
                                At vero eos et accusamus et iusto odio
                                dignissimos ducimus qui blanditiis praesentium
                                voluptatum deleniti atque corrupti quos dolores
                                et quas molestias excepturi sint occaecati
                                cupiditate non provident, similique sunt in
                                culpa qui officia deserunt mollitia animi, id
                                est laborum et dolorum fuga. Et harum quidem
                                rerum facilis est et expedita distinctio. Nam
                                libero tempore, cum soluta nobis est eligendi
                                optio cumque nihil impedit quo minus.
                            </p>
                        </TabPanel>
                    </TabView>
                </div>
            </div>
        </div>
        <div class="col-4">
            <Panel>
                <h5>Communities</h5>
                <div class="flex-auto">
                    <Avatar
                        v-for="(community, index) in communities.slice(0, 5)"
                        :key="index"
                        :label="community.charAt(0)"
                        class="mr-2"
                        size="large"
                        shape="circle"
                        :style="{
                            backgroundColor: colors[index % colors.length],
                        }"
                    />
                    <Avatar
                        :label="`+${communities.length - 5}`"
                        class="mr-2"
                        size="large"
                        shape="circle"
                    />
                </div>
                <Divider />
                <div>
                    <h5>Calendar</h5>
                    <VCalendar
                        view="weekly"
                        title-position="left"
                        expanded
                        :attributes="attributes"
                    />
                </div>

                <Divider />
                <div>
                    <div
                        class="flex justify-content-between align-items-center mb-2"
                    >
                        <h5 class="mb-0">Recent Activity</h5>
                        <Button label="View more" text></Button>
                    </div>

                    <Timeline :value="activities" class="w-full">
                        <template #content="slotProps">
                            <Card class="mb-3 surface-50 w-full">
                                <template #title>
                                    <div class="flex align-items-center gap-2">
                                        <Avatar
                                            :image="slotProps.item.image"
                                            class="mr-2"
                                            size="large"
                                            shape="circle"
                                        />
                                        {{ slotProps.item.status }}
                                    </div>
                                </template>
                                <template #subtitle>
                                    {{ slotProps.item.date }}
                                </template>
                                <template #content>
                                    <!-- <img
                                        v-if="slotProps.item.image"
                                        :src="`https://primefaces.org/cdn/primevue/images/product/${slotProps.item.image}`"
                                        :alt="slotProps.item.name"
                                        width="200"
                                        class="shadow-1"
                                    /> -->
                                    <div class="">
                                        <div class="mb-1">
                                        <span
                                            class="font-bold text-500"
                                            >{{ slotProps.item.project }}</span
                                        >
                                        </div>
                                        <div class="mb-1">
                                            <span class="font-bold">Resolved </span>
                                            <span
                                                class="text-blue-600 font-semibold"
                                                >Task #{{ slotProps.item.task_id }}</span
                                            >
                                        </div>
                                        <span class="font-italic">{{ slotProps.item.task_desc }}</span>
                                    </div>
                                </template>
                            </Card>
                        </template>
                    </Timeline>
                </div>
            </Panel>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            communities: [
                "ESD",
                "ITSA",
                "MATH",
                "PHYSICS",
                "CHEMISTRY",
                "BIOLOGY",
                "GEOGRAPHY",
                "HISTORY",
                "ENGLISH",
                "FRENCH",
                "SPANISH",
                "GERMAN",
                "ART",
            ],
            colors: [
                "#ece9fc",
                "#dee9fc",
                "#d8e2ef",
                "#e8e9fc",
                "#f2e9fc",
                "#f9e9fc",
                "#fce9f2",
                "#fce9e8",
                "#f9e9e2",
                "#f2e9d8",
            ],
        };
    },
};
</script>

<style>
.p-timeline-event-opposite {
    flex: 0;
}
</style>
