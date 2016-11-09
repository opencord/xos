/*eslint-env node */
(function () {
  'use strict';

  const gulp = require('gulp');
  const wrench = require('wrench');
  const path = require('path');

  const options = {
    ngXosVendor: './dist/',
    ngXosStyles: './dist/',
    xosHelperSource: './src/',
    xosHelperTmp: './.tmp/',
    docs: './docs'
  };

  wrench.readdirSyncRecursive(path.join(__dirname, './gulp'))
  .map(function(file) {
    require(path.join(__dirname, './gulp/' + file))(options);
  });

  gulp.task('default', function () {
    gulp.start('build');
  });

  gulp.task('build', ['vendor', 'helpers', 'uiLibrary']);

})(); 