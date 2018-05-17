import React, { Component } from "react";

import EventCardsLayout from "../EventCardsLayout";

class PublicEvents extends Component {
    constructor(props) {
        super(props);

        this.state = {
            eventList : []
        };

        this.getEvents();
    }

    getEvents() {
        this.props.globalState.auth.fetch(this.props.globalState.url + '/api/event/')
            .then((response) => {
                this.setState({eventList: response});
            })
            .catch(err => alert(err));
    }

    render() {
        return (
            <div>
                <EventCardsLayout eventList={this.state.eventList} title={`Öffentliche Veranstaltungen`} />
            </div>
        );
    }
}

export default PublicEvents;