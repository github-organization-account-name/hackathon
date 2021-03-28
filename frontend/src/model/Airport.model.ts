export default class Airport {
    id: string;
    lat: number;
    lon: number;
    name: string;
    score: number;

    constructor(id: string, lat: number, lon: number, name: string, score: number) {
        this.id = id;
        this.lat = lat;
        this.lon = lon;
        this.name = name;
        this.score = score;
    }
}

