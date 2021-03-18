var lon = document.getElementById('issLon').value;
var lat = document.getElementById('issLat').value;

const iconFeature = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat])),
    name: 'ISS location',
});

var map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        }),
        new ol.layer.Vector({
            source: new ol.source.Vector({
                features: [iconFeature]
            }),
            style: new ol.style.Style({
                image: new ol.style.Icon({
                    anchor: [0.5, 46],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'pixels',
                    src: '/static/img/red-marker.png'
                })
            })
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([lon, lat]),
        zoom: 4
    })
});

map.on('pointermove', function(evt) {
   var coords = ol.proj.toLonLat(evt.coordinate);
   var lat  = coords[1].toFixed(2);
   var lon = coords[0].toFixed(2);
   var locTxt = "Latitude: " + lat + " Longitude: " + lon;
   document.getElementById('coords').innerHTML = locTxt;
});
