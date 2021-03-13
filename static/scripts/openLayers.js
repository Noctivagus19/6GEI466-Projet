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
