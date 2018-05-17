import React, { Component } from "react";

class TXT extends Component {
    constructor(props) {
        super(props);
        this.state = {
            value: props.data.value || "",
            edited_once: false,
            validation_object: {valid:false, msg:""}
        };

        this.handleChange = this.handleChange.bind(this);
    }


    serializeData(data){
        return data;
    }

    handleChange(event) {
        let validation_object;
        if (this.props.data.required && event.target.value.length === 0) {
            validation_object = {valid: false, msg:"Das ist ein Pflichtfeld"};
        } else {
            validation_object = {valid: true, msg:""}
        }
        this.setState({value: event.target.value, edited_once: true, validation_object:validation_object});
        this.props.setValidationState(validation_object.valid, this.serializeData(event.target.value))
    }

    hasError() {
        return (!this.state.validation_object.valid && this.state.edited_once);
    }

    renderValidation() {
        if (this.hasError()) {
            return <small className="form-element-hint">{this.state.validation_object.msg}</small>;
        } else {
            return <span/>
        }
    }


    render() {
        return (
            <div key={this.props.i} className={`form-element form-textarea ${this.hasError() ? 'form-has-error' : ''}`}>

                <textarea
                    name={this.props.i}
                    id={`field-${this.props.data.i}`}
                    className="form-element-field" placeholder=" "
                    onChange={this.handleChange}
                    value={this.state.value}>
                    {this.props.data.value}
                    </textarea>

                <div className="form-element-bar"/>
                <label className="form-element-label" htmlFor={`field-${this.props.data.i}`}>{this.props.data.text}</label>

                {this.renderValidation()}
            </div>
        );
    }
}

export default TXT;