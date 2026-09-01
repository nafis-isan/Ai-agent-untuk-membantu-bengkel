// https://nuxt.com/docs/api/composables/use-fetch
export const useFetchAPI = (url: string, options = {}) => {
  const config = useRuntimeConfig()
  return useFetch(() => `${config.public.apiBase}${url}`, {
    ...options
  })
}
