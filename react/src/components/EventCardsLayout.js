import React, { Component } from "react";
import EventCard from "./EventCard";

class EventCardsLayout extends Component {
    constructor(props) {
        super(props);
    }


    renderEvents () {
        const listItems = this.props.eventList.map((event, i) =>
            <EventCard key={i} data={event} hideLoginButton={this.props.hideLoginButton} showAdministrateButton={this.props.showAdministrateButton}/>
        );
        return (
            <div>{listItems}</div>
        );
    }

    render() {
        return (
            <div className="container">
                <div className="row">
                    <div className="col-xs-12 col-sm-12 col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8">
                        <div>
                            <h2>{this.props.title}</h2>
                            <br />
                        </div>
                        {this.renderEvents()}
                    </div>
                </div>
            </div>
        );
    }
}

export default EventCardsLayout;