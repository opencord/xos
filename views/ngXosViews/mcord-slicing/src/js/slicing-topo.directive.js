(function () {
  'use strict';

  angular.module('xos.mcord-slicing')
  .directive('slicingTopo', function(){
    return {
      restrict: 'E',
      scope: {},
      bindToController: true,
      controllerAs: 'vm',
      templateUrl: 'templates/slicing-topo.tpl.html',
      controller: function($element, McordSlicingTopo, _, slicePositioner){

        let svg;
        let el = $element[0];
        let nodes, links;

        let sliceNumber = 0;

        McordSlicingTopo.query().$promise
        .then((topology) => {
          this.nodes = topology.nodes;
          this.links = topology.links;

          sliceNumber = topology.slices.length;

          // add slice index to interested nodes
          topology.slices = augmentNodeWithSliceInfo(topology.slices);

          drawAllSlices(topology);
        })
        .catch((e) => {
          throw new Error(e);
        });

        const augmentNodeWithSliceInfo = slices => slices.map((s, sIdx) => {
          s.nodes = _.map(s.nodes, n => {
            n.sliceId = sIdx + 1
            return n;
          })

          return s;
        });

        const handleSvg = (el) => {
          d3.select(el).select('svg').remove();

          svg = d3.select(el)
          .append('svg')
          .style('width', `${el.clientWidth}px`)
          .style('height', `${el.clientHeight}px`);
        };

        const tick = () => {
          svg.selectAll('.link')
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        }

        const drawAllSlices = (topoData) => {

          let _nodes = [];
          let _links = [];

          _.forEach(Object.keys(topoData), k => {
            _.forEach(topoData[k], item => {
              // retrieve all data plane nodes from the data
              _nodes = _nodes.concat(_.filter(item.nodes, n => n.plane === 'data'));
              // retrieve all data plane links
              _links = _links.concat(_.filter(item.links, n => n.plane === 'data'))
            });
          });

          handleSvg(el);
          // in the global view only data plane object are represented
          // _nodes = _.filter(_nodes, n => n.plane === 'data');

          // set nodes in a fixed position
          _nodes = _.map(_nodes, n => {
            let [x, y] = slicePositioner.getNodePosition(n, sliceNumber, el);
            n.x = x;
            n.y = y;
            n.transform = `translate(${x}, ${y})`;
            n.fixed = true;
            return n;
          });

          // keep only the relevant links
          // _links = _.filter(_links, l => {
          //   let hasStart = _.findIndex(_nodes, {id: l.source}) > -1;
          //   let hasEnd = _.findIndex(_nodes, {id: l.target}) > -1;
          //   return hasStart && hasEnd;
          // });

          // map links to nodes
          _links = _.map(_links, l => {
            return {
              source: _.find(_nodes, {id: l.source}),
              target: _.find(_nodes, {id: l.target}),
              data: l
            };
          });

          console.log(_nodes, _links);

          var force = d3.layout.force()
            .nodes(_nodes)
            .links(_links)
            .charge(-1060)
            .gravity(0.1)
            .linkDistance(200)
            .size([el.clientWidth, el.clientHeight])
            .on('tick', tick)
            .start();

          links = svg.selectAll('.link-container')
            .data(_links).enter()
            .insert('g')
            .attr('class', 'link-container');

          links.insert('line')
            .attr('class', 'link')

          nodes = svg.selectAll('.node')
            .data(_nodes)
            .enter().append('g')
            .attr({
              class: 'node-container',
              transform: d => d.transform
            });

          nodes.append('rect')
            .attr({
              class: d => `node ${d.plane || ''}`,
              width: 100,
              height: 50,
              x: -50,
              y: -25
            });

          nodes.append('text')
            .attr({
              'text-anchor': 'middle',
              'alignment-baseline': 'middle'
            })
            .text(d => `${d.id} - ${d.name}`);

        };
      }
    }
  });
})();