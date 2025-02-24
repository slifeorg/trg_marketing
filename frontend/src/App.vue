<template>
  <div class="h-screen">
    <router-view></router-view>
    <Dialogs></Dialogs>
  </div>
</template>

<script setup>
import { Dialogs } from 'frappe-ui'
</script>