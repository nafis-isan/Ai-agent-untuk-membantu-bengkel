import { u as useRuntimeConfig } from '../virtual/entry.mjs';
import { ref } from 'vue';
import { $ as $fetch } from '../_/nitro.mjs';
import { defineStore } from 'pinia';

//#region stores/auth.ts
var useAuthStore = defineStore("auth", () => {
	const isAuthenticated = ref(false);
	const user = ref(null);
	const token = ref("");
	const login = async (email, password) => {
		const config = useRuntimeConfig();
		const response = await $fetch(`${config.public.apiBase}/auth/login`, {
			method: "POST",
			body: {
				username: email,
				password
			}
		});
		token.value = response.access_token;
		isAuthenticated.value = true;
		user.value = { username: email };
	};
	const logout = () => {
		isAuthenticated.value = false;
		user.value = null;
		token.value = "";
	};
	return {
		isAuthenticated,
		user,
		token,
		login,
		logout
	};
});

export { useAuthStore as u };
//# sourceMappingURL=auth-CgeVtR3d.mjs.map
