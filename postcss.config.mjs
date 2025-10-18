export default {
	plugins: {
		// https://postcss.org/docs/postcss-plugins
		"@tailwindcss/postcss": {},
		"postcss-preset-env": {
			// https://github.com/Kozea/WeasyPrint/issues/1998
			stage: 1,
			features: {
				// https://github.com/csstools/postcss-plugins/blob/main/plugin-packs/postcss-preset-env/FEATURES.md
				// https://github.com/csstools/postcss-plugins/tree/main/plugins/postcss-custom-properties#readme
				"custom-properties": { preserve: false },
			},
		},
	},
}
