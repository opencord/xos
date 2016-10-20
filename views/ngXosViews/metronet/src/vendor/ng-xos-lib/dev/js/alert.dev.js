'use strict';

angular.module('ngXosLib')
  .component('alertTest', {
    restrict: 'E',
    bindings: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/alert.dev.html',
    controller: function () {
      this.config1 = {
        type: 'danger'
      };

      this.config2 = {
        type: 'danger',
        closeBtn: true
      };

      this.config3 = {
        type: 'info'
      };

      this.config4 = {
        type: 'success'
      };

      this.config5 = {
        type: 'warning'
      };
    }
  })