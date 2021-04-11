function checkCrossMeridian(points){
    pointsToRender = []

     for (var i = 0; i < points.length; i++) {
     pointsToRender.push(points[i]);
        if (typeof points[i+1] != 'undefined'){
            var startPoint = points[i];
            var endPoint = points[i+1];

            if (Math.abs(startPoint[0]-endPoint[0]) > 180) {
                var midY = (startPoint[1] + endPoint[1]) / 2

                var temp_endpoint = [startPoint[0], midY];
                var temp_startpoint = [startPoint[0], midY];

                if (startPoint[0] < endPoint[0]) {
                    temp_endpoint[0] = -180;
                    temp_startpoint[0] = 180;
                } else {
                    temp_endpoint[0] = 180;
                    temp_startpoint[0] = -180;
                }

                 pointsToRender.push(temp_endpoint);
                 drawTrajectory(pointsToRender);
                 pointsToRender = [];
                 pointsToRender.push(temp_startpoint);
            }
        }
    }
    drawTrajectory(pointsToRender);
}


function drawTrajectory(points){

    for (var i = 0; i < points.length; i++) {
        points[i] = ol.proj.transform(points[i], 'EPSG:4326', 'EPSG:3857');
    }

    var featureLine = new ol.Feature({
        geometry: new ol.geom.LineString(points)
    });

    var vectorLine = new ol.source.Vector({});
    vectorLine.addFeature(featureLine);

    var vectorLineLayer = new ol.layer.Vector({
        source: vectorLine,
        style: new ol.style.Style({
            fill: new ol.style.Fill({ color: '#ff1100', weight: 4 }),
            stroke: new ol.style.Stroke({ color: '#ff1100', width: 2 })
        })
    });

    map.addLayer(vectorLineLayer);
}

