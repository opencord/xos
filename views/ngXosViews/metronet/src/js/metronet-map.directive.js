(function () {
  'use strict';

  // https://snazzymaps.com/explore
  // const mapStyles = [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}];
  const mapStyles = [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#444444"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#46bcec"},{"visibility":"on"}]}];

  const markerIcon = {
    path: 'M92.5,62.3l-33,33,2.5,2.5c4.1,4.1,7.4,3.6,11.2-.1L95.9,75l-4.5-4.5,4.7-4.7-3.6-3.6Zm2.6,7L98.4,66l3.3,3.3-3.3,3.3-3.3-3.3ZM94.5,60l4.9-4.9,4.9,4.9-4.9,4.9ZM36.2,36.1L18.6,53.8c-7.8,7.8-5.8,17.4-2.4,22l-2.2-2.2c-10.6-10.6-11.2-20,0-31.2L28.2,28.1L31.3,25l8,8-3.1,3.1ZM55.5,55.4l3.6-3.6L66.9,44l-8-8l-2.5,2.5-5.2,5.2l-3.6,3.6L33.2,61.6C22,72.7,22.5,82.2,33.2,92.8L35.4,95c-3.4-4.5-5.4-14.1,2.4-22L55.5,55.4ZM50.7,21.7l-8-8L35,21.2l8,8,7.6-7.6ZM62.8,9.6L55.4,17l-8-8,7.4-7.4,8,8Zm0.7,18.3-7.6,7.6-8-8,7.6-7.6,8,8Zm26.1-6.6-8.1,8.1-8-8,8.1-8.1,8,8ZM79.3,31.5l-7.4,7.4-8-8,7.4-7.4,8,8ZM45.7,45.6L54.3,37l-8-8-8.6,8.6L23.4,51.8C12.2,63,12.8,72.4,23.4,83l2.2,2.2c-3.4-4.5-5.4-14.1,2.4-22ZM34.9,80.7l20.6,20.5c2,2,4.6,4.1,7.9,3.2-2.9,2.9-8.9,1.7-11.9-1.3L35.1,86.8,35,86.6H34.9l-0.8-.8a15,15,0,0,1,.1-1.9,14.7,14.7,0,0,1,.7-3.2Zm-0.6,7.4a21.3,21.3,0,0,0,5.9,11.7l5.7,5.7c3,3,9,4.1,11.9,1.3-3.3.9-5.9-1.2-7.9-3.2L34.3,88.1Zm3.5-12.4a16.6,16.6,0,0,0-2.3,3.6L57,100.8c3,3,9,4.1,11.9,1.3-3.3.9-5.9-1.2-7.9-3.2Z',
    fillColor: '#C11D26',
    fillOpacity: 1,
    anchor: new google.maps.Point(50, 50),
    strokeWeight: 0,
    scale: 0.3,
    class: 'test'
  };

  const lineColors = {
    eline: '#008000',
    etree: '#0000FF',
    elan: '#EB8F00'
  };

  angular.module('xos.metronet')
    .component('metronetMap', {
      controllerAs: 'vm',
      template: `
        <ng-map zoom="7" center="0, 0" styles="{{vm.mapStyles}}"></ng-map>
        <metronet-side-panel></metronet-side-panel>
      `,
      controller: function($q, $rootScope, _, Eline, ELan, ETree, NgMap) {
        this.mapStyles = mapStyles;
        this.markers = [];
        this.elinesPath = [];
        this.etreesPath = [];
        this.elansPath = [];

        let startUni, endUni;

        this.bounds = new google.maps.LatLngBounds();

        $q.all([
          Eline.query().$promise,
          ELan.query().$promise,
          ETree.query().$promise,
          NgMap.getMap()
        ])
        .then(res => {
          [this.elines, this.elans, this.etrees, this.map] = res;
          // TODO
          // [ ] if no result send to creation form

          // render info on the map
          this.renderElines(this.elines, this.map);
          this.renderEtrees(this.etrees, this.map);
          this.renderElans(this.elans, this.map);

          // center the map
          this.map.setCenter(this.bounds.getCenter());
          this.map.fitBounds(this.bounds);

          this.attachLineHandler();
        })
        .catch(e => {
          throw new Error(e);
        });
        this.user = {name: 'world'};

        // draw Elines on map
        this.renderElines = (elines, map) => {
          _.forEach(elines, eline => {
            // augment with info
            eline.connectionType = 'eline';

            this.addMarker(eline.uni1);
            this.addMarker(eline.uni2);
            this.addPath(eline, eline.uni1, eline.uni2);
          });
        };

        // draw Etrees on map
        this.renderEtrees = (etrees, map) => {
          _.forEach(etrees, etree => {

            // augment with info
            etree.connectionType = 'etree';

            this.addMarker(etree.root);
            _.forEach(etree.eps, (uni) => {
              this.addMarker(uni);
            });

            let unis = _.reduce(etree.eps, (unis, uni) => {
              unis.push(uni);
              return unis;
            }, [etree.root]);

            this.addPath(etree, ...unis);
          });
        };

        this.renderElans = (elans, map) => {
          _.forEach(elans, elan => {

            // augment with info
            elan.connectionType = 'elan';

            _.forEach(elan.eps, (uni) => {
              this.addMarker(uni);
            });
            // NOTE should we close the line?
            const unis = angular.copy(elan.eps);
            unis.push(elan.eps[0]);
            this.addPath(elan, ...unis);
          });
        };

        this.addMarker = (uni) => {
          let [lng, lat] = JSON.parse(uni.latlng);
          angular.extend(uni, {lat: lat, lng: lng});

          // add markers
          const latlng = new google.maps.LatLng(lat, lng);
          const marker = new google.maps.Marker({
            position: latlng,
            map: this.map,
            icon: markerIcon,
            title: uni.name,
            optimized: false,
            uni: uni
          });
          marker.setMap(this.map);

          // add event listener
          google.maps.event.addListener(marker, 'mousedown', function() {
            if(drawingEnabled){
              console.log(this.uni);
              startUni = this.uni;
            }
          });
          google.maps.event.addListener(marker, 'mouseup', function() {
            if(drawingEnabled){
              console.log(this.uni);
              endUni = this.uni;
            }
          });

          // extend maps bounds
          this.bounds.extend(latlng);

          // add the info window
          this.addInfoWindow(marker);
        };

        this.addInfoWindow = (marker) => {
          const infowindow = new google.maps.InfoWindow({
            content: `
              <h4>${marker.uni.name}</h4>
              <strong>${marker.uni.location} - ${marker.uni.pid}</strong>
              <br/><br/>
              <table class="table table-bordered">
                <tr>
                    <th><small>bwpCfgCbs</small></th>
                    <td><small>${marker.uni.bwpCfgCbs}</small></td>
                    <th><small>bwpCfgCir</small></th>
                    <td><small>${marker.uni.bwpCfgCir}</small></td>
                </tr>
                <tr>
                    <th><small>bwpCfgEbs</small></th>
                    <td><small>${marker.uni.bwpCfgEbs}</small></td>
                    <th><small>bwpCfgEir</small></th>
                    <td><small>${marker.uni.bwpCfgEir}</small></td>
                </tr>
              </table>
            `
          });

          marker.addListener('click', function() {
            infowindow.open(this.map, marker);
          });
        };

        this.addPath = (connection, ...unis) => {

          // create a new Line
          const poly = new google.maps.Polyline({
            map: this.map,
            clickable: true,
            connection: connection,
            strokeColor: lineColors[connection.connectionType]
          });

          // attach a click handler
          poly.addListener('click', function() {
            $rootScope.$emit('connection.details', connection);
          });

          // attach all the point to the line
          const latlng = (uni) => {
            return {
              lat: () => uni.lat,
              lng: () => uni.lng,
            };
          };
          _.forEach(unis, uni => poly.getPath().push(latlng(uni)))
        };

        // draw a line
        let drawingEnabled = false;
        this.attachLineHandler = () => {

          // hold shift to enable draw eline
          // hold ctrl to draw etree
          // hold option/alt to draw e lan
          window.onkeyup = (e) => {
            if(e.keyCode === 16){
              drawingEnabled = false;
              this.map.setOptions({draggable: true});
            };
          };
          window.onkeydown = (e) => {
            if(e.keyCode === 16){
              drawingEnabled = true;
              this.map.setOptions({draggable: false});
            };
          };

          google.maps.event.addDomListener(this.map.getDiv(), 'mousedown', (e) => {
            //do it with the right mouse-button only
            if(!drawingEnabled){
              return;
            }
            //the polygon
            let poly = new google.maps.Polyline({map: this.map, clickable: true, info: 'test'});

            //move-listener
            var move = google.maps.event.addListener(this.map, 'mousemove', (e) => {
              if(poly.getPath().length === 2){
                poly.getPath().pop();
              }
              poly.getPath().push(e.latLng);
            });
            //mouseup-listener
            $(window).mouseup((e) => {

              // TODO
              // [ ] Get if the event occur over a marker
              // [ ] Create a new E-LINE, E-LAN, E-TREE

              console.log('mouseup');

              // delete the line
              // poly.setMap(null);

              // check if we have start and end UNI
              if(startUni  && endUni){
                console.log(`Create a connection from ${startUni.name} to ${endUni.name}`);
              }

              google.maps.event.removeListener(move);
            });
          });
        }
      }
    });

}());