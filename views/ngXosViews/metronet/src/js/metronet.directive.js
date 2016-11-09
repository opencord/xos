(function () {
  'use strict';

  // const mapStyles = [{'featureType': 'administrative', 'elementType': 'labels.text.fill', 'stylers': [{'color': '#444444'}]}, {'featureType': 'landscape', 'elementType': 'all', 'stylers': [{'color': '#f2f2f2'}]}, {'featureType': 'poi', 'elementType': 'all', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'road', 'elementType': 'all', 'stylers': [{'saturation': -100}, {'lightness': 45}]}, {'featureType': 'road.highway', 'elementType': 'all', 'stylers': [{'visibility': 'simplified'}]}, {'featureType': 'road.arterial', 'elementType': 'labels.icon', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'transit', 'elementType': 'all', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'water', 'elementType': 'all', 'stylers': [{'color': '#46bcec'}, {'visibility': 'on'}]}];
  const mapStyles = [{featureType: 'all', elementType: 'labels.text.fill', stylers: [{saturation: 36}, {color: '#333333'}, {lightness: 40}]}, {featureType: 'all', elementType: 'labels.text.stroke', stylers: [{visibility: 'on'}, {color: '#ffffff'}, {lightness: 16}]}, {featureType: 'all', elementType: 'labels.icon', stylers: [{visibility: 'off'}]}, {featureType: 'administrative', elementType: 'geometry.fill', stylers: [{color: '#fefefe'}, {lightness: 20}]}, {featureType: 'administrative', elementType: 'geometry.stroke', stylers: [{color: '#fefefe'}, {lightness: 17}, {weight: 1.2}]}, {featureType: 'administrative', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'administrative.country', elementType: 'labels.text.fill', stylers: [{visibility: 'off'}]}, {featureType: 'administrative.province', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'administrative.locality', elementType: 'labels', stylers: [{visibility: 'simplified'}, {weight: '0.01'}]}, {featureType: 'administrative.neighborhood', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'administrative.land_parcel', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'landscape', elementType: 'geometry', stylers: [{color: '#f5f5f5'}, {lightness: 20}]}, {featureType: 'landscape', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'poi', elementType: 'geometry', stylers: [{color: '#f5f5f5'}, {lightness: 21}]}, {featureType: 'poi', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'poi.attraction', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'poi.business', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'poi.government', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'poi.medical', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'poi.park', elementType: 'geometry', stylers: [{color: '#dedede'}, {lightness: 21}]}, {featureType: 'poi.park', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'poi.place_of_worship', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'poi.school', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'poi.sports_complex', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'road', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'road.highway', elementType: 'geometry.fill', stylers: [{color: '#ffffff'}, {lightness: 17}]}, {featureType: 'road.highway', elementType: 'geometry.stroke', stylers: [{color: '#ffffff'}, {lightness: 29}, {weight: .2}]}, {featureType: 'road.arterial', elementType: 'geometry', stylers: [{color: '#ffffff'}, {lightness: 18}]}, {featureType: 'road.local', elementType: 'geometry', stylers: [{color: '#ffffff'}, {lightness: 16}]}, {featureType: 'transit', elementType: 'geometry', stylers: [{color: '#f2f2f2'}, {lightness: 19}]}, {featureType: 'transit', elementType: 'labels', stylers: [{visibility: 'off'}]}, {featureType: 'water', elementType: 'geometry', stylers: [{color: '#e9e9e9'}, {lightness: 17}]}];
  angular.module('xos.metronet')
  .component('metronetMap', {
    controllerAs: 'vm',
    template: `
      <metronet-panel></metronet-panel>
      <ng-map zoom='7' center='{{vm.mapCenter}}' styles='{{vm.mapStyles}}'></ng-map>
      <metronet-side-panel></metronet-side-panel>
    `,
    controller: function($q, NgMap, MetronetListener, MetronetGraph, MetronetOverlay){
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
        
      })
      .catch(e => {
        throw new Error(e);
      });

    }
  });
})();