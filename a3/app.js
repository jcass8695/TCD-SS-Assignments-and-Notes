var express = require('express');
var http = require('http');
var request = require('request-promise')
var config = require('./config');
var fs = require('fs')

var app = express();

app.get('/', (request, response) => {
    response.send('Welcome')
});

app.get('/auth', (request, response) => {
    var url = 'https://accounts.spotify.com/authorize';
    var clientId = config.clientId;
    var responseType = 'code';
    var redirectUri = 'http://localhost:5050/callback';
    var scopes = encodeURIComponent('playlist-read-private playlist-read-collaborative')
    response.redirect(
        url +
        '/?' +
        'client_id=' + clientId + '&' +
        'response_type=' + responseType + '&' +
        'scope=' + scopes + '&' +
        'redirect_uri=' + redirectUri
    );
});

app.get('/callback', (request, response) => {
    authCode = request.query.code
    if (authCode == null) {
        console.log(request.query)
        response.send('No auth code was sent')
        return
    }
    return getAccessToken(authCode)
        .then(res => {
            accessToken = res.access_token;
            refreshToken = res.refresh_token;
            fs.writeFileSync('tokens.json', JSON.stringify(res))
            response.send('AccessToken: ' + accessToken + 'RefreshToken: ' + refreshToken)
        });
});

app.get('/refresh', (request, response) => {
    refreshToken = JSON.parse(fs.readFileSync('./tokens.json')).refresh_token
    return refreshAccessToken(refreshToken)
        .then(res => {
            accessToken = res
            fs.writeFile('tokens.json', JSON.stringify({
                access_token: accessToken,
                refresh_token: refreshToken
            }));
            response.send('Refreshed AccessToken: ' + accessToken + 'RefreshToken: ' + refreshToken)
        });
});

app.get('/artists', (request, response) => {
    accessToken = JSON.parse(fs.readFileSync('./tokens.json')).access_token;
    url = 'https://api.spotify.com/v1/users/eternal_atom/playlists/5nRAlBCYZlJlRJGZU2MaOM/tracks/?fields=items(track(artists(name,id))),next'
    // Tiers are lower: count is 1, middle: count is 2-10, upper: 11+
    return getArtists(accessToken, url, { 'artists': [] })
        .then(artistsNames => {
            return fs.writeFileSync('./artists.json', artistsNames)
        })
        .finally(() => {
            parseTiers();
            response.send('Parsed artists')
        })
});

app.listen(5050, () => {
    console.log('Spotify Vis app listening on port 5050')
});

function getArtists(accessToken, url, parsedArtists) {
    return request.get(url).auth(null, null, true, accessToken)
        .then(unparsedArtists => {
            nextUrl = parseArtists(unparsedArtists, parsedArtists)
            if (nextUrl != null) {
                return getArtists(accessToken, nextUrl, parsedArtists)
            } else {
                return JSON.stringify(parsedArtists);
            }
        });
};

function parseArtists(unparsedArtists, parsedArtists) {
    jsonObject = JSON.parse(unparsedArtists);
    itemsArray = jsonObject.items;
    for (var i = 0; i < itemsArray.length; i++) {
        artistsArray = itemsArray[i].track.artists
        for (var j = 0; j < artistsArray.length; j++) {
            var name = artistsArray[j].name;
            var id = artistsArray[j].id;
            var location = null;
            for (var k = 0; k < parsedArtists.artists.length; k++) {
                if (parsedArtists.artists[k].name === name) {
                    location = k;
                }
            }

            if (location != null) {
                parsedArtists.artists[location].count += 1;
            } else {
                parsedArtists.artists.push({
                    'name': name,
                    'id': id,
                    'count': 1
                });
            }
        }
    }
    if ('next' in jsonObject) {
        return jsonObject['next'];
    } else {
        return null;
    }
};

function getAccessToken(authCode) {
    var url = 'https://accounts.spotify.com/api/token';
    var clientId = config.clientId;
    var clientSecret = config.clientSecret;
    var form = {
        'grant_type': 'authorization_code',
        'code': authCode,
        'redirect_uri': 'http://localhost:5050/callback',
        'client_id': clientId,
        'client_secret': clientSecret
    };
    return request.post({ url: url, form: form })
        .then(body => {
            var bodyObject = JSON.parse(body);
            return {
                access_token: bodyObject.access_token,
                refresh_token: bodyObject.refresh_token
            }
        })
        .catch(err => {
            console.log(err)
        });
}

function refreshAccessToken(refreshToken) {
    var url = 'https://accounts.spotify.com/api/token';
    var clientId = config.clientId;
    var clientSecret = config.clientSecret;
    var form = {
        'grant_type': 'refresh_token',
        'refresh_token': refreshToken,
        'client_id': clientId,
        'client_secret': clientSecret
    };
    return request.post({ url: url, form: form })
        .then(body => {
            return JSON.parse(body).access_token;
        })
        .catch(err => {
            console.log(err)
        });
}

function parseTiers() {
    data = JSON.parse(fs.readFileSync('artists.json')).artists;
    tieredData = { 'tier1': [], 'tier2': [], 'tier3': [] };
    for (var i = 0; i < data.length; i++) {
        count = data[i].count;
        name = data[i].name;
        if (count == 1) {
            tieredData.tier1.push({ 'name': name, 'count': count });
        } else if (count > 1 && count <= 10) {
            tieredData.tier2.push({ 'name': name, 'count': count });
        } else {
            tieredData.tier3.push({ 'name': name, 'count': count });
        }
    }

    fs.writeFileSync('tiered.json', JSON.stringify(tieredData));
}
