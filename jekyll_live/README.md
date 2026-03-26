# Jekyll Live Builder (Home Assistant Add-on)

A lightweight Home Assistant add-on that runs a Jekyll build in watch mode or 
one-shot mode.

Inspired by the idea to have simple wiki-style sites served directly from Home 
Assistant.

---

## Features

- Live rebuild using `jekyll build --watch`
- Configurable source and output directories
- Uses standard Jekyll Docker image (no custom Ruby setup required)
- Outputs directly to Home Assistant `/config/www` for HTTPS serving
- Available one-shot mode

---

## Directory Structure

Example setup:

```
/config/
├── jekyll/     # Your Jekyll source (markdown, layouts, config.yml)
├── www/                # Built site output (served at /local/)
```

---

## Configuration

Set these in the add-on UI:

```yaml
jekyll_dir: /config/jekyll
output_dir: /config/www
```

### Options

| Option       | Description                     |
|--------------|---------------------------------|
| jekyll_dir   | Path to your Jekyll site source |
| output_dir   | Path where built site is placed |
| incremental  | Enables `--incremental` builds |
| one_shot     | Run once and exit (no watch mode) |
| custom_args  | Additional arguments passed to Jekyll |

---

## Usage

1. Place your Jekyll site in the configured `jekyll_dir`
2. Ensure your site contains:
   - `_config.yml`
   - `Gemfile` (recommended)
3. Start the add-on
4. Edit your markdown files
5. Jekyll will automatically rebuild the site unless one_shot is enabled

---

## How It Works

- Add-on reads configuration from `/data/options.json`
- Runs:

```
jekyll build --watch --force_polling
```

- Outputs static files to your configured directory
- Home Assistant serves files via its built-in web server

---

## Notes

### Gemfile Recommended

If your site uses themes or plugins:

```ruby
gem "jekyll-theme-your-theme"
```

The add-on will run:

```
bundle install
bundle exec jekyll build
```

---

### File Watching

The add-on uses:

```
--watch --force_polling
```

to ensure file changes are detected reliably inside Docker.

---

### Permissions

All paths must be under `/config`.

---

## Site Development

For any and all questions about how to use Jekyll, refer to their documentation: 
[**Jekyll**](https://jekyllrb.com/docs/)

---

## Summary

This add-on provides a simple workflow:

Edit markdown → rebuild → view in browser

For editing markdown directly on your Home Assistant, I recommend the built-in 
file editor, which you can reach by going to
>**`Settings > Apps > File editor`**

---
## Installation

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fzuidec%2Fha-addon-jekyll-live
)

If you want to do add the repository manually, please follow the procedure highlighted in the [Home Assistant website](https://home-assistant.io/hassio/installing_third_party_addons). Use the following URL to add this repository: https://github.com/zuidec/ha-addon-jekyll-live


[repository-badge]: https://img.shields.io/badge/Add%20repository%20to%20my-Home%20Assistant-41BDF5?logo=home-assistant&style=for-the-badge
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fzuidec%2Fha-addon-jekyll-live

---
## License

This repository is distributed under the MIT License.

Jekyll docker images are distributed under the ISC License.
