/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 6/22/16.
 */

(function () {
  'use strict';

  describe('The Slices Encoder service', () => {

    let service, toscaBase, sliceQueryPromise, SliceSpy, rootScope;

    const toscaBaseDefault = {
      topology_template: {
        node_templates: {}
      }
    };

    const slicesArray = [
      {
        name: 'Slice1',
        description: 'Description1',
        network: 'noauto'
      },
      {
        name: 'Slice2',
        description: 'Description2',
        network: 'noauto'
      }
    ];

    const expected = {
      topology_template: {
        node_templates: {
          Slice1: {
            description: 'Description1',
            type: 'tosca.nodes.Slice',
            properties: {
              network: 'noauto'
            }
          },
          Slice2: {
            description: 'Description2',
            type: 'tosca.nodes.Slice',
            properties: {
              network: 'noauto'
            }
          }
        }
      }
    };

    beforeEach(module('xos.serviceGrid'));
    beforeEach(module('templates'));

    beforeEach(inject((SlicesEncoder, Slices, $q, $rootScope) => {
      toscaBase = angular.copy(toscaBaseDefault);
      service = SlicesEncoder;
      rootScope = $rootScope;

      sliceQueryPromise= $q.defer();
      SliceSpy = Slices;
      spyOn(SliceSpy, 'query').and.callFake(function(){
        return {$promise: sliceQueryPromise.promise};
      });
    }));
    
    describe('given a Slices array ', () => {
      it('should return the correct JSON structure', () => {
        let res = service.buildTosca(slicesArray, toscaBase);

        expect(res).toEqual(expected);
      });
    });

    describe('given a service', () => {
      it('should return the JSON structure for all related slices', () => {
        service.getServiceSlices({id : 1}, toscaBase)
        .then(res => {
          expect(res).toEqual(expected);
        });
        sliceQueryPromise.resolve(slicesArray);
        rootScope.$apply();
      });
    });
  });
})();

