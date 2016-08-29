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
      controller: function($element, SliceGraph, McordSlicingTopo, _, NodePositioner){

        let svg;
        let nodes, links;
        let nodeGroup, linkGroup;

        var t = d3.transition()
          .duration(500);

        this.activeSlices = [];

        McordSlicingTopo.query().$promise
        .then((topology) => {
          NodePositioner.storeEl($element[0]);
          handleSvg($element[0]);
          SliceGraph.buildGraph(topology);
          _nodes = SliceGraph.positionGraph($element[0]);
          _links = SliceGraph.getGraphLinks(_nodes);
          drawGraph();
        })
        .catch((e) => {
          throw new Error(e);
        });

        const handleSvg = (el) => {
          this.el = el;
          d3.select(el).select('svg').remove();

          svg = d3.select(el)
          .append('svg')
          .style('width', `${el.clientWidth}px`)
          .style('height', `${el.clientHeight}px`);

          linkGroup = svg.append('g')
            .attr({
              class: 'link-group'
            });

          nodeGroup = svg.append('g')
            .attr({
              class: 'node-group'
            });
        };

        const tick = () => {
          svg.selectAll('.link')
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        };

        // prepare the data to show all slices
        let _nodes = [];
        let _links = [];

        // attach slice details
        const attachSliceDetails = n => {
          let [newNodes, newLinks] = SliceGraph.getSliceDetail(n);
          _nodes = _nodes.concat(newNodes);
          _links = _links.concat(newLinks);
          drawGraph();
        };

        // remove slice detail
        const removeSliceDetails = sliceId => {

          SliceGraph.removeActiveSlice(sliceId);

          // remove control plane nodes related to this slice
          _nodes = _.filter(_nodes, n => {
            if(n.sliceId === sliceId && (n.plane === 'control' || n.type === 'button')){
              return false;
            }
            return true;
          });

          // remove control plane links related to this slice
          _links = _.filter(_links, l => {
            if(_.findIndex(_nodes, {id: l.data.source}) === -1){
              return false;
            }
            if(_.findIndex(_nodes, {id: l.data.target}) === -1){
              return false;
            }
            return true;
          });
          drawGraph();
        };

        const drawGraph = () => {

          // svg.selectAll('.node-container').remove();
          // svg.selectAll('.link-container').remove();

          var force = d3.layout.force()
            .nodes(_nodes)
            .links(_links)
            .charge(-1060)
            .gravity(0.1)
            .linkDistance(200)
            .size([this.el.clientWidth, this.el.clientHeight])
            .on('tick', tick)
            .start();

          links = linkGroup.selectAll('.link-container')
            .data(_links, d => d.data.id)
            .enter()
            .insert('g')
            .attr({
              class: 'link-container',
              opacity: 0
            });

          links
            .transition(t)
            .attr({
              opacity: 1
            });

          links.insert('line')
            .attr('class', d => `link ${d.data.plane}`);

          nodes = nodeGroup.selectAll('.node')
            .data(_nodes, d => d.id)
            .enter()
            .append('g')
            .attr({
              class: 'node-container',
              transform: d => d.transform,
              opacity: 0
            });

          nodes.transition(t)
            .attr({
              opacity: 1
            });

          nodes.append('rect')
            .attr({
              class: d => `node ${d.plane} ${d.type}`,
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

          nodes.on('click', (n) => {
            const sliceComponents = ['ran-ru', 'ran-cu', 'pgw', 'sgw'];
            if(sliceComponents.indexOf(n.type) > -1 && n.plane === 'data'){
              attachSliceDetails(n);
            }
            else if (n.type === 'button'){
              removeSliceDetails(n.sliceId);
            }
          });

          // remove exiting nodes
          svg.selectAll('.node-container')
            .data(_nodes, d => d.id)
            .exit()
            .transition(t)
            .attr({
              opacity: 0
            })
            .remove();

          // remove exiting links
          svg.selectAll('.link-container')
            .data(_links, d => d.data.id)
            .exit()
            .transition(t)
            .attr({
              opacity: 0
            })
            .remove();
        };
      }
    }
  });
})();