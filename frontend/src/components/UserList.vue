<template>
  <div class="user-list p-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold text-gray-900">System Users</h2>
      <Button
        variant="primary"
        icon="plus"
        @click="createNewUser"
      >
        New User
      </Button>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-8">
      <span class="loading loading-dots"></span>
    </div>

    <div v-else class="space-y-4">
      <div v-for="user in users" :key="user.name"
        class="flex items-center p-4 bg-white rounded-lg border border-gray-100 hover:border-gray-200 transition-all">
        <div class="flex items-center flex-1">
          <Avatar
            :label="user.full_name"
            :image="user.user_image"
            class="mr-4"
          />
          <div>
            <div class="font-medium text-gray-900">{{ user.full_name }}</div>
            <div class="text-sm text-gray-500">{{ user.name }}</div>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <span
            :class="[
              'px-2 py-1 text-sm rounded-full',
              user.enabled
                ? 'bg-green-100 text-green-800'
                : 'bg-gray-100 text-gray-800'
            ]"
          >
            {{ user.enabled ? 'Active' : 'Disabled' }}
          </span>

          <Dropdown
            :options="getUserActions(user)"
            placement="bottom-end"
          >
            <Button variant="subtle" icon="more-horizontal" />
          </Dropdown>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Avatar, Button, Dropdown } from 'frappe-ui'
import { createResource } from 'frappe-ui'

const loading = ref(true)
const users = ref([])

const userResource = createResource({
  url: 'frappe.desk.page.user_management.user_management.get_all_users',
  transform(data) {
    return data.message || []
  },
  onError(error) {
    console.error('Failed to fetch users:', error)
    frappe.throw({
      title: 'Error',
      message: 'Failed to fetch users'
    })
  }
})

async function loadUsers() {
  loading.value = true
  try {
    const data = await userResource.submit()
    users.value = data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

function getUserActions(user) {
  return [
    {
      label: user.enabled ? 'Disable User' : 'Enable User',
      icon: user.enabled ? 'user-minus' : 'user-check',
      onClick: () => toggleUserStatus(user)
    },
    {
      label: 'Edit User',
      icon: 'edit',
      onClick: () => editUser(user)
    },
    {
      label: 'Reset Password',
      icon: 'key',
      onClick: () => resetPassword(user)
    }
  ]
}

async function toggleUserStatus(user) {
  try {
    await frappe.call({
      method: 'frappe.core.doctype.user.user.toggle_user_status',
      args: {
        user: user.name,
        enabled: !user.enabled
      }
    })
    await loadUsers()
    frappe.toast({
      message: `User ${user.enabled ? 'disabled' : 'enabled'} successfully`,
      type: 'success'
    })
  } catch (error) {
    frappe.toast({
      message: 'Failed to update user status',
      type: 'error'
    })
  }
}

function editUser(user) {
  frappe.set_route('Form', 'User', user.name)
}

async function resetPassword(user) {
  try {
    await frappe.call({
      method: 'frappe.core.doctype.user.user.reset_password',
      args: { user: user.name }
    })
    frappe.toast({
      message: 'Password reset link sent successfully',
      type: 'success'
    })
  } catch (error) {
    frappe.toast({
      message: 'Failed to reset password',
      type: 'error'
    })
  }
}

function createNewUser() {
  frappe.new_doc('User')
}

onMounted(() => {
  loadUsers()
})
</script>
