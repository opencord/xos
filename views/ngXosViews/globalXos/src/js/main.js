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
.value('LXOS', [])
.directive('xosList', function(){
  return {
    restrict: 'E',
    scope: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/xos-list.tpl.html',
    controller: function($window, $q, _, Controllers, LXOS, LocalAuth, LocalSlices, LocalUsers){

      Controllers.query({backend_type: 'XOS'}).$promise
      .then(res => {
        this.xoss = res;
      });

      this.sliceTableCfg = {
        columns: [
          {
            label: 'Name',
            prop: 'name',
          },
          {
            label: 'Max Instances',
            prop: 'max_instances'
          },
          {
            label: 'Default Isolation',
            prop: 'default_isolation'
          },
          {
            label: 'Mount Data Sets',
            prop: 'mount_data_sets'
          },
          {
            label: 'L-XOS',
            type: 'custom',
            formatter: item => item.xos.name
          }
        ],
        actions: [
          {
            label: 'open locally',
            icon: 'open',
            cb: (item) => {
              $window.open(`${item.xos.auth_url}admin/core/slice/${item.id}`, '_blank');
            },
          }
        ],
        filter: 'field',
        order: true
      };

      this.usersTableCfg = {
        columns: [
          {
            label: 'Name',
            type: 'custom',
            formatter: item => `${item.firstname} ${item.lastname}`
          },
          {
            label: 'E-Mail',
            prop: 'email'
          },
          {
            label: 'User Name',
            prop: 'username'
          },
          {
            label: 'Time Zone',
            prop: 'timezone'
          },
          {
            label: 'L-XOS',
            type: 'custom',
            formatter: item => item.xos.name
          }
        ],
        actions: [
          {
            label: 'open locally',
            icon: 'open',
            cb: (item) => {
              $window.open(`${item.xos.auth_url}admin/core/user/${item.id}`, '_blank');
            },
          }
        ],
        filter: 'field',
        order: true
      }

      this.toggleXos = (xos) => {
        if(_.findIndex(LXOS, {id: xos.id}) > -1){
          xos.active = false;
          _.remove(LXOS, {id: xos.id});
        }
        else{
          xos.active = true;
          LXOS.push(xos);
        }

        // authenticate on L-XOS
        LocalAuth.login()
        .then(() => {
          // fetch slices
          return $q.all([
            LocalSlices.query().$promise,
            LocalUsers.query().$promise,
          ]);
        })
        .then(res => {
          [this.localSlices, this.localUsers] = res;
        })
        .catch(e => {
          console.log(e);
        });
      }
    }
  };
});