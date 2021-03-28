export default class Airport {
    id: string;
    lat: number;
    lon: number;
    name: string;

    constructor(id: string, lat: number, lon: number, name: string) {
        this.id = id;
        this.lat = lat;
        this.lon = lon;
        this.name = name;
    }
}

