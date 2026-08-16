import { defineConfig } from "vitepress";

const repo = "https://github.com/Squirreljetpack/matchmaker-docs";

export default defineConfig({
	base: "/matchmaker-docs/",
	lang: "en-US",
	title: "Matchmaker",
	titleTemplate: ":title — Matchmaker",
	description:
		"Matchmaker — a fast, configurable and intuitive fuzzy searcher for the terminal. Documentation.",
	appearance: "dark",
	lastUpdated: true,
	cleanUrls: true,
	head: [
		["meta", { name: "theme-color", content: "#08090a" }],
		["link", { rel: "preconnect", href: "https://fonts.googleapis.com" }],
		[
			"link",
			{ rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "" },
		],
		[
			"link",
			{
				rel: "stylesheet",
				href: "https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap",
			},
		],
	],
	themeConfig: {
		siteTitle: "Matchmaker",
		nav: [{ text: "Docs", link: "/" }],
		socialLinks: [
			{ icon: "github", link: "https://github.com/Squirreljetpack/matchmaker" },
		],
		sidebar: [
			{
				text: "Getting started",
				collapsed: false,
				items: [
					{ text: "Getting started", link: "/01-getting-started" },
					{ text: "Core workflows", link: "/02-core-workflows" },
				],
			},
			{
				text: "The interface",
				collapsed: false,
				items: [
					{ text: "Interface overview", link: "/03-interface" },
					{ text: "Input & data sources", link: "/04-input-and-data" },
					{ text: "Columns", link: "/05-columns" },
					{ text: "Preview", link: "/06-preview" },
					{ text: "Queries & matching", link: "/07-querying" },
				],
			},
			{
				text: "Configuration",
				collapsed: false,
				items: [
					{ text: "Configuration files", link: "/08-configuration" },
					{ text: "Presets & workflows", link: "/09-presets" },
				],
			},
			{
				text: "References",
				collapsed: false,
				items: [
					{ text: "Command line", link: "/10-command-line" },
					{ text: "Binds & actions", link: "/11-binds-and-actions" },
					{ text: "Templates", link: "/12-templates" },
					{ text: "Queries & misc (mm --doc other)", link: "/13-queries-and-misc" },
				],
			},
			{
				text: "Scripting & development",
				collapsed: false,
				items: [
					{ text: "Scripting", link: "/14-scripting" },
					{ text: "Lua commands", link: "/15-lua" },
					{ text: "Using the library", link: "/16-library" },
					{ text: "Diagnostics & logging", link: "/17-diagnostics" },
				],
			},
		],
		search: {
			provider: "local",
			options: {
				detailedView: true,
			},
		},
		outline: { level: [2, 3], label: "On this page" },
		editLink: {
			pattern: `${repo}/edit/main/docs/:path`,
			text: "Edit this page on GitHub",
		},
		lastUpdated: { text: "Last updated" },
		docFooter: { prev: "Previous", next: "Next" },
		darkModeSwitchLabel: "Theme",
		returnToTopLabel: "Back to top",
	},
});