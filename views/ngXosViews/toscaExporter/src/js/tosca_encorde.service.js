(function () {
  'use strict';

  /**
   * @ngdoc service
   * @name xos.toscaExporter.ToscaEncoder
   **/

  angular.module('xos.toscaExporter')
  .service('ToscaEncoder', function($q, _, Services, Tenants){

    const serviceTypes = {
      fabric: 'tosca.nodes.FabricService',
      onos: 'tosca.nodes.ONOSService',
      vCPE: 'tosca.nodes.VSGService',
      vOLT: 'tosca.nodes.VOLTService',
      vROUTER: 'tosca.nodes.VRouterService',
      VTN: 'tosca.nodes.VTNService',
      vTR: 'tosca.nodes.Service'
    };

    const toscaSpec = {
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
     * @name xos.toscaExporter.ToscaEncoder#$toYml
     * @methodOf xos.toscaExporter.ToscaEncoder
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
      console.log(file);
    };

    this.formatServiceProperties = service => {
      const d = $q.defer();
      const props = {
        view_url: service.view_url,
        icon_url: service.icon_url,
        kind: service.kind,
        public_key: service.public_key || null,
        private_key_fn: service.private_key_fn || null
      };
      d.resolve(props);
      return d.promise;
    };

    this.getServiceRequirements = service => {
      const d = $q.defer();

      Tenants.query({subscriber_service: service.id}).$promise
      .then(tenants => {
        const services = [];
        _.forEach(tenants, t => {
          console.log(`Provider: ${t.provider_service}`);
          services.push(Services.get({id: t.provider_service}).$promise);
        });

        return $q.all(services)
      })
      .then((deps) => {
        // NOTE this is not too readable
        // Get the provider service and create an array of unique names
        let requirements = _.uniq(_.reduce(deps, (list, d) => list.concat(d.name), []));

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
        d.resolve(requirements);
      });

      return d.promise;
    };

    this.serviceToTosca = service => {
      //clean
      toscaSpec.topology_template.node_templates = {};

      const d = $q.defer();
      const serviceName = `service#${service.name}`;

      // create the structure to hold the service
      toscaSpec.topology_template.node_templates[serviceName] = {};
      toscaSpec.topology_template.node_templates[serviceName].type = serviceTypes[service.kind] || 'tosca.nodes.Service';

      // build service properties
      this.formatServiceProperties(service)
      .then(props => {
        toscaSpec.topology_template.node_templates[serviceName].properties = props;
        return this.getServiceRequirements(service);
      })
      .then((deps) => {
        if(angular.isDefined(deps)){
          toscaSpec.topology_template.node_templates[serviceName].requirements = deps;
        }
        this.export();
        console.log(toscaSpec);
        d.resolve(this.toYml(toscaSpec));
      });
      return d.promise;

    }

  });

}());