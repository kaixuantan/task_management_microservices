import axios from "axios";

export default {
    data() {
        return {
            communities: JSON.parse(sessionStorage.getItem('communities')) || [],
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
        }
    },
    computed: {
        userId() {
            return window.sessionStorage.getItem('userid');
        },
    },
    methods: {
        async fetchUserGroups() {
            if (!sessionStorage.getItem('communities')) {
                try {
                    let response = await axios.get(
                        `${env.BASE_URL}/GroupAPI_REST/rest/v1/group/usergroup/${this.userId}`,
                        {
                            headers: {
                                "X-Group-AppId": env.X_Group_AppId,
                                "X-Group-Key": env.X_Group_Key,
                            },
                        }
                    );
                    if (response.data.Result.Success !== true) {
                        console.error("Error fetching user groups");
                    } else {
                        let communities = response.data.UserGroup.groups;
                        sessionStorage.setItem('communities', JSON.stringify(communities));
                    }
                } catch (error) {
                    console.error(error);
                }
            }
        },
        async fetchUserTasks() {
            try {
                let response = await axios.get(
                    `${env.BASE_URL}/TaskAPI_REST/rest/v1/task/usertask/${this.userId}`,
                    {
                        headers: {
                            "X-Task-AppId": env.X_Task_AppId,
                            "X-Task-Key": env.X_Task_Key,
                        },
                    }
                );
                if (response.data.Result.Success !== true) {
                    console.error("Error fetching user groups");
                } else {
                    this.tasks = response.data.UserTask.tasks;
                }
            } catch (error) {
                console.error(error);
            }
        },
    },
    async created() {
        await this.fetchUserGroups();
    }
}