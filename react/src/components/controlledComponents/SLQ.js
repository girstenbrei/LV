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

    renderValidation() {
        if (!this.state.validation_object.valid && this.state.edited_once) {
            return <span>{this.state.validation_object.msg}</span>
        } else {
            return <span/>
        }
    }


    renderOptions() {
        const choices = this.props.data.choices.split(",").map((choiceText, i) => {
                if (i === this.state.value) {
                    return <div key={'o' + i}>
                        <input name={this.props.data.i}
                               type="radio"
                               value={i}
                               onChange={this.handleChange}
                               checked/>
                        {choiceText}
                        <br/>
                    </div>
                } else {
                    return <div key={'o' + i}>
                        <input name={this.props.data.i}
                               type="radio"
                               value={i}
                               onChange={this.handleChange} />
                        {choiceText}<br/>
                    </div>
                }
            }
        );
        return (
            <div>{choices}</div>
        );
    }

    render() {
        return (
            <div key={this.props.i}>
                {this.renderOptions()}
                {this.renderValidation()}
            </div>
        );
    }
}

export default SLQ;