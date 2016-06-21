/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 6/22/16.
 */

(function () {
  'use strict';

  /**
   * @ngdoc service
   * @name xos.NetworkEncoder.serviceGrid
   **/

  angular.module('xos.serviceGrid')
    .service('NetworkEncoder', function($q, Networks){

      this.buildTosca = (networkId, toscaSpec) => {
        const d = $q.defer();

        Networks.get({id: networkId}).$promise
          .then(network => {
            const toscaObj = {};
            toscaObj[`network#${network.name}`] = {
              type: 'tosca.nodes.Network.XOS',
              properties: {
                'no-create': true,
                'no-delete': true,
                'no-update': true
              }
            };
            angular.extend(toscaSpec.topology_template.node_templates, toscaObj);
            d.resolve(toscaSpec);
          })
          .catch(d.reject);


        return d.promise;
      };
    });
})();

