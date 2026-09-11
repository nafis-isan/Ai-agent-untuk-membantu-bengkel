import { $ as $fetch } from '../_/nitro.mjs';

//#region composables/useAPI.ts
var getAuthHeaders = () => {
	return {};
};
var apiFetch = async (url, options = {}) => {
	try {
		return await $fetch(url, {
			...options,
			headers: {
				...getAuthHeaders(),
				...options.headers || {}
			}
		});
	} catch (error) {
		throw error;
	}
};

export { apiFetch as a };
//# sourceMappingURL=useAPI-DRNp7d_T.mjs.map
