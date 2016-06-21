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
  .service('SlicesEncoder', function($q, _, Slices, SiteEncoder, ImageEncoder, NetworkEncoder){

    this.buildTosca = (slices, toscaSpec) => {

      // store here the promise that will build the dependency structure
      let dependencyArr = [];

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
          dependencyArr.push(SiteEncoder.buildTosca(s.site, toscaSpec));
        }
        if(angular.isDefined(s.default_image)){
          dependencyArr.push(ImageEncoder.buildTosca(s.default_image, toscaSpec));
        }
        if(angular.isDefined(s.networks) && s.networks.length > 0){
          dependencyArr.push(NetworkEncoder.getSliceNetworks(s, toscaSpec));
        }

        return obj;
      }, {});


      // TODO add requirement to slice
      angular.extend(toscaSpec.topology_template.node_templates, slices);

      // if we have dependency wait for them
      if(dependencyArr.length > 0){
        $q.all(dependencyArr)
        .then(deps => {
          _.forEach(deps, d => {
            angular.extend(toscaSpec, d);
          });
          d.resolve(toscaSpec);
        })
        .catch(e => {
          throw new Error(e);
        });
      }
      //else resolve directly
      else {
        d.resolve(toscaSpec);
      }

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

