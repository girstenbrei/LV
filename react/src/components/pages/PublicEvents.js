import React, { Component } from "react";
import EventCard from "../EventCard";

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

    renderEvents () {
        const listItems = this.state.eventList.map((event, i) =>
            <EventCard key={i} data={event}/>
        );
        return (
            <div>{listItems}</div>
        );
    }

    render() {
        return (
            <div>
                <h2>PublicEvents</h2>
                {this.renderEvents()}
            </div>
        );
    }
}

export default PublicEvents;