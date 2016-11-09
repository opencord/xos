(function () {
  'use strict';

  angular.module('xos.metronet')
  .service('MetronetOverlay', function($window, MetronetForce, MetronetCfg){
    const self = this;
    const overlay = new google.maps.OverlayView();

    this.setOnMap = (map) => {
      overlay.setMap(map);
    };

    this.getOverlayPosition = () => {
      const sw = overlay.getProjection().fromLatLngToDivPixel(MetronetForce.getInitialBounds().getSouthWest());
      const ne = overlay.getProjection().fromLatLngToDivPixel(MetronetForce.getInitialBounds().getNorthEast());

      const left = sw.x - MetronetCfg.overlay.padding;
      const top = ne.y - MetronetCfg.overlay.padding;

      return [left, top];
    };

    this.getOverlaySize = () => {
      const sw = overlay.getProjection().fromLatLngToDivPixel(MetronetForce.getInitialBounds().getSouthWest());
      const ne = overlay.getProjection().fromLatLngToDivPixel(MetronetForce.getInitialBounds().getNorthEast());

      const width = (ne.x - sw.x) + (MetronetCfg.overlay.padding * 2);
      const height = (sw.y - ne.y) + (MetronetCfg.overlay.padding * 2);

      return [width, height];
    };

    // Add the container when the overlay is added to the map.
    overlay.onAdd = function() {

      // create the svg
      this.svg = d3.select(this.getPanes().overlayMouseTarget)
        .append('div')
        .attr({
          class: 'topo-container',
        })
        .style({
          height: $window.innerHeight,
          width: '100%'
        })
        .append('svg')
        .style({
          height: $window.innerHeight,
          width: '100%'
        });
      
      // create a container for links and nodes
      this.linkContainer = this.svg.append('g')
        .attr({
          class: 'link-container'
        });

      this.nodeContainer = this.svg.append('g')
        .attr({
          class: 'node-container'
        });
      MetronetForce.start(this.svg);
    };

    // anytime the map change (eg: zoom)
    // - move the svg
    // - Redraw the graph
    overlay.draw = function(){
      MetronetForce.setNodes(this.nodeContainer, this);
      MetronetForce.setLinks(this.linkContainer, this);
    };
  });
})();