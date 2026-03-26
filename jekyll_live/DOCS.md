# Jekyll Live Builder

Jekyll Live Builder runs a Jekyll site in watch mode or one-shot mode inside 
Home Assistant.

It is intended for simple wiki-style sites where source files live under 
`/config/jekyll` and the built site is written to `/config/www` so Home 
Assistant can serve it at `/local/`.

## Configuration

Default add-on configuration:

```yaml
jekyll_dir: /config/jekyll
output_dir: /config/www
incremental: false
one_shot: false
custom_args: ""
```

### Options

- `jekyll_dir`: Path to the Jekyll site source directory.
- `output_dir`: Path where the built site should be written.
- `custom_args`: any custom arguments you'd like to pass to the `jekyll build` 
command
- One-shot: build once and exit (default is to continue watching and 
regenerating)
- Incremental: faster rebuilds

Both paths should stay under `/config`.

## Usage

1. Put your Jekyll site in the configured `jekyll_dir`.
2. Make sure the site includes `_config.yml`.
3. A `Gemfile` is recommended if your site uses a theme or plugins.
4. Start the add-on.
5. Edit files in your Jekyll directory. The add-on will rebuild automatically 
   unless `one_shot` is set

## Notes

- The add-on runs Jekyll with watch mode enabled unless one_shot is enabled.
- `--force_polling` is used so file watching works more reliably in a container.
- If a `Gemfile` is present, the add-on uses `bundle install` and `bundle exec jekyll build`.

## Troubleshooting

>[!IMPORTANT]
>Always check the logs first!

### `Error: Jekyll source directory does not exist:`

Check the `jekyll_dir` in your configuration to make sure that it is pointing to 
the right location.

### Theme or plugin not found

Add the required gems to your site's `Gemfile`.

Example:

```ruby
gem "jekyll-theme-your-theme"
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

An easy way to use this is to create a Web Dashboard pointing at your local 
site, enabling access to simple websites right in home assistant.
