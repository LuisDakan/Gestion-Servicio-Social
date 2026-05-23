<template>
  <AppLayout :nav-items="$route.meta.nav" :page-title="$route.meta.title">
    <router-view />
  </AppLayout>
</template>

<script setup>
import AppLayout from '../../components/AppLayout.vue'
</script>
