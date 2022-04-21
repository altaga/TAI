import React, { Component } from 'react';
import logo from './map.png';
import './App.css';
import { coords, stations } from './const.js';
import axios from 'axios';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stations: []
    };
  }

  componentDidMount() {
    let myStations = stations.map((station, i) => {
      let myTempJson = {};
      myTempJson.name = station.v_id;
      myTempJson.num = station.attributes.Num;
      myTempJson.line = station.attributes.Line;
      return myTempJson
    });
    this.setState({
      stations: myStations
    }, () => {
      var config = {
        headers: {
          'Authorization': 'Bearer token'
        }
      };
      const req1 = axios.get('https://d6ycw9o7ak.execute-api.us-east-1.amazonaws.com/get-passengers', config);
      const req2 = axios.get('https://d6ycw9o7ak.execute-api.us-east-1.amazonaws.com/get-risk-low', config);
      const req3 = axios.get('https://d6ycw9o7ak.execute-api.us-east-1.amazonaws.com/get-risk-med', config);
      const req4 = axios.get('https://d6ycw9o7ak.execute-api.us-east-1.amazonaws.com/get-risk-high', config);
      axios.all([req1, req2, req3, req4]).then(axios.spread((res1, res2, res3, res4) => {
        let temp = this.state.stations;
        res1.data.results.forEach(element => {
          temp.forEach(station => {
            if (element.to_id === station.name) {
              station[element["e_type"]] = element["attributes"]["Passengers"];
            }
          });
        })
        res2.data.results.forEach(element => {
          temp.forEach(station => {
            if (element.to_id === station.name) {
              station["Risk"] = element.from_id;
            }
          });
        })
        res3.data.results.forEach(element => {
          temp.forEach(station => {
            if (element.to_id === station.name) {
              station["Risk"] = element.from_id;
            }
          });
        })
        res4.data.results.forEach(element => {
          temp.forEach(station => {
            if (element.to_id === station.name) {
              station["Risk"] = element.from_id;
            }
          });
        })
        this.setState({
          stations: temp
        });
      }));
    });
  }

  componentWillUnmount() {

  }

  render() {
    return (
      <div>
        <img width="2281px" height="2794px" src={logo} alt="logo" useMap="#workmap" />
        {
          this.state.stations.length > 0 &&
          <map name="workmap">
            {
              coords.map(([x, y, w, h], i) => (
                <area id={"area" + i} onClick={() => {
                  alert("Station: " + this.state.stations[i].name + "\n" +
                    "Line: " + this.state.stations[i].line + "\n" +
                    "Risk Level: " + this.state.stations[i].Risk + "\n" +
                    "Morning_Passengers: " + this.state.stations[i]["Morning_Passengers"] + "\n" +
                    "Noon_Passengers: " + this.state.stations[i]["Noon_Passengers"] + "\n" +
                    "Afternoon_Passengers: " + this.state.stations[i]["Afternoon_Passengers"] + "\n"
                  )
                }} key={i} shape="rect" coords={`${x},${y},${w},${h}`} alt="work" style={{ cursor: "pointer" }} />
              ))
            }
          </map>
        }
      </div>
    );
  }
}

export default App;