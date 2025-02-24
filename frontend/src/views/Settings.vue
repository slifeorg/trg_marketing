<template>
  <div class="settings-page">
    <UserList v-if="isAdmin" />
  </div>
</template>

<script>
import UserList from '@/components/UserList.vue'

export default {
  components: {
    UserList
  },
  computed: {
    isAdmin() {
      return frappe.session.user_roles.includes('Administrator')
    }
  }
}
</script>