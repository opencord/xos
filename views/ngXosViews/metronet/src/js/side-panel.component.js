/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 10/4/16.
 */

(function () {
  'use strict';
  angular.module('xos.metronet')
    .component('metronetSidePanel', {
      controllerAs: 'vm',
      template: `
        <div
            class="metronet-side-panel"
            ng-class="{active: vm.connection}">
            <pre>{{vm.connection | json}}</pre>
        </div>
      `,
      controller: function($rootScope) {
        $rootScope.$on('connection.details', (evt, connection) => {
          this.connection = connection;
          console.log(this.connection, 'aaaaa');
          $rootScope.$apply();
        });

      }
    });
})();

