// store.js
import { createStore } from 'vuex'

const getDefaultState = () => {
    return {
        first_user_project: null,
    };
};

export default createStore({
    state: getDefaultState(),
    mutations: {
        setFirstUserProject(state, proj_id) {
            state.first_user_project = proj_id;
        },
        RESET_STATE(state) {
            Object.assign(state, getDefaultState())
        }
    },
});

