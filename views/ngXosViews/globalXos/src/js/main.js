'use strict';

angular.module('xos.globalXos', [
  'ngResource',
  'ngCookies',
  'ui.router',
  'xos.helpers'
])
.config(($stateProvider) => {
  $stateProvider
  .state('xos-list', {
    url: '/',
    template: '<xos-list></xos-list>'
  });
})
.config(function($httpProvider){
  $httpProvider.interceptors.push('NoHyperlinks');
})
.directive('xosList', function(){
  return {
    restrict: 'E',
    scope: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/xos-list.tpl.html',
    controller: function(Controllers){

      Controllers.query({backend_type: 'XOS'}).$promise
      .then(res => {
        this.xoss = res;
      });
    }
  };
});