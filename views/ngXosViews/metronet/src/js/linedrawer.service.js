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
  .service('MetronetListeners', function($rootScope, MetronetELineDrawer){

    this.begin = (map) => {
      // hold shift to enable draw eline
      // hold ctrl to draw etree
      // hold option/alt to draw e lan
      
      // TODO move all eline logic inside ElineDrawerService
      window.onkeyup = (e) => {
        if(e.key === 'Shift'){
          map.setOptions({draggable: true});
          // if line is not connecting unis, clear
          if(!MetronetELineDrawer.getStartUni() || !MetronetELineDrawer.getEndUni()){
            MetronetELineDrawer.cleanLine();
          }
          MetronetELineDrawer.resetMouseEventData();
          MetronetELineDrawer.detachDrawingEvents();
        };
      };
      window.onkeydown = (e) => {
        if(e.key === 'Shift'){
          MetronetELineDrawer.attachDrawingEvents(map);
          map.setOptions({draggable: false});
        };
      };
    }
  })
  .service('MetronetELineDrawer', function($rootScope){
    let drawingEnabled = false;
    let startUni, endUni, poly;
    let listener, moveListener = null;

    this.setStartUni = (uni) => {
      startUni = uni;
    };

    this.setEndUni = (uni) => {
      endUni = uni;
    };

    this.getStartUni = () => startUni;

    this.getEndUni = () => endUni;

    this.cleanLine = () => poly ? poly.setMap(null) : false;

    this.isDrawingEnabled = () => drawingEnabled;

    this.enableDrawing = () => drawingEnabled = true;

    this.disableDrawing = () => drawingEnabled = false;

    this.resetMouseEventData = () => {
      drawingEnabled = false;
      startUni = null;
      endUni = null;
    };

    this.detachDrawingEvents = () => {
      this.disableDrawing();
      google.maps.event.removeListener(listener);
      google.maps.event.removeListener(moveListener);
    };

    this.attachDrawingEvents = (map) => {
      this.enableDrawing();
      listener = google.maps.event.addDomListener(map.getDiv(), 'mousedown', (e) => {
        console.log('Eline Mouse Down');
        // do it with shift pressed only

        // the polygon
        poly = new google.maps.Polyline({map: map, clickable: true, info: 'test'});

        // move-listener
        moveListener = google.maps.event.addListener(map, 'mousemove', (e) => {
          if(poly.getPath().length === 2){
            poly.getPath().pop();
          }
          poly.getPath().push(e.latLng);
        });
        //mouseup-listener
        $(window).mouseup((e) => {

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
        });
      });
    };
  });
})();

