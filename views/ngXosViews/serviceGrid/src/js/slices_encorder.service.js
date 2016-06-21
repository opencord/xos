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
      const d = $q.defer();
      slices = _.reduce(slices, (obj, s) => {
        obj[s.name] = {
          type: 'tosca.nodes.Slice',
          properties: {
            network: s.network
          }
        };

        if(angular.isDefined(s.description)){
          obj[s.name].description = s.description;
        }
        
        if(angular.isDefined(s.site)){
          // TODO build site tosca
        }
        if(angular.isDefined(s.default_image)){
          // TODO build image tosca
        }
        if(angular.isDefined(s.networks) && s.networks.length > 0){
          // TODO build networks tosca
        }
        console.log(s);

        return obj;
      }, {});
      angular.extend(toscaSpec.topology_template.node_templates, slices);
      d.resolve(toscaSpec);
      return d.promise;
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

