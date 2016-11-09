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
  .service('MetronetGraph', function($q, $timeout, _, Uni, ELine, ETree, ELan, MetronetState){

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

    // create a virtual switch to represent E-Lans
    this.createSw = (elan) => {
      return {
        id: `sw-${elan.id}`,
        name: `${elan.sid} vSwitch`,
        type: 'sw',
        // x: 200,
        // y: 200
      }
    };

    this.buildLinks = (connections, nodes) => {
      const l1 = connections.elines.map(eline => {
        return this.buildElineLink(eline, nodes);
      });
      const l2 = connections.etrees.map(etree => {
        return this.buildEtreeLink(etree, nodes);
      });
      const l3 = connections.elans.map(elan => {
        // for each elan create a new node that represent a virtual switch
        const sw = this.createSw(elan);
        this._nodes.push(sw);
        return this.buildElanLinks(elan, nodes, sw);
      });
      
      return _.flatten(l1.concat(l2).concat(l3));
    };

    this.buildElineLink = (eline, nodes) => {
      return {
        source: this.findUniNode(eline.uni1, nodes),
        target: this.findUniNode(eline.uni2, nodes),
        connection: eline
      };
    };

    this.buildEtreeLink = (etree, nodes) => {
      return etree.eps.map(u => {
        return {
          source: this.findUniNode(etree.root, nodes),
          target: this.findUniNode(u, nodes),
          connection: etree,
          targetUni: u // this is an hack to make it work, find a better desing
        };
      });
    };

    this.buildElanLinks = (elan, nodes, sw) => {
      // we use a virtual switch to represent elans
      elan.type = 'elan';
      return elan.eps.map(u => {
        return {
          source: sw,
          target: this.findUniNode(u, nodes),
          connection: elan,
          targetUni: u // this is an hack to make it work, find a better desing
        };
      })
    };

    this.findUniNode = (uni, nodes) => {
      // if we have the node it means that the CO is expanded
      let node = _.find(nodes, n => {
        return uni.id === n.id
      });

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

    this.getCoByUni = uni => {
      return _.find(this._nodes, n => n.id === uni.co);
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
        if(l.connection.type === 'direct'){
          l.target = this.findUniNode(l.connection.uni2, nodes);
          l.source = this.findUniNode(l.connection.uni1, nodes);
        }
        else if(l.connection.type === 'ethernet'){
          l.target = this.findUniNode(l.targetUni, nodes);
          l.source = this.findUniNode(l.connection.root, nodes);
        }
        else if (l.connection.type === 'elan'){
          l.target = this.findUniNode(l.targetUni, nodes);
        }
        return l;
      });
    };

    // remove links pointing to a collapsed co
    this.removeCoLinks = (co, links) => {
      return _.filter(links, l => {
        if(l.source === co){
          return false;
        }
        if(l.target === co){
          return false;
        }
        return true;
      });
    };

    this.togglePorts = (node) => {
      if(!node.unis){
        console.log('No ports!');
        return;
      }
      if(node.expanded){
        // remove ports from nodes
        _.forEach(node.unis, u => {
          u.selected = false;
          _.remove(this._nodes, n => {
            return n.id === u.id;
          });
        });

        // remove links that point to this CO
        this._links = this.removeCoLinks(node, this._links);

        // reset links from ports to another CO
        $timeout(() => {
          this._links = this.updateLinksTarget(this._links, this._nodes);
        }, 500);
      }
      else{

        // set unis in the same starting position of the CO
        node.unis = node.unis.map(n => {
          n.x = node.x;
          n.y = node.y;
          if(!n.fixed){
            n.px = node.x;
            n.py = node.y;
          }
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
    };

    this.toggleAllPorts = () => {

      if(MetronetState.showAllPorts){
        this._nodes
          .filter(n => n.type === 'co')
          .forEach(n => {
            n.expanded = false;
            this.togglePorts(n);
          });
      }
      else {
        this._nodes
          .filter(n => n.type === 'co')
          .forEach(n => {
            n.expanded = true;
            this.togglePorts(n);
          });
      }
    };

    this.toggleEtree = () => {
      if(MetronetState.showEtrees){
        this._links = this._links.filter(l => {
          if(!l.connection){
            // it is a local link (CO to UNI)
            return true;
          }
          return l.connection.type !== 'ethernet';
        });
      }
      else{
        const etreeLinks = this._connections.etrees.map(etree => {
          return this.buildEtreeLink(etree, this._nodes);
        });
        this._links = this._links.concat(_.flatten(etreeLinks));
      }
    };

    this.toggleEline = () => {
      if(MetronetState.showElines){
        this._links = this._links.filter(l => {
          if(!l.connection){
            // it is a local link (CO to UNI)
            return true;
          }
          return l.connection.type !== 'direct';
        });
      }
      else{
        const elineLinks = this._connections.elines.map(eline => {
          return this.buildElineLink(eline, this._nodes);
        });
        this._links = this._links.concat(_.flatten(elineLinks));
      }
    };

    this.toggleElan = () => {
      if(MetronetState.showElans){

        // remove sw nodes
        this._nodes = this._nodes.filter(n => n.type !== 'sw');

        this._links = this._links.filter(l => {
          if(!l.connection){
            // it is a local link (CO to UNI)
            return true;
          }
          return l.connection.type !== 'elan';
        });
      }
      else{
        const elanLinks = this._connections.elans.map(elan => {
          const sw = this.createSw(elan);
          this._nodes.push(sw);
          return this.buildElanLinks(elan, this._nodes, sw);
        });
        this._links = this._links.concat(_.flatten(elanLinks));
      }
    };
  });
})();