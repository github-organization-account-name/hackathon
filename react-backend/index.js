const express = require('express'),
    bodyParser = require('body-parser'),
    port = process.env.port || 3030,
    tgjs = require('tigergraph.js'),
    cred = require('./config');
const app = express();

app.use(bodyParser.json());
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', "*");
    res.setHeader('Access-Control-Allow-Headers', "Origin, X-Request-With, Content-Type, Accept, Authorization");
    res.setHeader('Access-Control-Allow-Methods', "GET, POST, DELETE, PUT, PATCH, OPTIONS");
    next();
});

tgconn = new tgjs.createTigerGraphConnection("graph.i.tgcloud.io", "MyGraph", "tigergraph", cred.PASSWORD, cred.SECRET, cred.TOKEN);

app.use("/getAirportsByCountry/:country", async (req, res, next) => {
    let country = req.params.country;
    country = country.replace(/ /g, '%20');
    let params = { "country": country }
    tgconn.runQuery("dc_by_country", params, data => {
        let airports = [];
        console.log(data);
        if (!data[0]['error']) {
            data = data[0]['@@topScores'];
            data.forEach(element => {
                airport = { "id": element['Vertex_ID'], 'name': element['name'], 'lat': element['lat'], 'lon': element['lng'], 'score': element['score'] };
                airports.push(airport);
            });
            res.json(airports);
        }
        else {
            next(new Error("Something went wrong,"));
        }
    })
});

app.use("/getWeightedShortestPath/:start&:terminal", async (req, res, next) => {
    let source = req.params.start;
    let terminal = req.params.terminal;
    console.log(source);
    console.log(terminal);
    let params = { "source": source, "terminal": terminal }
    tgconn.runQuery("shortest_path_weighted", params, data => {
        let airports = [];
        if (data[0]) {
            data = data[0]['total'];
            console.log(data);
            if (data.length == 0) {
                res.json([]);
            }
            else {
                data = data[0];
                data = data['attributes'];
                let distance = data['total.@minPath.top().dist'];
                paths = data['total.@path'];
                paths.forEach(element => {
                    airport = { "id": element['id'], 'name': element['name'], 'lat': element['lat'], 'lon': element['lon'] };
                    airports.push(airport);
                });
                let response = { "distance": distance, 'paths': airports }
                res.json(response);
            }
        }
        else {
            next(new Error("Something went wrong,"));
        }
    })
});



app.listen(port);


