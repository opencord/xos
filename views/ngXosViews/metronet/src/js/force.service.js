(function () {
  'use strict';

  angular.module('xos.metronet')
  .service('MetronetForce', function($window, NgMap, MetronetCfg, MetronetState, MetronetGraph){

    // store locally the overlay
    let overlay;

    const force = d3.layout.force()
      .size([$window.innerWidth, $window.innerHeight])
      .friction(0.9)
      .linkStrength(l => {
        // link form CO to port are stronger than others
        if(!l.connection){
          return 1;
        }
        return 0;
      })
      .linkDistance((l) => {
        if(!l.connection){
          return 40;
        }
        return 100;
      })
      .charge(n => n.type === 'co' ? -5 : -1)
      .gravity(0)
      // .theta(0.8)
      // .alpha(0.1);

    const bounds = new google.maps.LatLngBounds();

    const dragUni = force.drag()
      .on('dragstart', (n) => {
        n.fixed = true;
      });

    this.getInitialBounds = () => bounds;

    const tick = (e) => {
      // console.log('tick', e);
      const svg = d3.select('svg');

      svg.selectAll('.link')
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      svg.selectAll('.node')
        .attr('transform', n => {
          return (n.x && n.y) ? `translate(${n.x}, ${n.y})` : '';
        });
    };

    // start the force layout
    this.start = (ov) => {
      overlay = ov;
      NgMap.getMap()
      .then(map => {
        this.map = map;

        const nodes = MetronetGraph.nodes();
        const links = MetronetGraph.links();

        // set the map in the correct initial position
        nodes.forEach(n => {
          const latlng = new google.maps.LatLng(n.latlng.lat, n.latlng.lng);
          bounds.extend(latlng);
        });
        this.map.setCenter(bounds.getCenter());
        this.map.fitBounds(bounds);

        force
          .nodes(nodes)
          .links(links)
          .on('tick', tick)
      })
      .catch(err => {
        console.warn(err);
      });
    };

    this.resize = (width, height) => {
      force.size([width, height]).resume()
    };

    this.redraw = () => {
      this.setNodes(overlay.nodeContainer, overlay);
      this.setLinks(overlay.linkContainer)
    }

    // draw nodes on the map
    this.setNodes = (svg, overlay) => {

      const projection = overlay.getProjection();

      // set node in the correct position
      
      const nodes = MetronetGraph.nodes().map(n => {
        if(n.fixed && n.type === 'co'){

          const latlng = new google.maps.LatLng(n.latlng.lat, n.latlng.lng);
          var d = projection.fromLatLngToDivPixel(latlng);

          // we need to store also the node previuous position,
          // otherwise it's stored (and used in tick fn) the one from the first rendering of the map
          n.x = d.x;
          n.y = d.y;
          n.px = d.x;
          n.py = d.y;
        }
        // TODO recalculate position of fixed ports
        return n;
      });

      force
        .nodes(nodes)
        .start();

      var node = svg.selectAll('.node')
        .data(nodes)
        .attr({
          class: n => {
            return `node ${n.type} ${n.fixed ? 'fixed': ''} ${n.selected ? 'selected': ''}`;
          },
          transform: n => (n.x && n.y) ? `translate(${n.x}, ${n.y})` : ''
        });

      // draw labels
      if(MetronetState.showLabels){
        const label = node
          .append('text')
          .attr({
            x: 10,
            y: 4,
            opacity: 0
          })
          .text(n => n.name);

        // extend node
        node
          .transition()
          .duration(MetronetCfg.transition)
          .select('rect')
          .attr({
            width: function(){
              const labelWidth = d3.select(this.parentNode).select('text').node().getBBox().width;
              return 20 + 5 + labelWidth;
            }
          });

        label
          .transition()
          .duration(MetronetCfg.transition)
          .attr({
            opacity: 1
          })
      }
      else{
        node
          .select('rect')
          .transition()
          .duration(MetronetCfg.transition)
          .attr({
            width: 20
          });
        node
          .select('text')
          .transition()
          .duration(MetronetCfg.transition)
          .attr({
            opacity: 0
          })
          .remove();
      }

      const newNode = node.enter()
        .append('g')
        .attr({
          class: n => {
            return `node ${n.type} ${n.fixed ? 'fixed': ''} ${n.selected ? 'selected': ''}`;
          },
          transform: n => {
            if(n.id === 7){
              console.log(n.x, n.y, n.px, n.py);
            }
            return (n.x && n.y) ? `translate(${n.x}, ${n.y})`: ''
          }
        });

      // node background
      newNode
        .append('rect')
        .attr({
          width: 20,
          height: 20,
          x: -10,
          y: -10
        });

      // append icons (based on type)
      newNode.append('path')
        .attr({
          d: n => MetronetCfg.icons[n.type],
          class: 'icon'
        });

      // call drag on UNI
      newNode
        .filter(n => n.type === 'uni')
        .on('mouseover', () => {
          NgMap.getMap().then((map) => {
            map.setOptions({draggable: false});
          });
        })
        .on('mouseout', () => {
          // TODO save lat/lng of the position
          // needed to relocate them when the map zoom out
          NgMap.getMap().then((map) => {
            map.setOptions({draggable: true});
          });
        })
        .on('click', n => {
          if(d3.event.shiftKey){
            n.selected = !n.selected;
            this.setNodes(overlay.nodeContainer, overlay);
          }
        })
        .call(dragUni);

      // show ports on CO
      newNode
        .filter(n => n.type === 'co')
        .on('click', n => {
          MetronetGraph.togglePorts(n);
          this.setNodes(overlay.nodeContainer, overlay);
          this.setLinks(overlay.linkContainer, overlay);
          force.start();
        });

      // remove nodes
      const oldNode = node.exit()
      .attr({
        opacity: 1
      })
      .transition().duration(MetronetCfg.transition)
      .attr({
        transform: n => {
          const co = MetronetGraph.getCoByUni(n);
          return `translate(${co.x}, ${co.y})`
        },
        opacity: 0
      })
      .remove();
    };

    // draw links on the map
    this.setLinks = (svg) => {
      var link = svg.selectAll('.link')
        .data(MetronetGraph.links())
        .attr({
          x1: l => l.source.x,
          y1: l => l.source.y,
          x2: l => l.target.x,
          y2: l => l.target.y,
        });

      link.enter()
        .append('line')
        .attr({
          class: l => `link ${l.connection ? l.connection.type : 'local'}`,
          x1: l => l.source.x,
          y1: l => l.source.y,
          x2: l => l.target.x,
          y2: l => l.target.y,
        });

      link.exit()
        .attr({
          opacity: 1,
          x1: l => l.source.x,
          y1: l => l.source.y,
          x2: l => l.target.x,
          y2: l => l.target.y,
        })
        .transition()
        .duration(MetronetCfg.transition)
        .attr({
          x1: l => l.source.x,
          y1: l => l.source.y,
          x2: l => l.target.x,
          y2: l => l.target.y,
          opacity: 0
        })
        .remove();
    };
  })
})();