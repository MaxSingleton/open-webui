import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

import { viteStaticCopy } from 'vite-plugin-static-copy';

// /** @type {import('vite').Plugin} */
// const viteServerConfig = {
// 	name: 'log-request-middleware',
// 	configureServer(server) {
// 		server.middlewares.use((req, res, next) => {
// 			res.setHeader('Access-Control-Allow-Origin', '*');
// 			res.setHeader('Access-Control-Allow-Methods', 'GET');
// 			res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
// 			res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
// 			next();
// 		});
// 	}
// };

export default defineConfig({
	plugins: [
		sveltekit(),
		viteStaticCopy({
			targets: [
				{
					src: 'node_modules/onnxruntime-web/dist/*.jsep.*',

					dest: 'wasm'
				}
			]
		})
	],
	define: {
		APP_VERSION: JSON.stringify(process.env.npm_package_version),
		APP_BUILD_HASH: JSON.stringify(process.env.APP_BUILD_HASH || 'dev-build')
   },
  // Dev server: hot-reload UI and proxy API calls to backend
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://open-webui:8080',
        changeOrigin: true
      },
      '/health': {
        target: 'http://open-webui:8080',
        changeOrigin: true
      },
      '/socket.io': {
        target: 'http://open-webui:8080',
        ws: true
      }
    }
  },
	build: {
		sourcemap: true
	},
	worker: {
		format: 'es'
	}
});
