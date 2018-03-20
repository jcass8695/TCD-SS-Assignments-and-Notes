var express = require('express');
var http = require('http');
var request = require('request-promise')
var config = require('./config');
var fs = require('fs')

var app = express();

app.get('/', (request, response) => {
    authCode = request.query.code
    refreshToken = null
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
            fs.writeFileSync('tokens.json', JSON.stringify({
                access_token: accessToken,
                refresh_token: refreshToken
            }));
            response.send('Refreshed AccessToken: ' + accessToken + 'RefreshToken: ' + refreshToken)
        });
})

app.listen(5050, () => {
    console.log('Spotify Vis app listening on port 5050')
});

function getAccessToken(authCode) {
    var url = 'https://accounts.spotify.com/api/token';
    var clientId = config.clientId;
    var clientSecret = config.clientSecret;
    var form = {
        'grant_type': 'authorization_code',
        'code': authCode,
        'redirect_uri': 'http://localhost:5050',
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
