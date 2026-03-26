#!/bin/sh
set -e

CONFIG_PATH="/data/options.json"

# Default values if options.json is missing or incomplete
JEKYLL_DIR="/config/jekyll-recipes"
OUTPUT_DIR="/config/www"

if [ -f "$CONFIG_PATH" ]; then
  JEKYLL_DIR="$(ruby -rjson -e '
    data = JSON.parse(File.read(ARGV[0]))
    puts(data["jekyll_dir"] || ARGV[1])
  ' "$CONFIG_PATH" "$JEKYLL_DIR")"

  OUTPUT_DIR="$(ruby -rjson -e '
    data = JSON.parse(File.read(ARGV[0]))
    puts(data["output_dir"] || ARGV[1])
  ' "$CONFIG_PATH" "$OUTPUT_DIR")"
fi

echo "Using Jekyll source: $JEKYLL_DIR"
echo "Using output directory: $OUTPUT_DIR"

if [ ! -d "$JEKYLL_DIR" ]; then
  echo "Error: Jekyll source directory does not exist: $JEKYLL_DIR" >&2
  exit 1
fi

cd "$JEKYLL_DIR"

echo "Updating bundle..."

bundle config set path vendor/bundle
bundle install

echo "Starting Jekyll in watch mode..."

if [ -f "Gemfile" ]; then
  bundle config set path vendor/bundle
  bundle install
  exec bundle exec jekyll build \
    --source "${JEKYLL_DIR}" \
    --destination "${OUTPUT_DIR}" \
    --watch \
    --force_polling
else
  bashio::log.warning "No Gemfile found in ${JEKYLL_DIR}; using system Jekyll"
  exec jekyll build \
    --source "${JEKYLL_DIR}" \
    --destination "${OUTPUT_DIR}" \
    --watch \
    --force_polling
fi
