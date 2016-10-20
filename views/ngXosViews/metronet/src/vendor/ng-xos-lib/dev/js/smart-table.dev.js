(function () {
  'use strict';

  const data = [
    {
      'humanReadableName': 'cordSubscriber-1',
      'id': 1,
      'features': {
        'cdn': false,
        'uplink_speed': 1000000000,
        'downlink_speed': 1000000000,
        'uverse': true,
        'status': 'enabled'
      },
      'identity': {'account_num': '123',
      'name': 'My House'},
      'related': {
        'instance_name': 'mysite_vsg',
        'vsg_id': 7,
        'compute_node_name': 'nova-compute-1',
        'c_tag': 111,
        'instance_id': 1,
        'wan_container_ip': '10.168.0.3',
        'volt_id': 6,
        's_tag': 222
      }
    }
  ]

  angular.module('ngXosLib')
  .service('Resource', function($q){
    this.query = () => {
      const d = $q.defer();
      console.log(data);
      d.resolve(data)

      return {$promise: d.promise}
    }
  })
  .component('smartTableTest', {
    restrict: 'E',
    bindings: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/smart-table.dev.html',
    controller: function () {
      this.config = {
        resource: 'Resource'
      };
    }
  })
})(); 