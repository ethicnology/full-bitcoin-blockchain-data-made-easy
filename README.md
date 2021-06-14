# full-bitcoin-blockchain-data-made-easy
## prerequisites
Node and NPM are required.
```sh
npm install
```

## usage
Local
```sh
npm run dev
# localhost:8080
```

Build 
```sh
npm run build
# output -> /src/.vuepress/dist
```

## deploy
Before deployment you need to execute :
```sh
npx embedme src/code/README.md
```
It will replace comments to linked python file.

Then, 
```sh
./deploy
```