var width = 1600
var height = 500

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
        'features': []
    }

    citiesGeoJson = {
        'type': 'FeatureCollection',
        'features': []
    }

    d3.json('../data/minard-data.json', function (d) {
        // Get min max survivors for scaling
        surv = getMinMaxSurvivors(d)
        minSurv = surv[0]
        maxSurv = surv[1]
        temp = getMinMaxTemp(d)
        minTemp = temp[0]
        maxTemp = temp[1]
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

            if (index < array.length - 1) {
                journeyGeoJson.features.push({
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': [[parseFloat(item.LONP), parseFloat(item.LATP)], [parseFloat(array[index + 1].LONP), parseFloat(array[index + 1].LATP)]]
                    },
                    'properties': {
                        'div': item.DIV,
                        'dir': item.DIR,
                        'surv': item.SURV,
                        'temp': item.TEMP
                    }
                })
            }
        });

        var canvas = d3.select('.paths').append('svg')
            .attr('width', width)
            .attr('height', height);

        var colorScale = d3.interpolateRgb('blue', '#AFDAFF')

        var centroidCities = d3.geoCentroid(citiesGeoJson);
        var projCities = d3.geoMercator().center(centroidCities).scale(4000).translate([width / 3, height / 2]);
        var pathCities = d3.geoPath().projection(projCities);

        var centroidJourney = d3.geoCentroid(journeyGeoJson);
        var projJourney = d3.geoMercator().center(centroidJourney).scale(4000).translate([width / 3, height / 2]);
        var pathJourney = d3.geoPath().projection(projJourney);

        canvas.selectAll('path')
            .data(journeyGeoJson.features)
            .enter()
            .append('path')
            .attr('d', pathJourney)
            .attr('stroke', function (d) {
                var division = d.properties.div
                var temp = d.properties.temp == '' ? minTemp : d.properties.temp
                if (division === '1') return colorScale(temp / minTemp)

                else if (division === '2') return 'orange'

                else return 'green'
            })
            .attr('stroke-width', function (d) {
                var survivors = parseInt(d.properties.surv)
                if (d.properties.div === '1') return (15 * survivors / 340000)

                else if (d.properties.div === '2') return (8 * survivors / 60000)

                else return (8 * survivors / 22000)
            })
            .attr('stroke-dasharray', function (d) {
                if (d.properties.dir === 'R') return [3, 3]

                else return null
            })
            .attr('stroke-opacity', 0.75)
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

function basicShapes() {
    var canvas = d3.select('.basic-shapes').append('svg')
        .attr('width', width)
        .attr('height', height)

    var centres = [[40, 40], [160, 160], [280, 280], [160, 40], [40, 280], [280, 160]]
    var lineGenerator = d3.line().curve(d3.curveCardinal);
    var arcGenerator = d3.arc();
    arcGenerator
        .innerRadius(20)
        .outerRadius(100)

    canvas.selectAll('circle')
        .data(centres)
        .enter()
        .append('circle')
        .attr('cy', function (d) { return d[1] })
        .attr('cx', function (d) { return d[0] })
        .attr('r', function (d) { return 50 * Math.random() + 5 })
        .attr('stroke', 'red')
        .attr('stroke-width', 5)
        .attr('fill', 'blue')
        .attr('fill-opacity', Math.random())
        .attr('transform', 'translate(' + 500 + ',' + 100 + ')')
    canvas.selectAll('rect')
        .data([[100, -1], [100, 1]])
        .enter()
        .append('rect')
        .attr('width', d => d[0])
        .attr('height', d => d[0])
        .attr('fill', 'orange')
        .attr('fill-opacity', d => Math.random())
        .attr('transform', (d, i) => `translate(${d[1] * 300 + 660 - i * d[0]}, ${250}) rotate(${360 * Math.random()}, ${d[0] / 2}, ${d[0] / 2})`)

    canvas.selectAll('path')
        .data(centres)
        .enter()
        .append('path')
        .attr('d', lineGenerator(centres))
        .attr('stroke', 'green')
        .attr('stroke-width', 5)
        .attr('fill', 'none')
        .attr('fill-opacity', Math.random())
        .attr('transform', 'translate(' + 500 + ',' + 100 + ')')

    canvas.selectAll('g')
        .data([[0.125, 0.875]])
        .enter()
        .append('path')
        .attr('d', function (d) {
            console.log(d)
            return arcGenerator({
                startAngle: d[0] * 2 * Math.PI,
                endAngle: d[1] * 2 * Math.PI,
            });
        })
        .attr('transform', 'translate(' + (500 + 160) + ',' + (100 + 160) + ')')
        .attr('fill', 'orange')
        .attr('fill-opacity', 0.6)
}
