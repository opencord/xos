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
   * @name xos.SlicesEncoder.serviceGrid
   **/

  angular.module('xos.serviceGrid')
  .service('SlicesEncoder', function($q, Slices){

    this.buildTosca = (slices, toscaSpec) => {
      slices = _.reduce(slices, (obj, s) => {
        obj[s.name] = {
          description: s.description,
          type: 'tosca.nodes.Slice',
          properties: {
            network: s.network
          }
        };

        // TODO add slice requirements

        return obj;
      }, {});
      angular.extend(toscaSpec.topology_template.node_templates, slices);
      return toscaSpec;
    };

    this.getServiceSlices = (service, toscaSpec) => {
      const d = $q.defer();
      Slices.query({service: service.id}).$promise
        .then(slices => {
          d.resolve(this.buildTosca(slices, toscaSpec));
        });

      return d.promise;
    };
  });
})();

