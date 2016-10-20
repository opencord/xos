'use strict';

angular.module('ngXosLib')
  .component('tableTest', {
    restrict: 'E',
    bindings: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/table.dev.html',
    controller: function () {
      this.config = {
        columns: [
          {
            label: '#',
            prop: 'id'
          },
          {
            label: 'Name:',
            prop: 'name'
          }
        ]
      };
      this.data = [{id: 1, name: 'Jhon'}]
    }
  })