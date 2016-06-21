'use strict';

angular.module('xos.toscaExporter', [
  'ngResource',
  'ngCookies',
  'ui.router',
  'xos.helpers'
])
.config(($stateProvider) => {
  $stateProvider
  .state('user-list', {
    url: '/',
    template: '<users-list></users-list>'
  });
})
.config(function($httpProvider){
  $httpProvider.interceptors.push('NoHyperlinks');
})
.directive('usersList', function(){
  return {
    restrict: 'E',
    scope: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/services-list.tpl.html',
    controller: function(Services, ToscaEncoder){
      
      this.tableConfig = {
        columns: [
          {
            label: '#',
            prop: 'id'
          },
          {
            label: 'Status',
            prop: 'status',
            type: 'icon',
            formatter: item => {
              let status = parseInt(item.backend_status.match(/^[0-9]/)[0]);
              switch(status){
                case 0:
                  return 'time';
                case 1:
                  return 'ok';
                case 2:
                  return 'remove';
              }
            }
          },
          {
            label: 'Name',
            prop: 'name',
            link: item => `${item.view_url.replace(/\$[a-z]+\$/, item.id)}`
          },
          {
            label: 'Kind',
            prop: 'kind'
          },
          {
            label: 'Enabled',
            prop: 'enabled',
            type: 'boolean'
          }
        ],
        actions: [
          {
            label: 'export',
            icon: 'export',
            cb: service => {
              this.tosca = '';
              ToscaEncoder.serviceToTosca(service)
                .then(tosca => {
                  console.log('tosca', tosca);
                  this.tosca = tosca;
                });
            }
          }
        ],
        order: true
      };

      // retrieving user list
      Services.query().$promise
      .then((services) => {
        this.services = services;
      })
      .catch((e) => {
        throw new Error(e);
      });
    }
  };
});