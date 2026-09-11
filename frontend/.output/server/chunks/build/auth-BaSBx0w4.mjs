import { d as defineNuxtRouteMiddleware } from '../virtual/entry.mjs';
import 'nostics';
import 'nostics/formatters/ansi';
import 'vue';
import '../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';
import '@iconify/utils';
import 'consola';
import '../routes/renderer.mjs';
import 'unhead/server';
import 'unhead/legacy';
import 'unhead/plugins';
import 'vue-bundle-renderer/runtime';
import 'vue/server-renderer';
import 'devalue';
import 'vue-router';
import '@vue/shared';
import 'pinia';
import '@iconify/vue';
import 'tailwindcss/colors';
import 'unhead/utils';

//#region middleware/auth.ts
var auth_default = defineNuxtRouteMiddleware((to) => {
	if (to.path === "/login" || true) return;
});

export { auth_default as default };
//# sourceMappingURL=auth-BaSBx0w4.mjs.map
