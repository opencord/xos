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
      controller: function($element, McordSlicingTopo, _, elementPositioner){

        let svg;
        let nodes, links;

        this.activeSlices = [];

        McordSlicingTopo.query().$promise
        .then((topology) => {
          this.nodes = topology.nodes;
          this.links = topology.links;
          this.topology = topology;
          handleSvg($element[0]);
          buildAllSlicesData(topology);
          drawGraph();
        })
        .catch((e) => {
          throw new Error(e);
        });

        const augmentNodeWithPosInfo = (list, kind) => list.map((s, sIdx) => {
          s.nodes = _.map(s.nodes, n => {
            n.parentId = sIdx;
            n.parentKind = kind;
            n.vPos = sIdx + 1;
            n.vTotal = list.length;
            return n;
          })

          return s;
        });

        const handleSvg = (el) => {
          this.el = el;
          d3.select(el).select('svg').remove();

          // console.log(`${el.clientWidth} x ${el.clientHeight}`);

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

        // prepare the data to show all slices
        let _nodes = [];
        let _links = [];
        const buildAllSlicesData = topoData => {
          _.forEach(Object.keys(topoData), k => {
            // augment nodes with position info
            topoData[k] = augmentNodeWithPosInfo(topoData[k], k);
            _.forEach(topoData[k], item => {
              // retrieve all data plane nodes from the data
              _nodes = _nodes.concat(_.filter(item.nodes, n => n.plane === 'data'));
              // retrieve all data plane links
              _links = _links.concat(_.filter(item.links, n => n.plane === 'data'))
            });
          });
          // set nodes in a fixed position
          _nodes = _.map(_nodes, n => {
            let [x, y] = elementPositioner.getNodePosition(n, this.el);
            n.x = x;
            n.y = y;
            n.transform = `translate(${x}, ${y})`;
            n.fixed = true;
            return n;
          });

          // map links to nodes
          _links = _.map(_links, l => {
            return {
              source: _.find(_nodes, {id: l.source}),
              target: _.find(_nodes, {id: l.target}),
              data: l
            };
          });
        };

        // attach slice details
        const attachSliceDetails = sliceId => {

          if(this.activeSlices.indexOf(sliceId) > -1){
            // slice is already expanded
            console.log(`Slice ${sliceId} is already active`);
            return;
          }

          this.activeSlices.push(sliceId);

          // find slice related nodes and links
          let newNodes = _.filter(this.topology.slices[sliceId].nodes, n => n.plane === 'control');
          let newLinks = _.filter(this.topology.slices[sliceId].links, l => l.plane === 'control');
          
          // set nodes in a fixed position
          newNodes = _.map(newNodes, n => {
            let [x, y] = elementPositioner.getNodePosition(n, this.el);
            n.x = x;
            n.y = y;
            n.transform = `translate(${x}, ${y})`;
            n.fixed = true;
            return n;
          });
          
          _nodes = _nodes.concat(newNodes);


          // map links to nodes
          newLinks = _.map(newLinks, l => {
            return {
              source: _.find(_nodes, {id: l.source}),
              target: _.find(_nodes, {id: l.target}),
              data: l
            };
          });

          _links = _links.concat(newLinks);

          drawGraph();
        };

        // remove slice detail
        const removeSliceDetails = sliceId => {
          console.log(`remove slice ${sliceId}`);
          if(this.activeSlices.indexOf(sliceId) === -1){
            // slice is already expanded
            console.log(`Slice ${sliceId} is not active`);
            return;
          }

          this.activeSlices.splice(this.activeSlices.indexOf(sliceId), 1);

          // remove control plane nodes related to this slice
          _nodes = _.filter(_nodes, n => {
            if(n.parentId !== sliceId){
              return true;
            }
            return n.plane === 'data';
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
        }

        const drawGraph = () => {

          var force = d3.layout.force()
            .nodes(_nodes)
            .links(_links)
            .charge(-1060)
            .gravity(0.1)
            .linkDistance(200)
            .size([this.el.clientWidth, this.el.clientHeight])
            .on('tick', tick)
            .start();

          // clear nodes and links
          svg.selectAll('.node-container').remove();
          svg.selectAll('.link-container').remove();


          links = svg.selectAll('.link-container')
            .data(_links).enter()
            .insert('g')
            .attr('class', 'link-container');

          links.insert('line')
            .attr('class', d => `link ${d.data.plane}`)


          nodes = svg.selectAll('.node')
            .data(_nodes)
            .enter().append('g')
            .attr({
              class: 'node-container',
              transform: d => d.transform
            })
            .on('click', function(d){
              if(d.parentKind === 'slices' && d.plane === 'data'){
                attachSliceDetails(d.parentId);
              }
              else if (d.parentKind === 'slices' && d.plane === 'control'){
                removeSliceDetails(d.parentId);
              }
            });

          nodes.append('rect')
            .attr({
              class: d => `node ${d.plane} ${d.parentKind}`,
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