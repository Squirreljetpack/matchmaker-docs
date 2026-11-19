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
	srcExclude: ["**/%%*"],
	head: [
		["link", { rel: "icon", type: "image/svg+xml", href: "/matchmaker-docs/favicon.svg" }],
		["link", { rel: "alternate icon", type: "image/png", href: "/matchmaker-docs/favicon.png" }],
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
		logo: "/logo.svg",
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
					{ text: "Getting started", link: "/getting-started" },
					{ text: "Using presets", link: "/using-presets" },
					{ text: "Creating presets", link: "/creating-presets" },
				],
			},
			{
				text: "Interface",
				collapsed: false,
				items: [
					{ text: "Input and data sources", link: "/input-and-data" },
					{ text: "Queries", link: "/queries" },
					{ text: "Preview", link: "/preview" },
				],
			},
			{
				text: "Reference",
				collapsed: false,
				items: [
					{ text: "Options", link: "/options" },
					{ text: "Binds", link: "/binds" },
					{ text: "Template", link: "/template" },
					{ text: "Pager", link: "/pager" },
					{ text: "Image", link: "/image" },
					{ text: "Execute", link: "/execute" },
					{ text: "Other", link: "/other" },
				],
			},
			{
				text: "Library",
				collapsed: false,
				items: [
					{ text: "Using the library", link: "/library" },
					{ text: "Library actions", link: "/library-actions" },
					{ text: "Examples", link: "/examples" },
					{ text: "Benchmarks", link: "/benchmarks" },
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