#!/bin/bash

# Base project folder
PROJECT="frontend-vue"

# List of directories to create
DIRS=(
  "$PROJECT/src/components"
  "$PROJECT/src/views"
  "$PROJECT/public"
)

# List of files to create
FILES=(
  "$PROJECT/src/components/Header.vue"
  "$PROJECT/src/components/Footer.vue"
  "$PROJECT/src/components/ProductCard.vue"
  "$PROJECT/src/views/Login.vue"
  "$PROJECT/src/views/Register.vue"
  "$PROJECT/src/views/Products.vue"
  "$PROJECT/src/views/Checkout.vue"
  "$PROJECT/src/App.vue"
  "$PROJECT/src/main.js"
  "$PROJECT/package.json"
)

# Create directories
for dir in "${DIRS[@]}"; do
  mkdir -p "$dir"
done

# Create empty files
for file in "${FILES[@]}"; do
  touch "$file"
done

echo "Project structure for '$PROJECT' has been created."
