/* eslint-disable angular/ng_module_name */
(function(){
  'use strict';
  angular.module('ngXosLib', ['xos.helpers', 'ui.router'])
  .config(($stateProvider) => {
    $stateProvider
    .state('form-test', {
      url: '/form/',
      template: '<form-test></form-test>'
    })
    .state('table-test', {
      url: '/table/',
      template: '<table-test></table-test>'
    })
    .state('alert-test', {
      url: '/alert/',
      template: '<alert-test></alert-test>'
    })
    .state('field-test', {
      url: '/field/',
      template: '<field-test></field-test>'
    })
    .state('smart-table-test', {
      url: '/smartTable/',
      template: '<smart-table-test></smart-table-test>'
    })
  })
  .component('navDemo', {
    restrict: 'E',
    bindings: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/nav.dev.html',
    controller: function ($rootScope) {

      this.active = 'form';

      $rootScope.$on('$stateChangeSuccess', (event, toState) => {
        let strSelected = toState.url.split('/').join('');
        this.active = strSelected.charAt(0).toUpperCase() + strSelected.slice(1);
      });

      this.config = {
        actions: [
          {
            label: 'Form',
            class: '',
            link: '/#/form/'
          },
          {
            label: 'Field',
            class: '',
            link: '/#/field/'

          },
          {
            label: 'Alert',
            class: '',
            link: '/#/alert/'

          },
          {
            label: 'Table',
            class: '',
            link: '/#/table/'
          },
          {
            label: 'SmartTable',
            class: '',
            link: '/#/smartTable/'
          }
        ]
      }
    }
  });

})();