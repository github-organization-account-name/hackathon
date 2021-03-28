import React, { useEffect, useRef, useState, Fragment } from 'react';
import './Map.css';
import Airport from './model/Airport.model';
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';
import { plainToClass } from "class-transformer";
import { Button, Input, CircularProgress, Card, Grid, InputLabel, Paper } from '@material-ui/core';
import { Alert } from '@material-ui/lab';

interface IMap {
    mapType: google.maps.MapTypeId,
    mapTypeControl?: boolean,
    countries: string[],
    // airports: Airport[],
    // message: string,
}

type GoolgeLatLng = google.maps.LatLng;
type GoogleMap = google.maps.Map;
type GoogleMarker = google.maps.Marker;

const Map: React.FC<IMap> = ({ mapType, mapTypeControl = false, countries }) => {
    const ref = useRef<HTMLDivElement>(null);
    const [map, setMap] = useState<GoogleMap>();
    const [points, setPoints] = useState<Airport[]>([]);
    const [markers, setMarkers] = useState<GoogleMarker[]>([]);
    const [locationInfo, setLocationInfo] = useState<Airport>();
    const [start, setStart] = useState<Airport>();
    const [terminal, setTerminal] = useState<Airport>();
    const [paths, setPaths] = useState<Airport[]>([]);
    const [isLoading, setIsLoanding] = useState(true);
    const [error, setError] = useState("");
    const [distance, setDistance] = useState(0);
    const bounds = new google.maps.LatLngBounds();
    const baseUrl = "http://localhost:3030/";


    //init map
    const startMap = (): void => {
        if (!map) {
            defaultMap();
        }
    };
    useEffect(startMap, [map]);

    //set default map
    const defaultMap = (): void => {
        let latitude = 45.67;
        let longitude = 13.369;
        const defaultAddress = new google.maps.LatLng(latitude, longitude);
        initMap(5, defaultAddress);
    };

    const initMap = (zoomLevel: number, address: GoolgeLatLng): void => {
        if (ref.current) {
            setIsLoanding(false);
            setMap(
                new google.maps.Map(ref.current, {
                    zoom: zoomLevel,
                    center: address,
                    mapTypeControl: mapTypeControl,
                    streetViewControl: false,
                    zoomControl: true,
                    mapTypeId: mapType,
                })
            );
        }
    };

    //marker click event, show marker's airport info
    const markerClickEvent = (): void => {
        if (markers) {
            markers.map(marker => {
                marker.addListener('click', function (e) {
                    setLocationInfo({ id: marker.get("id"), name: marker.get("name"), lat: marker.get('lat'), lon: marker.get('lon'), score: marker.get('score') });
                });
            });
        }
    };
    useEffect(markerClickEvent, [markers]);

    //map click event, when click map, location info window hide
    const mapClickEvent = (): void => {
        if (map) {
            google.maps.event.addListener(map, 'click', function () {
                setLocationInfo(undefined);
            });
        }
    };
    useEffect(mapClickEvent, [map]);

    //when points change, draw marker on map
    const addMarkers = (): void => {
        if (points) {
            points.map(marker => {
                addMarker(marker);
            });
            map?.fitBounds(bounds);
            map?.panToBounds(bounds);
        }
    };
    const addMarker = (airport: Airport): void => {
        const position = new google.maps.LatLng(airport.lat, airport.lon);
        const marker: GoogleMarker = new google.maps.Marker({
            position: position,
            map: map,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                fillColor: 'red',
                fillOpacity: 0.5,
                strokeColor: '#00A',
                strokeOpacity: 0.7,
                strokeWeight: 1,
                scale: airport.score > 16 ? Math.pow(airport.score, 0.5) : 4,
            }
        });
        bounds.extend(position);
        marker.setValues({ "id": airport.id, "name": airport.name, 'lat': airport.lat, 'lon': airport.lon, 'score': airport.score });
        setMarkers(oldMarkers => [...oldMarkers, marker]);
    };
    useEffect(addMarkers, [points]);

    //clear previous markers on map
    const clearMarkers = (): void => {
        markers.map(marker => {
            marker.setMap(null);
        })
    }

    const clearPaths = (): void => {
        setPaths([]);
    }

    //when dropdown change
    const onCountryChange = async (e: any) => {
        const response = await fetch(baseUrl + 'getAirportsByCountry/' + e.value, {
            method: 'GET',
            headers: {},
        });
        const resData = await response.json();
        const airportsData = plainToClass(Airport, resData);
        clearMarkers();
        clearPaths();
        setPoints(airportsData);
    }

    //set start button click event
    const onStartClick = (info: Airport) => {
        setStart(info);
        setLocationInfo(undefined);
    }

    //terminal button click event
    const onTerminalClick = (info: Airport) => {
        setTerminal(info);
        setLocationInfo(undefined);
    }

    const onSearchBtnClick = async () => {
        //check whether source or terminal is defined
        if (start === undefined || terminal === undefined) {
            setError("Please select a start point or a terminal!")
            return;
        }
        console.log(start.id === terminal.id);
        if (start.id === terminal.id) {
            setError("Start point and terminal are same!");
            return;
        }
        setIsLoanding(true);
        const params = start.id.replace('/', '%2F') + "&" + terminal.id.replace('/', '%2F');
        const response = await fetch(baseUrl + 'getWeightedShortestPath/' + params, {
            method: 'GET',
            headers: {},
        });
        const resData = await response.json();
        console.log(resData);
        if (resData.length === 0) {
            console.log("no paths");
            setError("No path found!")
            setIsLoanding(false);
            return;
        }
        setError("");
        let distance = resData['distance'];
        let path = plainToClass(Airport, resData['paths']);
        clearMarkers();
        clearPaths();
        if (start.id !== path[0].id) {
            path.unshift(start);
        }
        setPoints(path);
        setPaths(path);
        setDistance(distance);
        setIsLoanding(false);
    }

    //draw flight route on map
    const drawLine = (): void => {
        let coordinates: google.maps.LatLng[] = [];
        if (paths.length !== 0 && map !== undefined) {
            console.log(paths);
            //add all paths' coordinates into an array
            paths.forEach(path => {
                coordinates.push(new google.maps.LatLng({ "lat": path.lat, "lng": path.lon }));
            });
            //draw every route on map
            for (let i = 0; i < coordinates.length - 1; i++) {
                let line = new google.maps.Polyline({
                    path: coordinates.slice(i, i + 2),
                    geodesic: true,
                    strokeColor: "#FF000",
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    icons: [
                        {
                            icon: { path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW },
                            offset: "100%",
                        },
                    ],
                });
                line.setMap(map);
            }
        }
    }
    useEffect(drawLine, [paths]);

    const onNoPathClose = (): void => {
        setError("");
    }

    return (
        <Fragment>
            <div className="container">
                {isLoading && <div className="loadingbg"></div>}
                <div className="card-container">
                    <Card className='card'>
                        <Grid container spacing={6}>
                            <Grid item xs={4}>
                                <InputLabel>Start</InputLabel>
                                <Input value={start !== undefined ? start.id : ""} placeholder='From' type='text' required={true}></Input>
                            </Grid>
                            <Grid item xs={4}>
                                <InputLabel>Terminal</InputLabel>
                                <Input value={terminal !== undefined ? terminal.id : ''} placeholder='To' type='text' required={true}></Input>
                            </Grid>
                            <Grid item xs={4}>
                                <Button variant="contained" onClick={onSearchBtnClick}>Search A Path</Button>
                            </Grid>
                            <p>Note: Please click spotted airport on the map to select starter or terminal.</p>
                        </Grid>
                    </Card>
                </div>
                {error != "" &&
                    <div className="alert-container">
                        <Alert severity="error" onClose={onNoPathClose}>{error}</Alert>
                    </div>
                }
                {paths.length !== 0 &&
                    <div className="path_container">
                        <Grid container spacing={3}>
                            <Grid item xs={12}>
                                <Paper className="paper">Path:
                                {paths.map(path => {
                                    if (path !== paths[paths.length - 1]){
                                        return <span>{path.id} --</span>
                                    }
                                    else {
                                        return <span>{path.id}</span>
                                    }
                                })}
                                </Paper>
                            </Grid>
                            <Grid item xs={12}>
                                <Paper className="paper">Distance: {distance} miles</Paper>
                            </Grid>
                        </Grid>
                    </div>
                }
                <div style={{ height: '600px', width: '100%' }}>
                    {isLoading &&
                        <div className="spinner-container">
                            <CircularProgress className="spinner" />
                        </div>
                    }
                    {!isLoading &&
                        <Dropdown className="dropdown" options={countries} onChange={onCountryChange} placeholder='Select a country:'></Dropdown>
                    }
                    <div ref={ref} className="map-container__map">
                        {locationInfo &&
                            <div className="location-info">
                                <h2>Airport Info</h2>
                                <ul>
                                    <li>ID: <strong>{locationInfo.id}</strong></li>
                                    <li>Name: <strong>{locationInfo.name}</strong></li>
                                    <li>Outdegree: <strong>{locationInfo.score}</strong></li>
                                </ul>
                                <button onClick={() => onStartClick(locationInfo)}>Set Start</button>
                                <button onClick={() => onTerminalClick(locationInfo)}>Set Terminal</button>
                            </div>
                        }
                    </div>
                </div>
            </div>
        </Fragment >
    );
};

export default Map;