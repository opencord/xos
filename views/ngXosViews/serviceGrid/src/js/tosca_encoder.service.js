(function () {
  'use strict';

  /**
   * @ngdoc service
   * @name xos.toscaExporter.serviceGrid
   **/

  angular.module('xos.serviceGrid')
  .service('ToscaEncoder', function($q, _, ArchiveCreator, Services, Tenants, Slices){

    const serviceTypes = {
      fabric: 'tosca.nodes.FabricService',
      onos: 'tosca.nodes.ONOSService',
      vCPE: 'tosca.nodes.VSGService',
      vOLT: 'tosca.nodes.VOLTService',
      vROUTER: 'tosca.nodes.VRouterService',
      VTN: 'tosca.nodes.VTNService',
      vTR: 'tosca.nodes.Service'
    };

    let toscaSpec = {
      tosca_definitions_version: 'tosca_simple_yaml_1_0',
      description: 'Just enough Tosca to get the vSG slice running on the CORD POD',
      imports: [
        'custom_types/xos.yaml'
      ],
      topology_template:{
        node_templates: {}
      }
    };

    /**
     * @ngdoc method
     * @name xos.serviceGrid.ToscaEncoder#$toYml
     * @methodOf xos.serviceGrid.ToscaEncoder
     * @description
     * Convert a Json data structure to Yaml, use https://github.com/nodeca/js-yaml
     * @param {Object} item A Json object to be converted
     * @returns {string} The Yaml representation of the Json input
     **/

    this.toYml = (item) => {
      return jsyaml.dump(item);
    };

    this.export = () => {
      const file = this.toYml(toscaSpec);
      return file;
      //ArchiveCreator.download(service.name);
    };

    this.formatServiceProperties = (service, toscaSpec) => {
      const d = $q.defer();
      const serviceName = `service#${service.name}`;
      // create the structure to hold the service
      toscaSpec.topology_template.node_templates[serviceName] = {};
      toscaSpec.topology_template.node_templates[serviceName].type = serviceTypes[service.kind] || 'tosca.nodes.Service';

      const res = {
        properties: {
          kind: service.kind
        }
      };

      if(angular.isDefined(service.view_url)){
        res.properties.view_url = service.view_url;
      }

      if(angular.isDefined(service.icon_url)){
        res.properties.icon_url = service.icon_url;
      }

      if(angular.isDefined(service.private_key_fn)){
        res.properties.private_key_fn = service.private_key_fn;
      }

      if(angular.isDefined(service.public_key)){
        ArchiveCreator.addFile(`${service.name}_rsa.pub`, service.public_key);
        res.properties.public_key = '{ get_artifact: [ SELF, pubkey, LOCAL_FILE] }'
        res['artifacts'] = {
          pubkey: `./${service.name}_rsa.pub`
        };
        toscaSpec.topology_template.node_templates[serviceName].artifacts = res.artifacts;
      }

      toscaSpec.topology_template.node_templates[serviceName].properties = res.properties;
      d.resolve(toscaSpec);
      return d.promise;
    };

    this.getServiceRequirements = (service, toscaSpec) => {
      const d = $q.defer();

      Tenants.query({subscriber_service: service.id}).$promise
      .then(tenants => {
        const services = [];
        // avoid multiple request for the same service
        tenants = _.uniqBy(tenants, 'provider_service');

        _.forEach(tenants, t => {
          services.push(Services.get({id: t.provider_service}).$promise);
        });

        return $q.all(services)
      })
      .then((deps) => {
        // Get the provider service and create an array of unique names
        let requirements = _.reduce(deps, (list, d) => list.concat(d.name), []);

        // create a object for requirements, later will parsed in Yaml
        requirements = _.reduce(requirements, (list, r) => {
          let name = `${r}_tenant`;
          let obj = {};
          obj[name] = {
            node: `service#${r}`,
            relationship: 'tosca.relationships.TenantOfService'
          };
          return list.concat(obj);
        }, []);

        if(requirements.length > 0){
          const serviceName = `service#${service.name}`;
          toscaSpec.topology_template.node_templates[serviceName].requirements = requirements;
        }

        d.resolve(toscaSpec);
      });

      return d.promise;
    };

    this.getServiceSlices = (service, toscaSpec) => {
      const d = $q.defer();
      Slices.query({service: service.id}).$promise
      .then(slices => {
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
        d.resolve(toscaSpec);
      });

      return d.promise;
    };

    this.serviceToTosca = service => {

      ArchiveCreator.createArchive();
      //clean
      toscaSpec.topology_template.node_templates = {};

      const d = $q.defer();

      // build service properties
      this.formatServiceProperties(service, toscaSpec)
      .then(spec => {
        return this.getServiceSlices(service, spec);
      })
      // add required slices (and it will all the slice requirements)
      .then((spec) => {
        return this.getServiceRequirements(service, spec);
      })
      // add required services (provider services)
      .then((spec) => {
        ArchiveCreator.addFile(`${service.name}_service.yaml`, this.toYml(spec));

        d.resolve(this.toYml(spec));
      })
      .catch(e => {
        d.reject(e);
      });
      return d.promise;

    }

  })
  .service('ArchiveCreator', function(){
    this.createArchive = () => {
      this.archive = new JSZip();
    };

    this.addFile = (fileName, content) => {
      this.archive.file(fileName, content);
    };

    this.download = (name) => {
      console.log(this.archive);
      this.archive.generateAsync({type: 'blob'})
      .then(function(content) {
        saveAs(content, `${name}.zip`);
      })
      .catch(e => {
        console.log(e);
      });
    };
  });

}());