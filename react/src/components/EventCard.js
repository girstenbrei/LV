import React, { Component } from "react";
import {Link} from "react-router-dom";
import {Thumbnail} from "react-bootstrap";


class EventCard extends Component {
    constructor(props) {
        super(props);

        this.state = {

        };

    }

    render() {
        return (
            <Thumbnail src="http://lorempixel.com/242/200" alt="242x200">
                <h3>{this.props.data.name}</h3>
                <p>{this.props.data.description}</p>
                <p>{this.props.data.start_datetime}</p>
                <p>{this.props.data.end_datetime}</p>
                <p>{this.props.data.signup_from}</p>
                <p>{this.props.data.signup_to}</p>
                <p>{this.props.data.slug}</p>
                <p>
                    <Link to={"/publicEvents/" + this.props.data.slug}>Anmelden</Link>
                </p>
            </Thumbnail>
        );
    }
}

export default EventCard;