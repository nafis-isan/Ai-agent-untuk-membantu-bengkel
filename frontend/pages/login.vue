<template>
  <main class="flex min-h-screen items-center justify-center bg-slate-950 px-4">
    <form class="w-full max-w-sm rounded-2xl bg-white p-8 shadow-2xl" @submit.prevent="submit">
      <div class="mb-8"><p class="text-sm font-bold uppercase tracking-[0.18em] text-blue-600">BengkelAI</p><h1 class="mt-2 text-2xl font-extrabold text-slate-900">Admin masuk</h1></div>
      <label class="mb-4 block text-sm font-semibold text-slate-700">Username<input v-model="username" class="mt-2 w-full rounded-xl border border-slate-200 px-3 py-3" autocomplete="username" required /></label>
      <label class="mb-5 block text-sm font-semibold text-slate-700">Password<input v-model="password" type="password" class="mt-2 w-full rounded-xl border border-slate-200 px-3 py-3" autocomplete="current-password" required /></label>
      <p v-if="error" class="mb-4 text-sm text-rose-600">{{ error }}</p>
      <button class="w-full rounded-xl bg-blue-600 px-4 py-3 font-bold text-white disabled:bg-slate-300" :disabled="loading">Masuk</button>
    </form>
  </main>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })
const auth = useAuthStore()
const route = useRoute()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const submit = async () => {
  loading.value = true
  error.value = ''
  try {
    await auth.login(username.value, password.value)
    await navigateTo(typeof route.query.redirect === 'string' ? route.query.redirect : '/')
  } catch (err: any) {
    error.value = err?.data?.detail || 'Login gagal.'
  } finally {
    loading.value = false
  }
}
</script>