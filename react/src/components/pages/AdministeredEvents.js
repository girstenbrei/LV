import React, { Component } from "react";
import {Link} from "react-router-dom";
import EventCardsLayout from "../EventCardsLayout";

class AdministeredEvents extends Component {
    constructor(props) {
        super(props);

        this.state = {
            eventList : []
        };

        this.getEvents();
    }

    getEvents() {
        this.props.globalState.auth.fetch(this.props.globalState.url + '/api/administered_events')
            .then((response) => {
                this.setState({eventList: response});
            })
            .catch(err => alert(err));
    }

    renderEvents () {
        const listItems = this.state.eventList.map((event, i) =>
            <li>
                <Link to={"/administeredEvents/" + event.slug}>{event.name}</Link>
            </li>
        );
        return (
            <ul>{listItems}</ul>
        );
    }

    render() {
        return (
            <div>
                <div className="text-center">
                    <Link to={"/create/"}
                          className={`btn btn-primary`}
                          role="button">Neue Veranstaltung anlegen</Link>
                </div>

                <EventCardsLayout eventList={this.state.eventList} title={`Veranstaltungen verwalten`}
                                  hideLoginButton={false} showAdministrateButton={true}
                />
            </div>
        );
    }
}

export default AdministeredEvents;