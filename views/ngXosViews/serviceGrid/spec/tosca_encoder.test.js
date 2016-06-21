(function () {
  'use strict';
  describe('The Tosca Encoder Service', () => {

    var service, httpBackend, rootScope, ArchiveCreatorSpy, toscaBase;

    const serviceData = {
      id: 1,
      name: 'vsg',
      kind: 'vCPE'
    };

    const toscaBaseDefault = {
      topology_template: {
        node_templates: {}
      }
    };

    beforeEach(module('xos.serviceGrid'));
    beforeEach(module('templates'));

    beforeEach(inject(function($httpBackend, $rootScope, ToscaEncoder, ArchiveCreator){

      httpBackend = $httpBackend;
      rootScope = $rootScope;
      toscaBase = angular.copy(toscaBaseDefault);
      service = ToscaEncoder;
      ArchiveCreatorSpy = ArchiveCreator;
      spyOn(ArchiveCreatorSpy, 'createArchive');
      spyOn(ArchiveCreatorSpy, 'addFile');
    }));

    describe('the formatServiceProperties method', () => {
      it('should return only the existing properties', (done) => {
        service.formatServiceProperties({name: 'test', kind: 'vCPE'}, toscaBase)
        .then(res => {
          expect(res).toEqual({
            topology_template:{
              node_templates: {
                'service#test': {
                  type: 'tosca.nodes.VSGService',
                  properties: {kind: 'vCPE'}
                }
              }
            }
          });
          done();
        });
        rootScope.$apply();
      });

      it('should return all properties', (done) => {
        service.formatServiceProperties({
          name: 'test',
          kind: 'vCPE',
          view_url: 'view_url',
          icon_url: 'icon_url',
          private_key_fn: 'private_key_fn'
        }, toscaBase)
        .then(res => {
          expect(res).toEqual({
            topology_template:{
              node_templates: {
                'service#test': {
                  type: 'tosca.nodes.VSGService',
                  properties: {
                    kind: 'vCPE',
                    view_url: 'view_url',
                    icon_url: 'icon_url',
                    private_key_fn: 'private_key_fn'
                  }
                }
              }
            }
          });
          done();
        });
        rootScope.$apply();
      });

      describe('when a public key is provided', () => {
        it('should add public_key and artifacts properties', (done) => {

          let expected = {
            topology_template:{
              node_templates: {
                'service#test': {
                  type: 'tosca.nodes.VSGService',
                  properties: {
                    kind: 'vCPE',
                    public_key: '{ get_artifact: [ SELF, pubkey, LOCAL_FILE] }'
                  },
                  artifacts: {
                    pubkey: './test_rsa.pub'
                  }
                }
              }
            }
          };

          service.formatServiceProperties({
            kind: 'vCPE',
            public_key: 'pkey',
            name: 'test'
          }, toscaBase)
          .then(res => {
            expect(res).toEqual(expected);
            done();
          });
          rootScope.$apply();
        });

        it('should add public_key file to the archive', (done) => {
          service.formatServiceProperties({
              kind: 'vCPE',
              public_key: 'pkey',
              name: 'test'
            }, toscaBase)
            .then(res => {
              expect(ArchiveCreatorSpy.addFile).toHaveBeenCalledWith('test_rsa.pub', 'pkey');
              done();
            });
          rootScope.$apply();
        });
      });
    });

    describe('the getServiceRequirements method', () => {
      let TenantSpy, ServiceSpy, tenantQueryPromise, serviceQueryPromise;
      beforeEach(inject(function(Tenants, Services, $q){

        tenantQueryPromise= $q.defer();

        TenantSpy = Tenants;
        spyOn(TenantSpy, 'query').and.callFake(function(){
          return {$promise: tenantQueryPromise.promise};
        });

        ServiceSpy = Services;
        spyOn(ServiceSpy, 'get').and.callFake(function(p){
          let d = $q.defer();
          d.resolve({name: `deps_${p.id}`});
          return {$promise: d.promise};
        });
      }));

      it('should call the tenants service with correct params', () => {
        service.getServiceRequirements({id: 1});
        expect(TenantSpy.query).toHaveBeenCalledWith({subscriber_service: 1});
      });

      it('should not add requirements if the current service has no dependency', (done) => {
        service.getServiceRequirements({id: 1}, {})
        .then(res => {
          expect(res).toEqual({});
          done();
        });
        tenantQueryPromise.resolve();
        rootScope.$apply();
      });

      it('should return a list of required service', () => {
        service.getServiceRequirements({id: 1, name: 'test'}, {topology_template: {node_templates: {'service#test': {}}}})
        .then(res => {
          console.log(res);
          expect(res.topology_template.node_templates['service#test'].requirements).toEqual([
            {
              deps_3_tenant: {
                node: 'service#deps_3',
                relationship: 'tosca.relationships.TenantOfService'
              }
            },
            {
              deps_4_tenant: {
                node: 'service#deps_4',
                relationship: 'tosca.relationships.TenantOfService'
              }
            }
          ]);
        });
        tenantQueryPromise.resolve([
          {
            subscriber_service: 1,
            provider_service: 3
          },
          {
            subscriber_service: 1,
            provider_service: 4
          }
        ]);
        rootScope.$apply();
      });

      it('should return a list of unique required service', () => {
        service.getServiceRequirements({id: 1, name: 'test'}, {topology_template: {node_templates: {'service#test': {}}}})
          .then(res => {
            expect(res.topology_template.node_templates['service#test'].requirements).toEqual([
              {
                deps_3_tenant: {
                  node: 'service#deps_3',
                  relationship: 'tosca.relationships.TenantOfService'
                }
              }
            ]);
          });
        tenantQueryPromise.resolve([
          {
            subscriber_service: 1,
            provider_service: 3
          },
          {
            subscriber_service: 1,
            provider_service: 3
          }
        ]);
        rootScope.$apply();
      });
    });

    describe('the serviceToTosca method', () => {

      const fakePropertiesDefault = {
        tosca_definitions_version: 'tosca_simple_yaml_1_0',
        description: 'Just enough Tosca to get the vSG slice running on the CORD POD',
        imports: [
          'custom_types/xos.yaml'
        ],
        topology_template:{
          node_templates: {
            'service#vsg': {
              type: 'tosca.nodes.VSGService',
              properties: {
                view_url: 'viewUrl',
                icon_url: 'iconUrl',
                kind: 'vCPE'
              }
            }
          }
        }
      };

      const fakeRequirements = {
        tosca_definitions_version: 'tosca_simple_yaml_1_0',
        description: 'Just enough Tosca to get the vSG slice running on the CORD POD',
        imports: [
          'custom_types/xos.yaml'
        ],
        topology_template:{
          node_templates: {
            'service#vsg': {
              type: 'tosca.nodes.VSGService',
              properties: {
                view_url: 'viewUrl',
                icon_url: 'iconUrl',
                kind: 'vCPE'
              },
              requirements: [
                {
                  node: 'service#vrouter',
                  relationship: 'tosca.relationships.TenantOfService'
                },
                {
                  node: 'service#volt',
                  relationship: 'tosca.relationships.TenantOfService'
                }
              ]
            }
          }
        }
      };

      const expectedWithoutRequirements = `tosca_definitions_version: tosca_simple_yaml_1_0
description: Just enough Tosca to get the vSG slice running on the CORD POD
imports:
  - custom_types/xos.yaml
topology_template:
  node_templates:
    'service#vsg':
      type: tosca.nodes.VSGService
      properties:
        view_url: viewUrl
        icon_url: iconUrl
        kind: vCPE
`;

      const expectedWithRequirements = `tosca_definitions_version: tosca_simple_yaml_1_0
description: Just enough Tosca to get the vSG slice running on the CORD POD
imports:
  - custom_types/xos.yaml
topology_template:
  node_templates:
    'service#vsg':
      type: tosca.nodes.VSGService
      properties:
        view_url: viewUrl
        icon_url: iconUrl
        kind: vCPE
      requirements:
        - node: 'service#vrouter'
          relationship: tosca.relationships.TenantOfService
        - node: 'service#volt'
          relationship: tosca.relationships.TenantOfService
`;

      const expectedWithSlices = `tosca_definitions_version: tosca_simple_yaml_1_0
description: Just enough Tosca to get the vSG slice running on the CORD POD
imports:
  - custom_types/xos.yaml
topology_template:
  node_templates:
    'service#vsg':
      type: tosca.nodes.VSGService
      properties:
        view_url: viewUrl
        icon_url: iconUrl
        kind: vCPE
    service_slice:
      description: A service slice
      type: tosca.nodes.Slice
      properties:
        network: noauto
`;

      let formatPromise, requirementPromise, slicesPromise, fakeProperties;

      beforeEach(inject(($q) => {

        // clone the base property for mock
        fakeProperties = angular.copy(fakePropertiesDefault);

        // create the promises
        // this will be resolved in the single IT block,
        // to allow different resolutions
        formatPromise = $q.defer();
        requirementPromise = $q.defer();
        slicesPromise = $q.defer();

        // mock functions and return promises
        spyOn(service, 'formatServiceProperties').and.callFake(function(){
          return formatPromise.promise;
        });
        spyOn(service, 'getServiceRequirements').and.callFake(function(){
          return requirementPromise.promise;
        });
        spyOn(service, 'getServiceSlices').and.callFake(function(){
          return slicesPromise.promise;
        });
      }));

      it('should create a new archive', () => {
        service.serviceToTosca(serviceData);
        expect(ArchiveCreatorSpy.createArchive).toHaveBeenCalled();
      });

      it('should add the service file to the archive', (done) => {
        service.serviceToTosca(serviceData)
        .then(() => {
          expect(ArchiveCreatorSpy.addFile).toHaveBeenCalledWith('vsg_service.yaml', expectedWithoutRequirements);
          done();
        });
        formatPromise.resolve(fakeProperties);
        requirementPromise.resolve(fakeProperties);
        slicesPromise.resolve(fakeProperties);
        rootScope.$apply();
      });

      it('should create a tosca spec with no requirements', (done) => {
        service.serviceToTosca(serviceData)
          .then(res => {
            expect(res).toEqual(expectedWithoutRequirements);
            done();
          });
        formatPromise.resolve(fakeProperties);
        requirementPromise.resolve(fakeProperties);
        slicesPromise.resolve(fakeProperties);
        rootScope.$apply();
      });

      it('should create a tosca spec with requirements', (done) => {
        service.serviceToTosca(serviceData)
          .then(res => {
            expect(res).toEqual(expectedWithRequirements);
            done();
          });
        formatPromise.resolve(fakeProperties);
        requirementPromise.resolve(fakeRequirements);
        slicesPromise.resolve(fakeProperties);
        rootScope.$apply();
      });

      it('should create a tosca spec with additional slices', (done) => {

        // this is dirty, we are changing an object and shouldn't be done in tests
        angular.extend(
          fakeProperties.topology_template.node_templates, {service_slice: {
            description: 'A service slice',
            type: 'tosca.nodes.Slice',
            properties: {
              network: 'noauto'
            }
          }});

        service.serviceToTosca(serviceData)
          .then(res => {
            expect(res).toEqual(expectedWithSlices);
            done();
          });
        formatPromise.resolve(fakeProperties);
        requirementPromise.resolve(fakeProperties);
        slicesPromise.resolve(fakeProperties);
        rootScope.$apply();
      });
    });
  });
}());