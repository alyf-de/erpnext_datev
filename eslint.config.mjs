import js from "@eslint/js";
import globals from "globals";

export default [
	js.configs.recommended,
	{
		languageOptions: {
			ecmaVersion: 2022,
			sourceType: "module",
			globals: {
				...globals.browser,
				...globals.node,
				frappe: "readonly",
				__: "readonly",
				cint: "readonly",
				cstr: "readonly",
				cur_frm: "readonly",
				cur_dialog: "readonly",
				cur_page: "readonly",
				cur_list: "readonly",
				flt: "readonly",
				locals: "readonly",
				is_null: "readonly",
				in_list: "readonly",
				has_common: "readonly",
				moment: "readonly",
			},
		},
		rules: {
			indent: "off",
			"brace-style": "off",
			"no-mixed-spaces-and-tabs": "off",
			"no-useless-escape": "off",
			"space-unary-ops": ["error", { words: true }],
			"linebreak-style": "off",
			quotes: "off",
			semi: "off",
			camelcase: "off",
			"no-unused-vars": "off",
			"no-console": "warn",
			"no-extra-boolean-cast": "off",
			"no-control-regex": "off",
		},
	},
];
