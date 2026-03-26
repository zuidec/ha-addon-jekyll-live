# Jekyll Live Builder

Jekyll Live Builder runs a Jekyll site in watch mode inside Home Assistant.

It is intended for simple wiki-style sites where source files live under `/config` and the built site is written to `/config/www` so Home Assistant can serve it at `/local/`.

## Configuration

Example add-on configuration:

```yaml
jekyll_dir: /config/jekyll-recipes
output_dir: /config/www
```

### Options

- `jekyll_dir`: Path to the Jekyll site source directory.
- `output_dir`: Path where the built site should be written.

Both paths should stay under `/config` unless you add more directory mappings to the add-on.

## Usage

1. Put your Jekyll site in the configured `jekyll_dir`.
2. Make sure the site includes `_config.yml`.
3. A `Gemfile` is recommended if your site uses a theme or plugins.
4. Start the add-on.
5. Edit files in your Jekyll directory. The add-on will rebuild automatically.

## Notes

- The add-on runs Jekyll with watch mode enabled.
- `--force_polling` is used so file watching works more reliably in a container.
- If a `Gemfile` is present, the add-on uses `bundle install` and `bundle exec jekyll build`.

## Troubleshooting

### No configuration options visible

- Make sure `config.yaml` contains both `options:` and `schema:`.
- Increment the add-on version after changing `config.yaml`.
- Refresh the repository or reinstall the add-on.

### Theme or plugin not found

Add the required gems to your site's `Gemfile`.

Example:

```ruby
gem "jekyll-theme-basically-basic"
```

### Sass conversion errors

If you run into Sass converter issues, pin the converter in your `Gemfile`:

```ruby
gem "jekyll-sass-converter", "2.2.0"
```

## Accessing the site

Files built into `/config/www` are served by Home Assistant under `/local/`.

Example:

```text
https://homeassistant.local/local/
```
>[!WARNING]
>Unlike a normal webserver, index.html is NOT automatically served.
>To access the site you have to request the file explicitly, e.g.
>`https://<your-home-assistant>/local/index.html`
