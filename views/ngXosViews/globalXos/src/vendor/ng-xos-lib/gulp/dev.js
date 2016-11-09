/*eslint-env node */
(function () {
  'use strict';

  const gulp = require('gulp');
  const inject = require('gulp-inject');
  const angularFilesort = require('gulp-angular-filesort');
  const wiredep = require('wiredep').stream;
  const path = require('path');
  const babel = require('gulp-babel');
  const sourcemaps = require('gulp-sourcemaps');
  const browserSync = require('browser-sync').create();
  module.exports = function(options){

    console.log(options.xosHelperTmp, path.join(__dirname, `../${options.xosHelperTmp}`));

    gulp.task('serveDevEnv', ['babelDev', 'wiredep', 'inject', 'injectStyle'], function(){
      browserSync.init({
        server: {
          baseDir: ['./dev', './.tmp', './dist'],
          // directory: true,
          routes: {
            '/bower_components': 'bower_components'
          },
        }
      });

      gulp.watch([
        './src/**/*.js'
      ], ['babelDev']);

      gulp.watch([
        './src/**/*.scss'
      ], ['style']);

      gulp.watch([
        './dev/*.html',
        './dev/*.js',
        './.tmp/**/*.js'
      ], function(){
        browserSync.reload();
      });
    });

    gulp.task('babelDev', function(){
      return gulp.src(options.xosHelperSource + '**/*.js')
        .pipe(sourcemaps.init())
        .pipe(babel({
          presets: ['es2015']
        }))
        .pipe(sourcemaps.write('./maps'))
        .pipe(gulp.dest(options.xosHelperTmp));
    });

    gulp.task('inject', function(){
      const files = gulp.src([
        `${options.xosHelperTmp}**/*.js`
      ])
      .pipe(angularFilesort())

      return gulp.src('./dev/index.html')
        .pipe(inject(files, {ignorePath: ['.tmp/']}))
        .pipe(gulp.dest('./dev/'));
    });

    gulp.task('injectStyle', function(){
      const files = gulp.src([
        `${options.ngXosStyles}*.css`
      ])

      return gulp.src('./dev/index.html')
        .pipe(inject(files, {ignorePath: ['dist/']}))
        .pipe(gulp.dest('./dev/'));
    });
    

    // inject bower dependencies with wiredep
    gulp.task('wiredep', function () {
      return gulp.src('./dev/index.html')
        .pipe(wiredep({devDependencies: false}))
        .pipe(gulp.dest('./dev'));
    });
  };
})();