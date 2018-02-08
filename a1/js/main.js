var width = 1600
var height = 500

function france() {
    d3.json('../data/france.json', function (data) {
        var canvas = d3.select('.paths').append('svg')
            .attr('width', width)
            .attr('height', height);

        var centroid = d3.geoCentroid(data)
        var proj = d3.geoMercator().center(centroid).scale(2000).translate([width / 2, height / 2])
        var path = d3.geoPath().projection(proj)

        canvas.append('path')
            .datum(data)
            .attr('d', path)
            .attr('fill', 'blue')
            .attr('fill-opacity', 0.3)
    })
}

function getCities() {
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
                'direction': 'A'
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '1',
                'direction': 'R'
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '2',
                'direction': 'A'
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '2',
                'direction': 'R'
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '3',
                'direction': 'A'
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'division': '3',
                'direction': 'R'
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'connection': '1'
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'connection': '2'
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            },
            'properties': {
                'connection': '3'
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

            // HACK
            if (index == 14) {
                console.log(item)
                feature = journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '1' })
                feature.geometry.coordinates.push(
                    [parseFloat(item.LONP), parseFloat(item.LATP)],
                    [parseFloat(array[index + 1].LONP), parseFloat(array[index + 1].LATP)]
                )
            }

            else if (index == 31) {
                console.log(item)
                feature = journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '2' })
                feature.geometry.coordinates.push(
                    [parseFloat(item.LONP), parseFloat(item.LATP)],
                    [parseFloat(array[index + 1].LONP), parseFloat(array[index + 1].LATP)]
                )
            }

            else if (index == 44) {
                console.log(item)
                feature = journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '3' })
                feature.geometry.coordinates.push(
                    [parseFloat(item.LONP), parseFloat(item.LATP)],
                    [parseFloat(array[index + 1].LONP), parseFloat(array[index + 1].LATP)]
                )
            }
        });

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
            .datum(citiesGeoJson)
            .attr('d', pathCities)
            .attr('fill', 'blue');

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '1' && obj.properties.direction === 'A') }))
            .attr('d', pathJourney)
            .attr('stroke', 'blue')
            .attr('stroke-width', 6)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '1' && obj.properties.direction === 'R') }))
            .attr('d', pathJourney)
            .attr('stroke', 'blue')
            .attr('stroke-dasharray', ('3', '3'))
            .attr('stroke-width', 6)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '2' && obj.properties.direction === 'A') }))
            .attr('d', pathJourney)
            .attr('stroke', 'orange')
            .attr('stroke-width', 3)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '2' && obj.properties.direction === 'R') }))
            .attr('d', pathJourney)
            .attr('stroke', 'orange')
            .attr('stroke-dasharray', ('3', '3'))
            .attr('stroke-width', 3)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '3' && obj.properties.direction === 'A') }))
            .attr('d', pathJourney)
            .attr('stroke', 'green')
            .attr('stroke-width', 3)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return (obj.properties.division === '3' && obj.properties.direction === 'R') }))
            .attr('d', pathJourney)
            .attr('stroke', 'green')
            .attr('stroke-dasharray', ('3', '3'))
            .attr('stroke-width', 3)
            .attr('fill-opacity', 0.0);

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '1' }))
            .attr('d', pathJourney)
            .attr('stroke', 'blue')
            .attr('stroke-width', 6)
            .attr('fill-opacity', 0.0)

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '2' }))
            .attr('d', pathJourney)
            .attr('stroke', 'orange')
            .attr('stroke-width', 3)
            .attr('fill-opacity', 0.0)

        canvas.append('path')
            .datum(journeyGeoJson.features.find(function (obj) { return obj.properties.connection === '3' }))
            .attr('d', pathJourney)
            .attr('stroke', 'green')
            .attr('stroke-width', 3)
            .attr('fill-opacity', 0.0)

        canvas.selectAll('path')
            .data(citiesGeoJson.features)
            .enter()
            .append('text')
            .attr('transform', function (d) {
                return 'translate(' + projCities(d.geometry.coordinates) + ')';
            })
            .attr('dy', -3) // vertical offset
            .attr('dx', 3) // horizontal offset
            .text(function (d) {
                return d.properties.name
            })
    });
}
