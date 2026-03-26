#!/bin/sh
set -e

CONFIG_PATH="/data/options.json"

# Default values if options.json is missing or incomplete
JEKYLL_DIR="/config/jekyll"
OUTPUT_DIR="/config/www"
INCREMENTAL="false"
ONE_SHOT="false"
CUSTOM_ARGS=""

if [ -f "$CONFIG_PATH" ]; then
    eval "$(
    ruby -rjson -e '
        data = JSON.parse(File.read(ARGV[0]))

        def shell_escape(value)
        "'"'"'" + value.to_s.gsub("'"'"'", %q('"'"'"'"'"'"'"'"')) + "'"'"'"
        end

        puts "JEKYLL_DIR=#{shell_escape(data["jekyll_dir"] || ARGV[1])}"
        puts "OUTPUT_DIR=#{shell_escape(data["output_dir"] || ARGV[2])}"
        puts "INCREMENTAL=#{shell_escape(data.key?("incremental") ? data["incremental"] : false)}"
        puts "ONE_SHOT=#{shell_escape(data.key?("one_shot") ? data["one_shot"] : false)}"
        puts "CUSTOM_ARGS=#{shell_escape(data["custom_args"] || "")}"
        ' "$CONFIG_PATH" "$JEKYLL_DIR" "$OUTPUT_DIR"
    )"
fi

echo "[config]Using Jekyll source: $JEKYLL_DIR"
echo "[config]Using output directory: $OUTPUT_DIR"
echo "[config]Incremental: $INCREMENTAL"
echo "[config]One-shot: $ONE_SHOT"
echo "[config]Custom args: $CUSTOM_ARGS"

if [ ! -d "$JEKYLL_DIR" ]; then
    echo "\033[31mError: Jekyll source directory does not exist: $JEKYLL_DIR\033[0m" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
cd "$JEKYLL_DIR"

if [ -f "Gemfile" ]; then
    echo "Gemfile found, running \'bundle install\'"
    bundle config set path vendor/bundle
    bundle install
    JEKYLL_CMD="bundle exec jekyll build"
else
    JEKYLL_CMD="jekyll build"
fi

BASE_ARGS="--source \"$JEKYLL_DIR\" --destination \"$OUTPUT_DIR\""

if [ "$INCREMENTAL" = "true" ]; then
    BASE_ARGS="$BASE_ARGS --incremental"
fi

if [ "$ONE_SHOT" = "true" ]; then
    EXTRA_ARGS=""
else
    EXTRA_ARGS="--watch --force_polling"
fi

CMD="$JEKYLL_CMD $BASE_ARGS $EXTRA_ARGS $CUSTOM_ARGS"

echo "Running: $CMD"
exec sh -c "$CMD"
