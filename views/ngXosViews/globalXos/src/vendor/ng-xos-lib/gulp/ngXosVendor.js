/*eslint-env node */
(function () {
  
  'use strict';
  const gulp = require('gulp');
  const uglify = require('gulp-uglify');
  const concat = require('gulp-concat');
  const wiredep = require('wiredep');
  const del = require('del');

  module.exports = function(options){

    gulp.task('cleanVendor', function(){
      return del(
        [
          `${options.ngXosVendor}/ngXosVendor.min.js`
        ],
        {force: true}
      );
    });

    gulp.task('vendor', ['cleanVendor'], function(){
      const bowerDeps = wiredep().js;
      return gulp.src(bowerDeps)
        .pipe(concat('ngXosVendor.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest(options.ngXosVendor));
    });
  };
})();