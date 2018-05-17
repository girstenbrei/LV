import React, { Component } from "react";

class SLQ extends Component {
    constructor(props) {
        super(props);

        this.state = {
            value: parseInt(props.data.value, 10) | -1,
            edited_once: false,
            validation_object: {valid:false, msg:""}
        };

        this.handleChange = this.handleChange.bind(this);
    }

    serializeData(data){
        return data.toString();
    }

    handleChange(event) {
        let validation_object = {valid: true, msg:""}

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


    renderOptions() {
        const choices = this.props.data.choices.split(",").map((choiceText, i) => {
                if (i === this.state.value) {
                    return <label key={'o' + i}
                                  className={`form-radio-label`}>
                        <input name={this.props.data.i}
                               className={`form-radio-field`}
                               type="radio"
                               value={i}
                               onChange={this.handleChange}
                               checked/>
                        <i className="form-radio-button"/>
                        <span>{choiceText}</span>
                        <br/>
                    </label>
                } else {
                    return <label key={'o' + i}
                                  className={`form-radio-label`}>
                        <input name={this.props.data.i}
                               className={`form-radio-field`}
                               type="radio"
                               value={i}
                               onChange={this.handleChange} />
                        <i className="form-radio-button"/>
                        <span>{choiceText}</span>
                    </label>
                }
            }
        );
        return (
            <div>{choices}</div>
        );
    }

    render() {
        return (
            <div key={this.props.i} className={`form-radio form-radio-inline ${this.hasError() ? 'form-has-error' : ''}`}>
                <div className="form-radio-legend">{this.props.data.text}</div>
                {this.renderOptions()}
                {this.renderValidation()}
            </div>
        );
    }
}

export default SLQ;