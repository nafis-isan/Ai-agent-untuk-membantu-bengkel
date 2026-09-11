export default defineNuxtRouteMiddleware((to) => {
  if (to.path === '/login' || !import.meta.client) return
  if (!localStorage.getItem('bengkelai-token')) return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
})