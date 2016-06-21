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

  // TODO write tests
  angular.module('xos.serviceGrid')
    .service('NetworkEncoder', function($q, Networks, NetworkTemplateEncoder){

      this.buildTosca = (networks, toscaSpec) => {

        // store here the promise that will build the dependency structure
        let dependency = {};

        const d = $q.defer();

        try {
          networks = _.reduce(networks, (obj, n) => {
            obj[`network#${n.name}`] = {
              type: 'tosca.nodes.Network.XOS',
              requirements: []
            };

            // for each network slice, add requirement
            if(angular.isDefined(n.slices)) {
              _.forEach(n.slices, s => {
                let owner = {
                  owner: {
                    node: s.name,
                    relationship: 'tosca.relationships.MemberOfSlice'
                  }
                };

                let conn =  {
                  connection: {
                    node: s.name,
                    relationship: 'tosca.relationships.ConnectsToSlice'
                  }
                };
                obj[`network#${n.name}`].requirements.push(owner, conn);
              });

              if(angular.isDefined(n.template)){
                dependency.template = NetworkTemplateEncoder.buildTosca(n.template, toscaSpec);
              }
            }

            return obj;

          }, {});

          // TODO manage requirements [template]


          // if we have dependency wait for them
          if(Object.keys(dependency).length > 0){
            $q.all(dependency)
            .then(deps => {
              _.forEach(deps, d => {
                angular.extend(toscaSpec, d);
              });

              // HOW TO RETRIEVE NETWORK NAME???????
              //if(deps.template){
              //  networks[`network#${n.name}`].requirements.push()
              //}
              angular.extend(toscaSpec.topology_template.node_templates, networks);
              d.resolve(toscaSpec);
            })
            .catch(e => {
              throw new Error(e);
            });
          }
          //else resolve directly
          else {
            angular.extend(toscaSpec.topology_template.node_templates, networks);
            d.resolve(toscaSpec);
          }
        }
        catch(e){
          d.reject(e);
        }

        return d.promise;
      };

      this.getSliceNetworks = (slice, toscaSpec) => {
        const d = $q.defer();
        Networks.query({owner: slice.id}).$promise
        .then((networks) => {
          // check that all the network this slice own are listed in the slice
          // does this make sense?
          networks = _.filter(networks, n => {
            return slice.networks.indexOf(n.id) !== -1;
          });

          // denormalize slice inside network
          networks = networks.map(n => {
            let idx = n.slices.indexOf(slice.id);
            n.slices[idx] = slice;
            return n;
          });

          this.buildTosca(networks, toscaSpec)
          .then(d.resolve)
          .catch(d.reject);

        });

        return d.promise;
      }
    });
})();

