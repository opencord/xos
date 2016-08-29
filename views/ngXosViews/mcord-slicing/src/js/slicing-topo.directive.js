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
      controller: function($element, SliceGraph, McordSlicingTopo, _, NodePositioner, FormHandler){

        let svg;
        let nodes, links;
        let nodeGroup, linkGroup, formGroup;
        let dragLine, dragStartNode, dragEndNode;

        var t = d3.transition()
          .duration(500);

        this.activeSlices = [];

        const resetDragInfo = () => {
          // reset drag nodes
          dragStartNode = null;
          dragEndNode = null;

          // hide dragLine
          dragLine
            .classed('hidden', true);
        };

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

          formGroup = d3.select(el)
            .append('div')
            .attr({
              class: 'form-container'
            });

          // line displayed when dragging nodes
          dragLine = svg.append('svg:path')
            .attr('class', 'dragline hidden')
            .attr('d', 'M0,0L0,0');
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
              // if I remove the node check that there is no form attached
              FormHandler.removeFormByParentNode(n, linkGroup, formGroup);
              return false;
            }
            return true;
          });

          // remove sliceId from data plane element
          _nodes = _.map(_nodes, n => {
            if(n.sliceId === sliceId){
              delete n.sliceId;
            }
            return n;
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
            .text(d => `${d.id} ${d.name}`);

          nodes.on('click', (n) => {
            resetDragInfo();
            const sliceComponents = ['ran-ru', 'ran-cu', 'pgw', 'sgw'];
            if(sliceComponents.indexOf(n.type) > -1 && n.plane === 'data' && !n.sliceId){
              attachSliceDetails(n);
            }
            else if (n.type === 'button'){
              removeSliceDetails(n.sliceId);
            }
            else if (!n.formAttached){
              n.formAttached = true;
              FormHandler.drawForm(n, linkGroup, formGroup);
            }
            else if (n.formAttached){
              n.formAttached = false;
              FormHandler.removeFormByParentNode(n, linkGroup, formGroup);
            }
          });

          nodes
            .on('mousedown', (n) => {
              // save a reference to dragStart
              dragStartNode = n;

              dragLine
                .classed('hidden', false)
                .attr('d', 'M' + dragStartNode.x + ',' + dragStartNode.y + 'L' + dragStartNode.x + ',' + dragStartNode.y);
            })
            .on('mouseover', (n) => {
              // console.log();
              if(dragStartNode){
                dragEndNode = n;
              }
              // else if (dragStartNode = dragEndNode){
              //   dragStartNode = null;
              // }
            });

          svg
            .on('mousemove', function(){
              if(!dragStartNode){
                return;
              }
              dragLine.attr('d', 'M' + dragStartNode.x + ',' + dragStartNode.y + 'L' + d3.mouse(this)[0] + ',' + d3.mouse(this)[1]);
            })
            .on('mouseup', () => {
              if(!dragStartNode || !dragEndNode){
                return;
              }

              // TODO
              // [X] check that I can connect the two nodes
              // [X] check link direction
              // [ ] save the new link in the BE

              // check that I can connect the 2 nodes
              const successorType = SliceGraph.getNodeDataPlaneSuccessors(dragStartNode)[0].type;
              if(dragEndNode.type !== successorType){
                resetDragInfo();
                return;
              }

              // create the link
              _links.push({
                source: dragStartNode,
                target: dragEndNode,
                data: {
                  id: `${dragStartNode.id}.${dragEndNode.id}`,
                  source: dragStartNode.id,
                  target: dragEndNode.id
                }
              });

              // update the graph
              // TODO recalculate graph positions
              drawGraph();

              resetDragInfo();
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