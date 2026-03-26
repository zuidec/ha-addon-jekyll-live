# Jekyll Live Builder (Home Assistant Add-on)

A lightweight Home Assistant add-on that runs a Jekyll build in **watch mode**, automatically rebuilding your static site whenever your markdown files change.

Designed for simple wiki-style sites served directly from Home Assistant.

---

## Features

- Live rebuild using `jekyll build --watch`
- Configurable source and output directories
- Uses standard Jekyll Docker image (no custom Ruby setup required)
- Outputs directly to Home Assistant `/config/www` for HTTPS serving
- Works with an external preprocessing pipeline

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

---

## Usage

1. Place your Jekyll site in the configured `jekyll_dir`
2. Ensure your site contains:
   - `_config.yml`
   - `Gemfile` (recommended)
3. Start the add-on
4. Edit your markdown files
5. Jekyll will automatically rebuild the site

---

## Accessing Your Site

Anything built into:

```
/config/www/
```

is available at:

```
https://<your-home-assistant>/local/
```

Example:

```
https://homeassistant.local/local/
```
>[!WARNING]
>Unlike a normal webserver, index.html is NOT automatically served.
>To access the site you have to request the file explicitly, e.g.
>`https://<your-home-assistant>/local/index.html`
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
gem "jekyll-theme-basically-basic"
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

All paths must be under `/config` unless additional mappings are added.

---

## Troubleshooting

### No configuration options visible

Refresh or reinstall the add-on

---

### Jekyll build fails (missing theme/plugin)

Make sure your `Gemfile` includes required gems and is located in your `jekyll_dir`.

---

### Sass errors / "Broken pipe"

Pin the Sass converter in your `Gemfile`:

```ruby
gem "jekyll-sass-converter", "2.2.0"
```

---

## Development

Add-on structure:

```
/config/addons/local/jekyll_live/
├── config.yaml
├── Dockerfile
├── run.sh
└── README.md
```

---

## Future Improvements

- Optional one-shot build mode
- Pre-build hook (run preprocessing script)
- Incremental builds

---

## Summary

This add-on provides a simple workflow:

Edit markdown → automatic rebuild → view in browser

For editing markdown directly on your homeassistant, I recommend the built-in file editor, which you can reach by going to
>**`Settings > Apps > File editor`**

---

## License

MIT 

