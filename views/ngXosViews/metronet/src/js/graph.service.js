(function () {
  'use strict';

  // this is temporary (COs should be modeled in the BE)
  const unisToCo = (unis) => {
    let tmp = _.groupBy(unis, 'latlng');
    return _.reduce(tmp, (cos, unis) => {
      let [lng, lat] = JSON.parse(unis[0].latlng);
      const coId = `co-${cos.length}`;
      cos.push({
        id: coId,
        latlng: {lat: lat, lng: lng},
        type: 'co',
        unis: unis.map(u => {
          let [lng, lat] = JSON.parse(u.latlng);
          u.latlng = {lat: lat, lng: lng};
          u.type = 'uni';
          u.co = coId;
          return u;
        }),
        name: unis[0].name,
        location: unis[0].location,
        fixed: true // D3 requires it
      });
      return cos;
    }, [])
  };

  angular.module('xos.metronet')
  .service('MetronetGraph', function($q, _, Uni, ELine, ETree, ELan){

    // store real connections (links depend on the grouping in COs)
    // if a CO is compact links point to it,
    // otherwise to the correct UNI
    this._connections = {
      elines: [],
      etrees: [],
      elans: []
    };

    // store graph nodes and links
    this._nodes = [];
    this._links = [];

    this.connections = () => this._connections;
    this.nodes = () => this._nodes;
    this.links = () => this._links;

    this.setLinks = (links) => {
      this._links = links;
    }

    this.loadData = () => {
      const d = $q.defer();

      $q.all([
        Uni.query().$promise,
        ELine.query().$promise,
        ETree.query().$promise,
        ELan.query().$promise
      ])
      .then(res => {
        let [unis, elines, etrees, elans] = res;
        
        this._nodes = unisToCo(unis);
        this._connections.elines = elines;
        this._connections.etrees = etrees;
        this._connections.elans = elans;
        this._links = this.buildLinks(this._connections, this._nodes);

        d.resolve();
      })
      .catch(d.reject);

      return d.promise;
    };

    this.buildLinks = (connections, nodes) => {
      const l1 = connections.elines.map(eline => {
        return this.buildElineLink(eline, nodes);
      });
      return l1;
    };

    this.buildElineLink = (eline, nodes) => {
      return {
        source: this.findUniNode(eline.uni1, nodes),
        target: this.findUniNode(eline.uni2, nodes),
        connection: eline
      };
    };

    this.findUniNode = (uni, nodes) => {
      // if we have the node it means that the CO is expanded
      let node = _.find(nodes, n => {
        return uni.id === n.id
      });
      console.log(node);

      // else look for the CO
      if(!node){
        node = _.find(nodes, n => {
          return _.findIndex(n.unis, u => {
            return uni.id === u.id;
          }) > -1;
        });
      }
      return node;
    };

    // when a CO is expanded,
    // the link should be updated to point toward the UNI
    this.updateLinksTarget = (links, nodes) => {
      // NOTE as this will work only for Eline
      // TODO find a way to generalize it
      return links.map(l => {
        if(!l.connection){
          // it is between CO and UNI,
          // should be ok
          return l;
        }
        if(l.target.type === 'co'){
          l.target = this.findUniNode(l.connection.uni2, nodes);
        }
        if(l.source.type === 'co'){
          l.source = this.findUniNode(l.connection.uni1, nodes);
        }
        return l;
      });
    };

    this.togglePorts = (node) => {
      if(!node.unis){
        console.log('No ports!');
        return;
      }
      if(node.expanded){
        console.log('remove');
        // TODO remove ports from nodes and rebuild links
        _.forEach(node.unis, u => {
          _.remove(this._nodes, {id: u.id});
        });
        // TODO remove links that point to this CO
        // reset links from ports to another CO
        this._links = this.updateLinksTarget(this._links, this._nodes);
      }
      else{

        // set unis in the same starting position of the CO
        node.unis = node.unis.map(n => {
          n.x = node.x;
          n.y = node.y;
          return n;
        });
        this._nodes = this._nodes.concat(node.unis);
        _.forEach(node.unis, u => {
          this._links.push({
            source: node,
            target: this.findUniNode(u, this._nodes),
            connection: null
          });
        });
        this._links = this.updateLinksTarget(this._links, this._nodes);
      }
      node.expanded = !node.expanded;
    }
  });
})();