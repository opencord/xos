(function () {
  'use strict';

  const mapStyles = [{'featureType': 'administrative', 'elementType': 'labels.text.fill', 'stylers': [{'color': '#444444'}]}, {'featureType': 'landscape', 'elementType': 'all', 'stylers': [{'color': '#f2f2f2'}]}, {'featureType': 'poi', 'elementType': 'all', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'road', 'elementType': 'all', 'stylers': [{'saturation': -100}, {'lightness': 45}]}, {'featureType': 'road.highway', 'elementType': 'all', 'stylers': [{'visibility': 'simplified'}]}, {'featureType': 'road.arterial', 'elementType': 'labels.icon', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'transit', 'elementType': 'all', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'water', 'elementType': 'all', 'stylers': [{'color': '#46bcec'}, {'visibility': 'on'}]}];

  angular.module('xos.metronet')
  .component('metronetMap', {
    controllerAs: 'vm',
    template: `
      <ng-map zoom='7' center='{{vm.mapCenter}}' styles='{{vm.mapStyles}}'></ng-map>
      <metronet-side-panel></metronet-side-panel>
    `,
    controller: function($q, $window, NgMap, MetronetOverlay, MetronetGraph){
      this.mapStyles = mapStyles;
      this.svg;

      this.mapCenter = `37.648600906606795, -121.855098`;

      this.bounds = new google.maps.LatLngBounds();

      $q.all([
        NgMap.getMap(),
        MetronetGraph.loadData()
      ])
      .then(res => {
        let [map, graph] = res;

        MetronetOverlay.setOnMap(map);

        // console.log(MetronetGraph.nodes(), MetronetGraph.links());

        
      })
      .catch(e => {
        throw new Error(e);
      });

    }
  });
})();