var width = 1600
var height = 500

function plotFrance() {
    d3.json('../data/france.json', function (data) {
        var canvas = d3.select('.paths').select('svg')
        var centroid = d3.geoCentroid(data)
        var proj = d3.geoMercator().center(centroid).scale(4000).translate([width / 2, height / 2])
        var path = d3.geoPath().projection(proj)

        canvas.append('path')
            .datum(data)
            .attr('d', path)
            .attr('fill', 'blue')
            .attr('fill-opacity', 0.3)
    })
}

function getMinMaxSurvivors(minardData) {
    min = Number.MAX_VALUE
    max = Number.MIN_VALUE

    minardData.forEach(function (item, index, array) {
        survivors = parseInt(item.SURV)
        if (survivors < min) { min = survivors }

        if (survivors > max) { max = survivors }
    })

    return [min, max]
}

function getMinMaxTemp(minardData) {
    min = Number.MAX_VALUE
    max = 0

    minardData.forEach(function (item, index, array) {
        temp = parseInt(item.TEMP)
        if (temp < min) { min = temp }

        if (temp > max) { max = temp }
    })

    return [min, max]
}

function plotMinardsMap() {
    var journeyGeoJson = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '1',
                'direction': 'A',
                'survivors': 0,
                'temp': 0
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '1',
                'direction': 'R',
                'survivors': 0,
                'temp': 0
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '2',
                'direction': 'A',
                'survivors': 0,
                'temp': 0
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '2',
                'direction': 'R',
                'survivors': 0,
                'temp': 0
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '3',
                'direction': 'A',
                'survivors': 0,
                'temp': 0
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '3',
                'direction': 'R',
                'survivors': 0,
                'temp': 0
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'connection': '1',
                'survivors': 0,
                'temp': 0
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'connection': '2',
                'survivors': 0,
                'temp': 0
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'connection': '3',
                'survivors': 0,
                'temp': 0
            }
        }]
    }

    citiesGeoJson = {
        'type': 'FeatureCollection',
        'features': []
    }

    d3.json('../data/minard-data.json', function (d) {
        d.forEach(function (item, index, array) {
            // Create Cities points
            if (item.LATC != "" && item.LONC != "") {
                citiesGeoJson.features.push({
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [parseFloat(item.LONC), parseFloat(item.LATC)]
                    },
                    'properties': {
                        'name': item.CITY
                    }
                })
            }

            // Create Lines between points
            var feature = journeyGeoJson.features.find(function (obj) { return (obj.properties.division === item.DIV && obj.properties.direction === item.DIR) })
            feature.geometry.coordinates.push([
                parseFloat(item.LONP),
                parseFloat(item.LATP),
            ])

            feature.properties.survivors = parseInt(item.SURV);
            feature.properties.temp = parseInt(item.TEMP);

            // HACK for connecting the A and R lines
            if (index == 14) {
                feature = journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '1' })
                feature.geometry.coordinates.push(
                    [parseFloat(item.LONP), parseFloat(item.LATP)],
                    [parseFloat(array[index + 1].LONP), parseFloat(array[index + 1].LATP)]
                )

                feature.properties.survivors = parseInt(item.SURV);
                feature.properties.temp = parseInt(item.TEMP);
            }

            else if (index == 31) {
                feature = journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '2' })
                feature.geometry.coordinates.push(
                    [parseFloat(item.LONP), parseFloat(item.LATP)],
                    [parseFloat(array[index + 1].LONP), parseFloat(array[index + 1].LATP)]
                )

                feature.properties.survivors = parseInt(item.SURV);
                feature.properties.temp = parseInt(item.TEMP);
            }

            else if (index == 44) {
                feature = journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '3' })
                feature.geometry.coordinates.push(
                    [parseFloat(item.LONP), parseFloat(item.LATP)],
                    [parseFloat(array[index + 1].LONP), parseFloat(array[index + 1].LATP)]
                );

                feature.properties.survivors = parseInt(item.SURV);
                feature.properties.temp = parseInt(item.TEMP);
            }

        });

        // Get min max survivors and temperature for scaling
        surv = getMinMaxSurvivors(d)
        minSurv = surv[0]
        maxSurv = surv[1]
        temp = getMinMaxTemp(d)
        minTemp = temp[0]
        maxTemp = temp[1]

        var colorSurv = d3.interpolateRgb('#ff1e00', '#ff8400')

        var canvas = d3.select('.paths').append('svg')
            .attr('width', width)
            .attr('height', height);

        var centroidCities = d3.geoCentroid(citiesGeoJson);
        var projCities = d3.geoMercator().center(centroidCities).scale(4000).translate([width / 3, height / 2]);
        var pathCities = d3.geoPath().projection(projCities);

        var centroidJourney = d3.geoCentroid(journeyGeoJson);
        var projJourney = d3.geoMercator().center(centroidJourney).scale(4000).translate([width / 3, height / 2]);
        var pathJourney = d3.geoPath().projection(projJourney);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '1' && obj.properties.direction === 'A') }))
            .attr('d', pathJourney)
            .attr('stroke', function (d) { return colorSurv((d.properties.surv / maxSurv)) })
            .attr('stroke-width', 10)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '1' && obj.properties.direction === 'R') }))
            .attr('d', pathJourney)
            .attr('stroke', 'blue')
            .attr('stroke-dasharray', ('3', '3'))
            .attr('stroke-width', 10)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '2' && obj.properties.direction === 'A') }))
            .attr('d', pathJourney)
            .attr('stroke', 'orange')
            .attr('stroke-width', 6)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '2' && obj.properties.direction === 'R') }))
            .attr('d', pathJourney)
            .attr('stroke', 'orange')
            .attr('stroke-dasharray', ('3', '3'))
            .attr('stroke-width', 6)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '3' && obj.properties.direction === 'A') }))
            .attr('d', pathJourney)
            .attr('stroke', 'green')
            .attr('stroke-width', 6)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '3' && obj.properties.direction === 'R') }))
            .attr('d', pathJourney)
            .attr('stroke', 'green')
            .attr('stroke-dasharray', ('3', '3'))
            .attr('stroke-width', 6)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '1' }))
            .attr('d', pathJourney)
            .attr('stroke', 'blue')
            .attr('stroke-width', 10)
            .attr('fill-opacity', 0.0)

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '2' }))
            .attr('d', pathJourney)
            .attr('stroke', 'orange')
            .attr('stroke-width', 6)
            .attr('fill-opacity', 0.0)

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '3' }))
            .attr('d', pathJourney)
            .attr('stroke', 'green')
            .attr('stroke-width', 6)
            .attr('fill-opacity', 0.0)

        canvas.append('path')
            .datum(citiesGeoJson)
            .attr('d', pathCities)
            .attr('fill', 'blue');

        var label = canvas.selectAll('text')
            .data(citiesGeoJson.features)
            .enter()
            .append('text')
            .attr('transform', function (d) { return "translate(" + pathCities.centroid(d) + ")"; })
            .attr('dy', 7) // vertical offset
            .attr('dx', 5) // horizontal offset
            .text(function (d) { return d.properties.name; });
    });
}
