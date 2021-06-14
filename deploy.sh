#!/usr/bin/env sh

# abort on errors
set -e

# embed python files in markdown
npx embedme src/code/README.md

# build
npm run build

# navigate into the build output directory
cd src/.vuepress/dist

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:ethicnology/full-bitcoin-blockchain-data-made-easy.git main:gh-pages

cd -