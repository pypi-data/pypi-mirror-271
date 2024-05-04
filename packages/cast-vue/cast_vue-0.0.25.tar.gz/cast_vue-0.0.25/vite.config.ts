import { resolve } from "path";
import { defineConfig } from "vite";
import Vue from "@vitejs/plugin-vue";
import type { UserConfig as VitestUserConfigInterface } from "vitest/config"

const vitestConfig: VitestUserConfigInterface = {
  test: {
    globals: true,
    environment: "jsdom",
  },
}

export default defineConfig({
  plugins: [Vue()],
  test: vitestConfig.test,
  root: resolve("./cast_vue/static/src/"),
  base: "/static/",
  server: {
    host: "0.0.0.0",
    port: 5173,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: [".js", ".json", ".ts"],
    alias: {
      "@": resolve("./cast_vue/static/src/js/cast_vue"),
    },
  },
  build: {
    outDir: resolve("./cast_vue/static/cast_vue"),
    assetsDir: "",
    manifest: true,
    emptyOutDir: true,
    target: "es2015",
    rollupOptions: {
      input: {
        main: resolve("./cast_vue/static/src/js/cast_vue/main.ts"),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
})
