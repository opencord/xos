'use strict';

angular.module('xos.metronet', [
  'ngResource',
  'ngCookies',
  'ui.router',
  'xos.helpers',
  'ngMap'
])
.config(($stateProvider) => {
  $stateProvider
  .state('metronetMap', {
    url: '/',
    template: '<metronet-map></metronet-map>'
  });
})
.config(function($httpProvider){
  $httpProvider.interceptors.push('NoHyperlinks');
});