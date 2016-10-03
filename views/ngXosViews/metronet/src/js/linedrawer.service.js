/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 10/18/16.
 */

(function () {
  'use strict';

  angular.module('xos.metronet')
  .service('MetronetLineDrawer', function($rootScope){
    let drawingEnabled = false;
    let startUni, endUni, poly;

    this.setStartUni = (uni) => {
      startUni = uni;
    };

    this.setEndUni = (uni) => {
      endUni = uni;
    };

    this.cleanLine = () => poly ? poly.setMap(null) : false;

    this.isDrawingEnabled = () => drawingEnabled;

    this.resetMouseEventData = () => {
      drawingEnabled = false;
      startUni = null;
      endUni = null;
    };

    this.attachDrawingEvents = (map) => {

      // hold shift to enable draw eline
      // hold ctrl to draw etree
      // hold option/alt to draw e lan
      window.onkeyup = (e) => {
        if(e.key === 'Shift'){
          drawingEnabled = false;
          map.setOptions({draggable: true});
          // if line is not connecting unis, clear
          if(!startUni || !endUni){
            this.cleanLine();
          }
          this.resetMouseEventData();
        };
      };
      window.onkeydown = (e) => {
        if(e.key === 'Shift'){
          drawingEnabled = true;
          map.setOptions({draggable: false});
        };
      };

      google.maps.event.addDomListener(map.getDiv(), 'mousedown', (e) => {
        // do it with shift pressed only
        if(!drawingEnabled){
          return;
        }
        // the polygon
        poly = new google.maps.Polyline({map: map, clickable: true, info: 'test'});

        // move-listener
        var move = google.maps.event.addListener(map, 'mousemove', (e) => {
          if(poly.getPath().length === 2){
            poly.getPath().pop();
          }
          poly.getPath().push(e.latLng);
        });
        //mouseup-listener
        $(window).mouseup((e) => {

          if(!drawingEnabled){
            return;
          }

          // TODO
          // [x] Get if the event occur over a marker
          // [ ] Create a new E-LINE, E-LAN, E-TREE

          // check if we have start and end UNI
          if(startUni && endUni){
            console.log(`Create a connection from ${startUni.name} to ${endUni.name}`);
            $rootScope.$emit('connection.details', {
              uni1: startUni,
              uni2: endUni,
              kind: 'eline',
              type: 'direct'
            });
          }

          google.maps.event.removeListener(move);
        });
      });
    };
  });
})();

