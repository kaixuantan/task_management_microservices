import axios from "axios";

export default {
    data() {
        return {
            communities: [],
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
            user_projects: []
        }
    },
    computed: {
        userId() {
            return window.sessionStorage.getItem('userid');
        },
        username() {
            return window.sessionStorage.getItem("username");
        },
        role() {
            return window.sessionStorage.getItem("role");
        }
    },
    methods: {
        async fetchUserGroups() {
            try {
                console.log("fetching user communities");
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
                    console.log(response.data.UserGroup.groups)
                    this.communities = response.data.UserGroup.groups;
                }
            } catch (error) {
                console.error(error);
            }
            
        },
        async fetchUserProjects() {
            try {
                console.log("fetching user projects");
                let response = await axios.get(
                    `${env.BASE_URL}/SubGroupAPI_REST/rest/v1/subgroup/usersubgroup/${this.userId}`,
                    {
                        headers: {
                            "X-SubGroup-AppId": env.X_SubGroup_AppId,
                            "X-SubGroup-Key": env.X_SubGroup_Key,
                        },
                    }
                );
                if (response.data.Result.Success !== true) {
                    console.error("Error fetching user projects");
                } else {
                    this.user_projects = response.data.UserSubGroup.subGroups;
                    console.log("projects updated");
                }
            } catch (error) {
                console.error(error);
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
        sortTasksByStatus(tasks) {
            if (tasks) {
                tasks.forEach(task => {
                    switch(task.status) {
                    case 'In Progress':
                        this.tasks_in_progress.push(task);
                        break;
                    case 'New':
                        this.tasks_new.push(task);
                        break;
                    case 'Completed':
                        this.tasks_completed.push(task);
                        break;
                    default:
                        console.log(`Unknown status: ${task.status}`);
                    }
                });
            }
        },
        formatDate(timestamp) {
            let date = new Date(timestamp);
            let year = date.getFullYear().toString().slice(-2);
            return date.getDate() + "/" + (date.getMonth() + 1) + "/" + year;
        },
        
    }
}