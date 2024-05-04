# Installing Vue.js Theme for Django-Cast

This document provides the instructions on how to install the Vue.js theme for Django-Cast. Please follow the steps below.

## Installation

### 1. Install the theme

To install the Vue.js theme, you will need to run the following command in your command line:

```shell
pip install cast-vue
```

### 2. Add entries to INSTALLED_APPS

You will need to add `django_vite` and `cast_vue.apps.CastVueConfig`
to your INSTALLED_APPS in your Django settings.

Then, set the DJANGO_VITE_ASSETS_PATH and DJANGO_VITE_DEV_MODE like so:

```python
INSTALLED_APPS = [
    ...
    'django_vite',
    'cast_vue.apps.CastVueConfig',
    ...
]

# For production
DJANGO_VITE_ASSETS_PATH = ROOT_DIR.path("staticfiles").path("cast_vue")  # does not matter for development
DJANGO_VITE_MANIFEST_PATH = DJANGO_VITE_ASSETS_PATH.path("manifest.json")
DJANGO_VITE_STATIC_URL_PREFIX = "cast_vue/"  # really important for production!
DJANGO_VITE_DEV_MODE = DEBUG

# For development
DJANGO_VITE_ASSETS_PATH = "need to be set but doesn't matter"
DJANGO_VITE_DEV_MODE = True
```

### 3. Set the theme in Wagtail admin

You can set the theme to `vue` in the Wagtail admin for the
complete site or just one blog.

### End

That's it! You have successfully installed and set up the Vue.js theme
for [`django-cast`](https://github.com/ephes/django-cast).

## Development

### Run Vite Development Server

```shell
npx vite
```

Then the vue app will be available at `http://localhost:8000`, the
url of the django app. If there's nothing to see, the actual port of vite
dev server (5173, was 3000 some time ago) and the port `django-vite` uses
(5173) might be different.

### Run Tests

Just the tests:
```shell
npx vitest -r cast_vue/static/src/tests
```

With coverage:
```shell
npm run coverage
```

### Build

This works:
```shell
npx vite build
```

After that, you need to copy the bundle files to `cast_vue/static/dist`:
```shell
cp cast_vue/static/cast_vue/* cast_vue/static/dist
```

After that, you need to copy the manifest.json to `cast_vue/static/dist`:
```shell
cp cast_vue/static/cast_vue/.vite/manifest.json cast_vue/static/dist
```

Commit the whole stuff and push.

This does not work!
```shell
npm run build
```

Don't forget to commit the changes in `cast_vue/static/dist`!

### Update Dependencies

```shell
npx npm-check-updates -u
```
