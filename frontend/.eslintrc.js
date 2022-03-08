module.exports = {
    "env": {
        "browser": true,
        "es2021": true
    },
    "extends": [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:prettier/recommended"
    ],
    "parser": "@typescript-eslint/parser",
    "parserOptions": {
        "ecmaVersion": "latest",
        "sourceType": "module"
    },
    "plugins": [
        "svelte3",
        "@typescript-eslint"
    ],
    "overrides": [
        {
            files: ['*.svelte'],
            processor: 'svelte3/svelte3'
        }
    ],
    "settings": {
        'svelte3/typescript': () => require('typescript')
    },
    "rules": {
    }
}
