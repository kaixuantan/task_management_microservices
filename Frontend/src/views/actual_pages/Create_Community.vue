<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed } from 'vue';
import AppConfig from '@/layout/AppConfig.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
</script>



<template>
    <div className="card">
        <h5>Empty Page</h5>
        <p>Use this page to start from scratch and place your custom content.</p>
    </div>
</template>
