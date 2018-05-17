import React, { Component } from "react";
import EventCard from "../EventCard";
import {Thumbnail} from "react-bootstrap";

class AdminEventDetail extends Component {
    constructor(props) {
        super(props);
        console.log(props);

        const {match: {params}} = props;


        this.state = {
            event : {},
            slug: params.slug,
            loaded: false
        };

        this.getEvent();
    }

    getEvent() {
        console.log(this.props)

        this.props.globalState.auth.fetch(this.props.globalState.url + '/api/event/' + this.state.slug + "/signup/")
            .then((response) => {

                let empty_states = new Array(response.question_sets.length);
                for (var i=0; i<empty_states.length; i++) {
                    empty_states[i] = false;
                }

                this.setState({event: response, loaded: true});
            })
            .catch(err => alert(err));
    }

    render() {
        if (!this.state.loaded) {
            return (
                <p>Loading...</p>
            )
        }
        return (
            <div className="container">
                <div className="row">
                    <div className="col-xs-12 col-sm-12 col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8">

                        <EventCard key="1" data={this.state.event.details} hideLoginButton={true}/>

                        <Thumbnail className="EventCard">
                            <h3>Details</h3>
                            <br/>
                            <p>ToDo: Anzahl Anmeldungen, Deadlines bearbeiten</p>
                            <a className="btn btn-info" href={`${this.props.globalState.url}/api/event/${this.state.slug}/download/`} target="_blank">Excel-Liste herunterladen</a>
                        </Thumbnail>

                        <Thumbnail className="EventCard">
                            <h3>Teilnehmerliste</h3>
                            <br/>
                            <p>ToDo: Empfangsbestätigung verschicken</p>
                        </Thumbnail>

                        <Thumbnail className="EventCard">
                            <h3>Staff</h3>
                            <br/>
                            <p>ToDo: Liste von Bearbeitern bearbeitbar machen</p>
                        </Thumbnail>


                    </div>
                </div>
            </div>
        );
    }
}

export default AdminEventDetail;