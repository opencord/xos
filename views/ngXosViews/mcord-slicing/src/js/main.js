'use strict';

angular.module('xos.mcord-slicing', [
  'ngResource',
  'ngCookies',
  'ui.router',
  'xos.helpers'
])
.config(($stateProvider) => {
  $stateProvider
  .state('slicing-topo', {
    url: '/',
    template: '<slicing-topo></slicing-topo>'
  })
  .state('node-links', {
    url: '/data',
    template: '<node-links></node-links>'
  });
})
.config(function($httpProvider){
  $httpProvider.interceptors.push('NoHyperlinks');
})
.service('McordSlicingTopo', function($http, $q){
  this.query = () => {
    const d = $q.defer();

    $http.get('api/services/mcord/slicing')
    .then((res) => {
      // INVESTIGATE why proxy change resposne
      const data = {
        slices: res.data[0],
        upstreams: res.data[1],
        'ue-groups': res.data[2],
        // mmes: res.data[3]
      };
      d.resolve(data);
    })
    .catch((e) => {
      d.reject(e);
    });

    return {$promise: d.promise};
  };
})
.directive('nodeLinks', function(){
  return {
    restrict: 'E',
    scope: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/node-links.tpl.html',
    controller: function(McordSlicingTopo){

      this.tableConfig = {
        columns: [
          {
            label: 'Id',
            prop: 'id'
          },
          {
            label: 'Name',
            prop: 'name'
          },
          {
            label: 'Type',
            prop: 'type'
          },
          {
            label: 'Plane',
            prop: 'plane'
          },
          {
            label: 'Model Id',
            prop: 'model_id'
          }
        ]
      };
      
      // retrieving user list
      McordSlicingTopo.query().$promise
      .then((users) => {
        this.users = users.nodes;
      })
      .catch((e) => {
        throw new Error(e);
      });
    }
  };
});