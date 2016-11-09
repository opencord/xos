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
  .service('MetronetListeners', function(
    $rootScope,
    MetronetELineDrawer,
    MetronetEtreeDrawer,
    CentralOffice){

    const validKey= ['Shift', 'Meta', 'Alt'];

    this.begin = (map) => {
      // hold shift to enable draw eline
      // hold Meta to draw etree
      // hold option/alt to draw elan
      
      const ports = CentralOffice.getPorts();
      const cos = CentralOffice.getCos();

      window.onkeyup = (e) => {

        // reattach default listeners
        if(validKey.indexOf(e.key) > -1){
          map.setOptions({draggable: true});
          _.forEach(ports, (marker) => {
            CentralOffice.addInfoWindowListener(marker);
          });

          _.forEach(cos, (marker) => {
            google.maps.event.clearInstanceListeners(marker);
            CentralOffice.addCoListener(marker, map);
          });
        }

        if(e.key === 'Shift'){
          MetronetELineDrawer.detachDrawingEvents();
        };

        if(e.key === 'Meta'){
          // TODO and save
          MetronetEtreeDrawer.detachDrawingEvents();
        };
      };
      window.onkeydown = (e) => {
        console.log(e.key);
        if(validKey.indexOf(e.key) > -1){
          map.setOptions({draggable: false});

          // clear existing listener from port
          _.forEach(ports, (marker) => {
            google.maps.event.clearInstanceListeners(marker);
          });

          // attach marker events to COs
          _.forEach(cos, (marker) => {
            marker.addListener('mouseover', function() {
              if(this.portShown !== true){
                // draw ports
                CentralOffice.showPortsFromCo(this, map);
                // NOTE emitting an event to notify multiple services
                $rootScope.$emit('metronet.redrawConnections', map);
              }
            });
          });
        }

        if(e.key === 'Shift'){
          MetronetELineDrawer.attachDrawingEvents(map);
        };

        if(e.key === 'Meta'){
          MetronetEtreeDrawer.attachDrawingEvents(map);
        };
      };
    }
  });
})();

