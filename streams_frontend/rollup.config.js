import svelte from 'rollup-plugin-svelte';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import livereload from 'rollup-plugin-livereload';
import includePaths from 'rollup-plugin-includepaths';
import postcss from 'rollup-plugin-postcss';

const production = !process.env.ROLLUP_WATCH;

let includePathOptions = {
	include: {},
	paths: ['src'],
	external: [],
	extensions: ['.js', '.json', '.html']
};

export default {
	input: 'src/main.js',
	output: {
		sourcemap: !production,
		format: 'iife',
		name: 'app',
		file: 'public/bundle.js'
	},
	plugins: [
		svelte({
			// enable run-time checks when not in production
			dev: !production,
			// we'll extract any component CSS out into
			// a separate file — better for performance
			emitCss: true,
			css: css => {
				css.write('public/bundle.css');
			}
		}),

		// If you have external dependencies installed from
		// npm, you'll most likely need these plugins. In
		// some cases you'll need additional configuration —
		// consult the documentation for details:
		// https://github.com/rollup/rollup-plugin-commonjs
		resolve({
			browser: true,
			dedupe: importee => importee === 'svelte' || importee.startsWith('svelte/')
		}),
		commonjs(),
		postcss({
			extract: true,
			minimize: true,
			use: [
				['sass', {
					includePaths: [
						'./src/theme',
						'./node_modules'
					]
				}]
			]
		}),
		includePaths(includePathOptions),

		// Watch the `public` directory and refresh the
		// browser on changes when not in production
		!production && livereload('public')
	],
	watch: {
		clearScreen: false
	}
};
