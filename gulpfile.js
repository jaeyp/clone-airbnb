const gulp = require("gulp");
const image = require("gulp-image");
const postCSS = require("gulp-postcss");
const sass = require("gulp-sass");
const minify = require("gulp-csso");
const del = require("del");

/**
 * Routing Object
 */
const routes = {
  img: {
    src: "assets/img/*",
    dest: "static/img"
  },
  scss: {
    src: "assets/scss/style.css",
    dest: "static/css"
  }
};

/**
 * Task Methods
 */
const taskImg = () =>
  gulp
    .src(routes.img.src)
    .pipe(image())
    .pipe(gulp.dest(routes.img.dest));

const taskStyle = () =>
  gulp
    .src("assets/scss/style.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(postCSS([require("tailwindcss"), require("autoprefixer")]))
    .pipe(minify())
    .pipe(gulp.dest("static/css"));

const clean = () => del(["static"]);

/**
 * Series/Parallel Methods
 */
const prepare = gulp.series([clean]);
const jobs = gulp.series([taskImg, taskStyle]);

/**
 * Exports Methods
 */
exports.clean = gulp.series([clean]);
exports.css = gulp.series([taskStyle]);
exports.default = gulp.series([prepare, jobs]); // npm run build
