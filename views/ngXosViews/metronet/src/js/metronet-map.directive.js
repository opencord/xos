(function () {
  'use strict';

  // https://snazzymaps.com/explore
  // const mapStyles = [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}];
  const mapStyles = [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#444444"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#46bcec"},{"visibility":"on"}]}];

  angular.module('xos.metronet')
    .component('metronetMap', {
      controllerAs: 'vm',
      template: `
        <ng-map zoom="7" center="0, 0" styles="{{vm.mapStyles}}"></ng-map>
        <metronet-side-panel></metronet-side-panel>
      `,
      controller: function(
        $q,
        $rootScope,
        _,
        Eline,
        ELan,
        ETree,
        Uni,
        NgMap,
        CentralOffice,
        MetronetMap,
        MetronetEline,
        MetronetEtree,
        MetronetListeners) {
        this.mapStyles = mapStyles;

        this.bounds = new google.maps.LatLngBounds();

        NgMap.getMap()
        .then(map => {
          this.map = map;


          // render UNIs to map
          return CentralOffice.renderCo(this.map);
        })
        .then((cos) => {
          // TODO
          // [ ] if no result set zoom to a wide area

          // render connections on the map
          MetronetEline.renderElines(this.map);
          MetronetEtree.renderEtrees(this.map);
          // this.renderElans(this.elans, this.map);

          // center the map
          this.map.setCenter(MetronetMap.getBounds().getCenter());
          this.map.fitBounds(MetronetMap.getBounds());

          // listeing for events
          MetronetListeners.begin(this.map);
        })
        .catch(e => {
          throw new Error(e);
        });

      }
    });

}());