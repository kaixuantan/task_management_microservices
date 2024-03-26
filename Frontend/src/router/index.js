import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import { isAuthenticated } from './auth'; 

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'home',
                    component: () => import('@/views/Home.vue')
                },
                {
                    path: '/community',
                    name: 'community',
                    component: () => import('@/views/actual_pages/Community.vue')
                },
                {
                    path: '/create-community',
                    name: 'create community',
                    component: () => import('@/views/actual_pages/Create_Community.vue')
                },
                {
                    path: '/create-task',
                    name: 'create task',
                    component: () => import('@/views/actual_pages/Create_Task.vue')
                },
                {
                    path: '/project',
                    name: 'project',
                    component: () => import('@/views/actual_pages/Single_project.vue'),
                    beforeEnter: (to, from, next) => {
                        if (!to.query.subGroupId) {
                          next(from.path); // Redirect back to the previous page
                        } else {
                          next();
                        }
                    }
                },
                {
                    path: '/projects',
                    name: 'projects',
                    component: () => import('@/views/actual_pages/Projects.vue'),
                    beforeEnter: (to, from, next) => {
                        if (!to.query.groupId) {
                          next(from.path); // Redirect back to the previous page
                        } else {
                          next();
                        }
                    }
                },
                {
                    path: '/dashboard',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
            ]    
        },
        {
            path: '/pages/notfound',
            name: 'notfound',
            component: () => import('@/views/pages/NotFound.vue')
        },

        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/auth/register',
            name: 'register',
            component: () => import('@/views/pages/auth/Register.vue')
        },
        {
            path: '/auth/access',
            name: 'accessDenied',
            component: () => import('@/views/pages/auth/Access.vue')
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/pages/auth/Error.vue')
        },
    ]
}); 
router.beforeEach((to, from, next) => {
    // Check if the user is authenticated
    const authenticated = isAuthenticated();
  
    // Allow access to login and register routes without authentication
    if (to.name === 'login' || to.name === 'register') {
      next();
      return;
    }
  
    // Redirect to login page if not authenticated
    if (!authenticated) {
      next({ name: 'login' });
      return;
    }
  
    // Allow access to the requested route if authenticated
    next();
  });


export default router;
