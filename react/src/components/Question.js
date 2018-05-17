import React, { Component } from "react";

import CHR from "./controlledComponents/CHR";
import MAL from "./controlledComponents/MAL";
import TME from "./controlledComponents/TME";
import DAT from "./controlledComponents/DAT";
import TXT from "./controlledComponents/TXT";
import SLQ from "./controlledComponents/SLQ";
import MLQ from "./controlledComponents/MLQ";


class Question extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isValid:false
        };

        this.setValidationState = this.setValidationState.bind(this);
    }

    setValidationState(isValid, serialized_data) {
        this.setState({isValid: isValid, serialized_data:serialized_data});
        this.props.setValidationState(this.props.i, isValid, serialized_data)
    }

    renderQuestionField() {

        this.props.data.i = this.props.i;

        switch(this.props.data.type) {
            case "MAL": // email
                return <MAL data={this.props.data} setValidationState={this.setValidationState} />;
            case "TME": // time
                return <TME data={this.props.data} setValidationState={this.setValidationState} />;
            case "DAT": // date
                return <DAT data={this.props.data} setValidationState={this.setValidationState} />;
            case "TXT": // textarea
                return <TXT data={this.props.data} setValidationState={this.setValidationState} />;
            case "CHR": // input type text
                return <CHR data={this.props.data} setValidationState={this.setValidationState} />;
            case "SLQ": // single choice
                return <SLQ data={this.props.data} setValidationState={this.setValidationState} />;
            case "MLQ": // multiple choice
                return <MLQ data={this.props.data} setValidationState={this.setValidationState} />;
            default:
                return this.renderDefault();
        }
    }

    renderDefault() {
        return(
            <p>Fehlendes Type-Template beim Rendern!</p>
        );
    }

    render() {
        return (
            <div key={this.props.i}>
                <p>{this.props.data.required}</p>
                {this.renderQuestionField()}

            </div>
        );
    }
}

export default Question;