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
const items = ref([
    { label: "Add New", icon: "pi pi-fw pi-plus" },
    { label: "Remove", icon: "pi pi-fw pi-minus" },
]);

const activities = ref([
    {
        status: "Ben Simmons",
        date: "15/10/2020 10:30",
        icon: "pi pi-shopping-cart",
        color: "#9C27B0",
        image: "/images/avatars/panda.png"
    },
    {
        status: "John Tan",
        date: "15/10/2020 14:00",
        icon: "pi pi-cog",
        color: "#673AB7",
        image: "/images/avatars/fox.png"
    },
    {
        status: "Paul Lynette",
        date: "15/10/2020 16:15",
        icon: "pi pi-shopping-cart",
        color: "#FF9800",
        image: "/images/avatars/woman.png"
    },
].reverse());

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
                <!-- 4 cards at the top of the screen -->
                <div class="col-12 lg:col-6 xl:col-3">
                    <div class="card mb-0">
                        <div class="flex justify-content-between mb-3">
                            <div>
                                <span class="block text-500 font-medium mb-3"
                                    >Orders</span
                                >
                                <div class="text-900 font-medium text-xl">
                                    152
                                </div>
                            </div>
                            <div
                                class="flex align-items-center justify-content-center bg-blue-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i
                                    class="pi pi-shopping-cart text-blue-500 text-xl"
                                ></i>
                            </div>
                        </div>
                        <span class="text-green-500 font-medium">24 new </span>
                        <span class="text-500">since last visit</span>
                    </div>
                </div>
                <div class="col-12 lg:col-6 xl:col-3">
                    <div class="card mb-0">
                        <div class="flex justify-content-between mb-3">
                            <div>
                                <span class="block text-500 font-medium mb-3"
                                    >Revenue</span
                                >
                                <div class="text-900 font-medium text-xl">
                                    $2.100
                                </div>
                            </div>
                            <div
                                class="flex align-items-center justify-content-center bg-orange-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i
                                    class="pi pi-map-marker text-orange-500 text-xl"
                                ></i>
                            </div>
                        </div>
                        <span class="text-green-500 font-medium">%52+ </span>
                        <span class="text-500">since last week</span>
                    </div>
                </div>
                <div class="col-12 lg:col-6 xl:col-3">
                    <div class="card mb-0">
                        <div class="flex justify-content-between mb-3">
                            <div>
                                <span class="block text-500 font-medium mb-3"
                                    >Customers</span
                                >
                                <div class="text-900 font-medium text-xl">
                                    28441
                                </div>
                            </div>
                            <div
                                class="flex align-items-center justify-content-center bg-cyan-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i
                                    class="pi pi-inbox text-cyan-500 text-xl"
                                ></i>
                            </div>
                        </div>
                        <span class="text-green-500 font-medium">520 </span>
                        <span class="text-500">newly registered</span>
                    </div>
                </div>
                <div class="col-12 lg:col-6 xl:col-3">
                    <div class="card mb-0">
                        <div class="flex justify-content-between mb-3">
                            <div>
                                <span class="block text-500 font-medium mb-3"
                                    >Comments</span
                                >
                                <div class="text-900 font-medium text-xl">
                                    152 Unread
                                </div>
                            </div>
                            <div
                                class="flex align-items-center justify-content-center bg-purple-100 border-round"
                                style="width: 2.5rem; height: 2.5rem"
                            >
                                <i
                                    class="pi pi-comment text-purple-500 text-xl"
                                ></i>
                            </div>
                        </div>
                        <span class="text-green-500 font-medium">85 </span>
                        <span class="text-500">responded</span>
                    </div>
                </div>
                <!-- 2 columns at the bottom -->
                <div class="col-12 xl:col-6">
                    <div class="card">
                        <h5>Recent Sales</h5>
                        <DataTable
                            :value="products"
                            :rows="5"
                            :paginator="true"
                            responsiveLayout="scroll"
                        >
                            <Column style="width: 15%">
                                <template #header> Image </template>
                                <template #body="slotProps">
                                    <img
                                        :src="
                                            'demo/images/product/' +
                                            slotProps.data.image
                                        "
                                        :alt="slotProps.data.image"
                                        width="50"
                                        class="shadow-2"
                                    />
                                </template>
                            </Column>
                            <Column
                                field="name"
                                header="Name"
                                :sortable="true"
                                style="width: 35%"
                            ></Column>
                            <Column
                                field="price"
                                header="Price"
                                :sortable="true"
                                style="width: 35%"
                            >
                                <template #body="slotProps">
                                    {{ formatCurrency(slotProps.data.price) }}
                                </template>
                            </Column>
                            <Column style="width: 15%">
                                <template #header> View </template>
                                <template #body>
                                    <Button
                                        icon="pi pi-search"
                                        type="button"
                                        class="p-button-text"
                                    ></Button>
                                </template>
                            </Column>
                        </DataTable>
                    </div>
                    <div class="card">
                        <div
                            class="flex justify-content-between align-items-center mb-5"
                        >
                            <h5>Best Selling Products</h5>
                            <div>
                                <Button
                                    icon="pi pi-ellipsis-v"
                                    class="p-button-text p-button-plain p-button-rounded"
                                    @click="$refs.menu2.toggle($event)"
                                ></Button>
                                <Menu
                                    ref="menu2"
                                    :popup="true"
                                    :model="items"
                                ></Menu>
                            </div>
                        </div>
                        <ul class="list-none p-0 m-0">
                            <li
                                class="flex flex-column md:flex-row md:align-items-center md:justify-content-between mb-4"
                            >
                                <div>
                                    <span
                                        class="text-900 font-medium mr-2 mb-1 md:mb-0"
                                        >Space T-Shirt</span
                                    >
                                    <div class="mt-1 text-600">Clothing</div>
                                </div>
                                <div
                                    class="mt-2 md:mt-0 flex align-items-center"
                                >
                                    <div
                                        class="surface-300 border-round overflow-hidden w-10rem lg:w-6rem"
                                        style="height: 8px"
                                    >
                                        <div
                                            class="bg-orange-500 h-full"
                                            style="width: 50%"
                                        ></div>
                                    </div>
                                    <span
                                        class="text-orange-500 ml-3 font-medium"
                                        >%50</span
                                    >
                                </div>
                            </li>
                            <li
                                class="flex flex-column md:flex-row md:align-items-center md:justify-content-between mb-4"
                            >
                                <div>
                                    <span
                                        class="text-900 font-medium mr-2 mb-1 md:mb-0"
                                        >Portal Sticker</span
                                    >
                                    <div class="mt-1 text-600">Accessories</div>
                                </div>
                                <div
                                    class="mt-2 md:mt-0 ml-0 md:ml-8 flex align-items-center"
                                >
                                    <div
                                        class="surface-300 border-round overflow-hidden w-10rem lg:w-6rem"
                                        style="height: 8px"
                                    >
                                        <div
                                            class="bg-cyan-500 h-full"
                                            style="width: 16%"
                                        ></div>
                                    </div>
                                    <span class="text-cyan-500 ml-3 font-medium"
                                        >%16</span
                                    >
                                </div>
                            </li>
                            <li
                                class="flex flex-column md:flex-row md:align-items-center md:justify-content-between mb-4"
                            >
                                <div>
                                    <span
                                        class="text-900 font-medium mr-2 mb-1 md:mb-0"
                                        >Supernova Sticker</span
                                    >
                                    <div class="mt-1 text-600">Accessories</div>
                                </div>
                                <div
                                    class="mt-2 md:mt-0 ml-0 md:ml-8 flex align-items-center"
                                >
                                    <div
                                        class="surface-300 border-round overflow-hidden w-10rem lg:w-6rem"
                                        style="height: 8px"
                                    >
                                        <div
                                            class="bg-pink-500 h-full"
                                            style="width: 67%"
                                        ></div>
                                    </div>
                                    <span class="text-pink-500 ml-3 font-medium"
                                        >%67</span
                                    >
                                </div>
                            </li>
                            <li
                                class="flex flex-column md:flex-row md:align-items-center md:justify-content-between mb-4"
                            >
                                <div>
                                    <span
                                        class="text-900 font-medium mr-2 mb-1 md:mb-0"
                                        >Wonders Notebook</span
                                    >
                                    <div class="mt-1 text-600">Office</div>
                                </div>
                                <div
                                    class="mt-2 md:mt-0 ml-0 md:ml-8 flex align-items-center"
                                >
                                    <div
                                        class="surface-300 border-round overflow-hidden w-10rem lg:w-6rem"
                                        style="height: 8px"
                                    >
                                        <div
                                            class="bg-green-500 h-full"
                                            style="width: 35%"
                                        ></div>
                                    </div>
                                    <span
                                        class="text-green-500 ml-3 font-medium"
                                        >%35</span
                                    >
                                </div>
                            </li>
                            <li
                                class="flex flex-column md:flex-row md:align-items-center md:justify-content-between mb-4"
                            >
                                <div>
                                    <span
                                        class="text-900 font-medium mr-2 mb-1 md:mb-0"
                                        >Mat Black Case</span
                                    >
                                    <div class="mt-1 text-600">Accessories</div>
                                </div>
                                <div
                                    class="mt-2 md:mt-0 ml-0 md:ml-8 flex align-items-center"
                                >
                                    <div
                                        class="surface-300 border-round overflow-hidden w-10rem lg:w-6rem"
                                        style="height: 8px"
                                    >
                                        <div
                                            class="bg-purple-500 h-full"
                                            style="width: 75%"
                                        ></div>
                                    </div>
                                    <span
                                        class="text-purple-500 ml-3 font-medium"
                                        >%75</span
                                    >
                                </div>
                            </li>
                            <li
                                class="flex flex-column md:flex-row md:align-items-center md:justify-content-between mb-4"
                            >
                                <div>
                                    <span
                                        class="text-900 font-medium mr-2 mb-1 md:mb-0"
                                        >Robots T-Shirt</span
                                    >
                                    <div class="mt-1 text-600">Clothing</div>
                                </div>
                                <div
                                    class="mt-2 md:mt-0 ml-0 md:ml-8 flex align-items-center"
                                >
                                    <div
                                        class="surface-300 border-round overflow-hidden w-10rem lg:w-6rem"
                                        style="height: 8px"
                                    >
                                        <div
                                            class="bg-teal-500 h-full"
                                            style="width: 40%"
                                        ></div>
                                    </div>
                                    <span class="text-teal-500 ml-3 font-medium"
                                        >%40</span
                                    >
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="col-12 xl:col-6">
                    <div class="card">
                        <h5>Sales Overview</h5>
                        <Chart
                            type="line"
                            :data="lineData"
                            :options="lineOptions"
                        />
                    </div>
                    <div class="card">
                        <div
                            class="flex align-items-center justify-content-between mb-4"
                        >
                            <h5>Notifications</h5>
                            <div>
                                <Button
                                    icon="pi pi-ellipsis-v"
                                    class="p-button-text p-button-plain p-button-rounded"
                                    @click="$refs.menu1.toggle($event)"
                                ></Button>
                                <Menu
                                    ref="menu1"
                                    :popup="true"
                                    :model="items"
                                ></Menu>
                            </div>
                        </div>

                        <span class="block text-600 font-medium mb-3"
                            >TODAY</span
                        >
                        <ul class="p-0 mx-0 mt-0 mb-4 list-none">
                            <li
                                class="flex align-items-center py-2 border-bottom-1 surface-border"
                            >
                                <div
                                    class="w-3rem h-3rem flex align-items-center justify-content-center bg-blue-100 border-circle mr-3 flex-shrink-0"
                                >
                                    <i
                                        class="pi pi-dollar text-xl text-blue-500"
                                    ></i>
                                </div>
                                <span class="text-900 line-height-3"
                                    >Richard Jones
                                    <span class="text-700"
                                        >has purchased a blue t-shirt for
                                        <span class="text-blue-500"
                                            >79$</span
                                        ></span
                                    >
                                </span>
                            </li>
                            <li class="flex align-items-center py-2">
                                <div
                                    class="w-3rem h-3rem flex align-items-center justify-content-center bg-orange-100 border-circle mr-3 flex-shrink-0"
                                >
                                    <i
                                        class="pi pi-download text-xl text-orange-500"
                                    ></i>
                                </div>
                                <span class="text-700 line-height-3"
                                    >Your request for withdrawal of
                                    <span class="text-blue-500 font-medium"
                                        >2500$</span
                                    >
                                    has been initiated.</span
                                >
                            </li>
                        </ul>

                        <span class="block text-600 font-medium mb-3"
                            >YESTERDAY</span
                        >
                        <ul class="p-0 m-0 list-none">
                            <li
                                class="flex align-items-center py-2 border-bottom-1 surface-border"
                            >
                                <div
                                    class="w-3rem h-3rem flex align-items-center justify-content-center bg-blue-100 border-circle mr-3 flex-shrink-0"
                                >
                                    <i
                                        class="pi pi-dollar text-xl text-blue-500"
                                    ></i>
                                </div>
                                <span class="text-900 line-height-3"
                                    >Keyser Wick
                                    <span class="text-700"
                                        >has purchased a black jacket for
                                        <span class="text-blue-500"
                                            >59$</span
                                        ></span
                                    >
                                </span>
                            </li>
                            <li
                                class="flex align-items-center py-2 border-bottom-1 surface-border"
                            >
                                <div
                                    class="w-3rem h-3rem flex align-items-center justify-content-center bg-pink-100 border-circle mr-3 flex-shrink-0"
                                >
                                    <i
                                        class="pi pi-question text-xl text-pink-500"
                                    ></i>
                                </div>
                                <span class="text-900 line-height-3"
                                    >Jane Davis
                                    <span class="text-700"
                                        >has posted a new questions about your
                                        product.</span
                                    >
                                </span>
                            </li>
                        </ul>
                    </div>
                    <div
                        class="px-4 py-5 shadow-2 flex flex-column md:flex-row md:align-items-center justify-content-between mb-3"
                        style="
                            border-radius: 1rem;
                            background: linear-gradient(
                                    0deg,
                                    rgba(0, 123, 255, 0.5),
                                    rgba(0, 123, 255, 0.5)
                                ),
                                linear-gradient(
                                    92.54deg,
                                    #1c80cf 47.88%,
                                    #ffffff 100.01%
                                );
                        "
                    >
                        <div>
                            <div
                                class="text-blue-100 font-medium text-xl mt-2 mb-3"
                            >
                                TAKE THE NEXT STEP
                            </div>
                            <div class="text-white font-medium text-5xl">
                                Try PrimeBlocks
                            </div>
                        </div>
                        <div class="mt-4 mr-auto md:mt-0 md:mr-0">
                            <a
                                href="https://www.primefaces.org/primeblocks-vue"
                                class="p-button font-bold px-5 py-3 p-button-warning p-button-rounded p-button-raised"
                            >
                                Get Started
                            </a>
                        </div>
                    </div>
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
                    <div class="flex justify-content-between align-items-center mb-2">
                        <h5 class="mb-0">Recent Activity</h5>
                        <Button label="View more" text></Button>
                    </div>
                    
                    <Timeline :value="activities" class="w-full">
                        <template #content="slotProps">
                            <Card class="mb-3 surface-50 w-full">
                                <template #title>
                                    <div class="flex align-items-center gap-2">
                                        <Avatar :image="slotProps.item.image" class="mr-2" size="large" shape="circle" />
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
                                    <div class="mb-1">
                                        <span class="font-bold">Resolved </span>
                                        <span class="text-blue-600 font-semibold">Task #121</span>
                                    </div>
                                    <p class="">
                                      Fix the bug on the homepage
                                    </p>
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
