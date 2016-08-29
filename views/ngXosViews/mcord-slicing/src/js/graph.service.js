(function () {
  'use strict';

  angular.module('xos.mcord-slicing')
  .service('SliceGraph', function(_, NodePositioner){
    const g = new graphlib.Graph();

    /**
    * @ngdoc method
    * @name xos.mcord-slicing.SliceGraph#buildGraph
    * @methodOf xos.mcord-slicing.SliceGraph
    * @description
    * buildGraph
    * @param {object} data An object in the for of {nodes: [], links: []} describing the graph
    * @returns {null}
    **/
    this.buildGraph = (data) => {
      _.forEach(data.nodes, n => g.setNode(n.id, n));
      _.forEach(data.links, n => g.setEdge(n.source, n.target, n));
    };

    this.getLinks = () => {
      return g.edges().map(e => {
        return {
          source: g.node(e.v),
          target: g.node(e.w),
          data: g.edge(e)
        }
      });
    }

    this.getGraph = () => g;

    // find the end of the graph toward upstream
    this.getUpstreamSinks = (el) => {
      const sinks =  _.reduce(g.sinks(), (sinks, node, i) => {
        let n = g.node(node);
        if(n.type === 'upstream'){
          sinks.push(n);
        }
        return sinks;
      }, []);

      return _.map(sinks, (s, i) => {
        s.position = {
          top: 0,
          bottom: el.clientHeight,
          total: sinks.length,
          index: i + 1
        };
        s.fixed = true;
        return s;
      })
    };

    this.positionGraph = (el) => {
      // get root node
      let nodes = this.getUpstreamSinks(el);

      // find children, recursively
      let children = [];
      _.forEach(nodes, (n, i) => {
        children = children.concat(this.findPredecessor(n));
      });
      nodes = nodes.concat(children);

      // calculate the position for all nodes
      nodes = _.map(nodes, r => {
        return NodePositioner.getDataPlaneNodePos(r, el);
      });

      console.log(nodes);
      return nodes;
    };

    // this iterate on all the nodes, and add position information
    this.findPredecessor = (node) => {
      let preds = g.predecessors(node.id);

      // saving predecessor information
      preds = preds.map((p, i) => {
        p = g.node(p);
        const parentAvailableSpace = (node.position.bottom - node.position.top) / node.position.total;
        const parentY = NodePositioner.getVpos(node);
        p.position = {
          top: parentY - (parentAvailableSpace / 2),
          bottom: (parentY + (parentAvailableSpace / 2)),
          total: preds.length,
          index: i + 1
        };
        p.fixed = true;
        return p;
      });

      //recurse
      const predsChild = _.reduce(preds, (list, p) => {
        return list.concat(this.findPredecessor(p));
      }, []);

      return preds.concat(predsChild);
    };

    this.getGraphLinks = (nodes) => {
      const links = [];
      _.forEach(nodes, n => {
        const edges = g.inEdges(n.id);
        _.forEach(edges, e => {
          links.push({
            source: g.node(e.v),
            target: g.node(e.w),
            data: g.edge(e)
          });
          console.log(g.edge(e).id);
        });
      });
      console.log(links);
      return links;
    };

  })
  .service('NodePositioner', function(_, sliceElOrder){

    this.getHpos = (node, el) => {
      let elPos = sliceElOrder.indexOf(node.type) + 1;
      let x = (el.clientWidth / (sliceElOrder.length + 1)) * elPos;
      return x;
    };

    this.getVpos = (node) => {
      // calculate the available space to distribute items
      const availableSpace = node.position.bottom - node.position.top;

      // calculate the distance between each item
      const step = availableSpace / (node.position.total + 1);

      // vertical position
      const y = (step * node.position.index) + node.position.top;
      return y;
    };

    // for nodes that are part of the data plane
    this.getDataPlaneNodePos = (node, el) => {
      const x = this.getHpos(node, el);
      const y = this.getVpos(node);
      node.x = x;
      node.y = y;
      node.transform = `translate(${x}, ${y})`;
      return node;
    };

  });
})();
