(function () {
  'use strict';
  describe('The Tosca Encoder Service', () => {

    var service, httpBackend, rootScope, ArchiveCreatorSpy;

    const serviceData = {
      id: 1,
      name: 'vsg',
      kind: 'vCPE'
    };

    beforeEach(module('xos.serviceGrid'));
    beforeEach(module('templates'));

    beforeEach(inject(function($httpBackend, $rootScope, ToscaEncoder, ArchiveCreator){

      httpBackend = $httpBackend;
      rootScope = $rootScope;
      // Setting up mock request
      //$httpBackend.expectGET('/api/core/users/?no_hyperlinks=1').respond([
      //  {
      //    email: 'teo@onlab.us',
      //    firstname: 'Matteo',
      //    lastname: 'Scandolo'
      //  }
      //]);

      service = ToscaEncoder;
      ArchiveCreatorSpy = ArchiveCreator;
      spyOn(ArchiveCreatorSpy, 'createArchive');
      spyOn(ArchiveCreatorSpy, 'addFile');
    }));

    describe('the formatServiceProperties method', () => {
      it('should return only the existing properties', (done) => {
        service.formatServiceProperties({kind: 'vCPE'})
        .then(res => {
          expect(res).toEqual({properties: {kind: 'vCPE'}});
          done();
        });
        rootScope.$apply();
      });

      it('should return all properties', (done) => {
        service.formatServiceProperties({
          kind: 'vCPE',
          view_url: 'view_url',
          icon_url: 'icon_url',
          private_key_fn: 'private_key_fn'
        })
        .then(res => {
          expect(res).toEqual({
            properties: {
              kind: 'vCPE',
              view_url: 'view_url',
              icon_url: 'icon_url',
              private_key_fn: 'private_key_fn'
            }
          });
          done();
        });
        rootScope.$apply();
      });

      describe('when a public key is provided', () => {
        it('should add public_key and artifacts properties', (done) => {
          service.formatServiceProperties({
            kind: 'vCPE',
            public_key: 'pkey',
            name: 'testName'
          })
          .then(res => {
            expect(res).toEqual({
              properties: {
                kind: 'vCPE',
                public_key: '{ get_artifact: [ SELF, pubkey, LOCAL_FILE] }'
              },
              artifacts: {
                pubkey: './testName_rsa.pub'
              }
            })
            done();
          });
          rootScope.$apply();
        });

        it('should add public_key file to the archive', (done) => {
          service.formatServiceProperties({
              kind: 'vCPE',
              public_key: 'pkey',
              name: 'testName'
            })
            .then(res => {
              expect(ArchiveCreatorSpy.addFile).toHaveBeenCalledWith('testName_rsa.pub', 'pkey');
              done();
            });
          rootScope.$apply();
        });
      });
    });

    describe('the serviceToTosca method', () => {

      const fakeProperties = {
        properties: {
          view_url: 'viewUrl',
          icon_url: 'iconUrl',
          kind: 'vCPE'
        }
      };

      const fakeRequirements = [
        {
          node: 'service#vrouter',
          relationship: 'tosca.relationships.TenantOfService'
        },
        {
          node: 'service#volt',
          relationship: 'tosca.relationships.TenantOfService'
        }
      ];

      const expectedWithoutRequirements = `tosca_definitions_version: tosca_simple_yaml_1_0
description: Just enough Tosca to get the vSG slice running on the CORD POD
imports:
  - custom_types/xos.yaml
topology_template:
  node_templates:
    'service#vsg':
      type: tosca.nodes.VSGService
      properties:
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

      let formatPromise, requirementPromise;

      beforeEach(inject(($q) => {
        // create the promises
        // this will be resolved in the single IT block,
        // to allow different resolutions
        formatPromise = $q.defer();
        requirementPromise = $q.defer();

        // mock functions and return promises
        spyOn(service, 'formatServiceProperties').and.callFake(function(){
          return formatPromise.promise;
        });
        spyOn(service, 'getServiceRequirements').and.callFake(function(){
          return requirementPromise.promise;
        })
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
        requirementPromise.resolve();
        rootScope.$apply();
      });

      it('should create a tosca spec with no requirements', (done) => {
        service.serviceToTosca(serviceData)
          .then(res => {
            expect(res).toEqual(expectedWithoutRequirements);
            done();
          });
        formatPromise.resolve(fakeProperties);
        requirementPromise.resolve();
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
        rootScope.$apply();
      });
    });
  });
}());