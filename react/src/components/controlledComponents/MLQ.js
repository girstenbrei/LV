import React, { Component } from "react";

class MLQ extends Component {
    constructor(props) {
        super(props);

        this.choices = this.props.data.choices.split(",");

        this.state = {
            selected_indices: this.prepareValues(),
            value: props.data.value,
            edited_once: false,
            validation_object: {valid:false, msg:""}
        };

        this.handleChange = this.handleChange.bind(this);
    }

    serializeData(data){
        var filtered_choices = Object.keys(data).reduce(function (filtered, key) {
            if (data[key]) filtered[key] = data[key];
            return filtered;
        }, {});
        return Object.keys(filtered_choices).join(',');
    }

    prepareValues() {
        let values = {};
        for (let i=0; i<this.choices.length; i++) {
            values[i] = false;
        }

        if(this.props.data.value) {
            this.props.data.value.split(",").map((key, i) => {
                values[parseInt(key, 10)] = true; return null;
            });
        }

        return values;
    }

    updateValues(index) {
        let selected_indices = Object.assign({}, this.state.selected_indices);
        selected_indices[index] = !selected_indices[index];

        return selected_indices;

    }


    handleChange(event) {

        let validation_object;
        validation_object = {valid: true, msg:""}

        console.log(event.target.value)

        this.setState({
            value: event.target.value,
            edited_once: true,
            selected_indices: this.updateValues(event.target.value),
            validation_object:validation_object
        });
        this.props.setValidationState(validation_object.valid, this.serializeData(this.updateValues(event.target.value)))
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
        const renderChoices = this.props.data.choices.split(",").map((choiceText, i) => {
                if (i === this.state.selected_index) {
                    return <label key={'o' + i} className="form-checkbox-label">
                                <input name={this.props.data.i}
                                       className="form-checkbox-field"
                                   type="checkbox"
                                   value={i}
                                   onChange={this.handleChange}
                                   checked/>
                                    <i className="form-checkbox-button"></i>
                                    <span>{choiceText}</span>
                            </label>
                } else {
                    return (
                        <label key={'o' + i} className="form-checkbox-label">
                            <input name={this.props.data.i}
                                   className="form-checkbox-field"
                                   type="checkbox"
                                   value={i}
                                   onChange={this.handleChange}
                                   />
                            <i className="form-checkbox-button"></i>
                            <span>{choiceText}</span>
                        </label>
                    )
                }
            }
        );
        return (
            <div>{renderChoices}</div>
        );
    }

    render() {
        return (
            <div key={this.props.i} className={`form-radio form-radio-inline ${this.hasError() ? 'form-has-error' : ''}`}>
                <div className="form-checkbox-legend">{this.props.data.text}</div>
                {this.renderOptions()}
                {this.renderValidation()}
            </div>
        );
    }
}

export default MLQ;