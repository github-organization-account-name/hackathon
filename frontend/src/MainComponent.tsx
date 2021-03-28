import {
    Streamlit,
    StreamlitComponentBase,
    withStreamlitConnection
} from "streamlit-component-lib";
import React, { ReactNode, Fragment, useState, useEffect } from "react";
import Airport from './model/Airport.model';
import Map from './MapComponent';
import { plainToClass } from "class-transformer";


interface State {
    airports: Airport
}

class MainComponent extends StreamlitComponentBase {

    public state = {
        isLoading: true,
        isCountryLoading: true,
        airports: [],
        countries: [],
    }

    componentDidMount = async () => {
        const countryData = this.props.args['key'];
        // const obj = JSON.parse(countryData);
        let res = countryData.split('\n');
        res.shift();
        let countryOptions: Object[] = [];
        res.forEach((element: string) => {
            countryOptions.push({
                "text": element.trimStart(),
                "key": element.trimStart(),
                "value": element.trimStart(),
            });
        });
        this.setState({ countries: countryOptions, isCountryLoading: false });
    }

    public render = (): ReactNode => {

        return (
            <div>
                {!this.state.isCountryLoading &&
                    <Map mapType={google.maps.MapTypeId.ROADMAP} mapTypeControl={true} countries={this.state.countries}></Map>
                }
            </div>
        )
    }
}

export default withStreamlitConnection(MainComponent)

