import React, { Component } from "react";
import {Link} from "react-router-dom";
import {ButtonToolbar, Thumbnail} from "react-bootstrap";

import './styles/EventCard.css'


class EventCard extends Component {
    constructor(props) {
        super(props);

        this.state = {

        };

        this.date_format_options = { weekday: 'short', year: 'numeric', month: 'long', day: 'numeric' };
    }

    formatDate(date_string) {
        return new Date(date_string).toLocaleDateString('de-DE', this.date_format_options)
    }

    laysInPast(date_string) {
        return (Date.parse(date_string)-Date.parse(new Date())<0);
    }

    registrationIsPossible() {
        return !this.laysInPast(this.props.data.signup_to);
    }

    render() {
        return (
            <Thumbnail className="EventCard">
                <h3>{this.props.data.name}</h3>
                <p className={`EventCard-description`}>{this.props.data.description}</p>
                <br/>
                <p>
                    <span className="glyphicon glyphicon-time" aria-hidden="true"/>
                    &nbsp; Veranstaltung:
                    &nbsp; {this.formatDate(this.props.data.start_datetime)} - {this.formatDate(this.props.data.end_datetime)}
                </p>
                <p>
                    <span className="glyphicon glyphicon glyphicon-edit" aria-hidden="true"/>
                    &nbsp; Anmeldung:
                    &nbsp; {this.formatDate(this.props.data.signup_from)} - {this.formatDate(this.props.data.signup_to)}
                </p>
                <ButtonToolbar>
                {!this.props.hideLoginButton &&
                        <Link to={"/publicEvents/" + this.props.data.slug}
                              className={`btn btn-primary ${this.registrationIsPossible() ? 'active' : 'disabled'}`}
                              role="button">Anmelden</Link>
                }
                {this.props.showAdministrateButton &&
                        <Link to={"/administeredEvents/" + this.props.data.slug}
                              className={`btn btn-primary `}
                              role="button">Verwalten</Link>
                }
                </ButtonToolbar>
            </Thumbnail>
        );
    }
}

export default EventCard;