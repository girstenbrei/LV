import React, { Component } from "react";

class DAT extends Component {
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


        console.log(event.target.value)
        if (this.props.data.required && event.target.value.length === 0) {
            validation_object = {valid: false, msg:"Das ist ein Pflichtfeld"};
        } else {
            validation_object = {valid: true, msg:""}
        }
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


    render() {
        return (
            <div key={this.props.i}>
                <input name={this.props.i}
                       type="date"
                       value={this.state.value}
                       onChange={this.handleChange}/>
                {this.renderValidation()}
            </div>
        );
    }
}

export default DAT;