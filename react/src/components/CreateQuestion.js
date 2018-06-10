import React, { Component } from "react";
import {Button, ButtonGroup, ButtonToolbar} from "react-bootstrap";
import CHR from "./controlledComponents/CHR";
import MAL from "./controlledComponents/MAL";
import TME from "./controlledComponents/TME";
import DAT from "./controlledComponents/DAT";
import TXT from "./controlledComponents/TXT";
import SLQ from "./controlledComponents/SLQ";
import MLQ from "./controlledComponents/MLQ";

class CreateQuestion extends Component {
    constructor(props) {
        super(props);

        this.state = {
            text: props.data.text || "",
            type: props.data.type || "CHR",
            choices: props.data.choices || '',
            edited_once: false,
            validation_object: {valid:false, msg:""},
            key_id: parseInt(props.key_id),
            required: props.data.text || false
        };

        this.handleChangeText = this.handleChangeText.bind(this);
        this.handleChangeType = this.handleChangeType.bind(this);
        this.handleChangeRequired = this.handleChangeRequired.bind(this);
        this.handleChangeChoices = this.handleChangeChoices.bind(this);
        this.removeQuestionSet = this.removeQuestionSet.bind(this);
        this.removeQuestion = this.removeQuestion.bind(this);
        this.moveQuestionDown = this.moveQuestionDown.bind(this);
        this.moveQuestionUp = this.moveQuestionUp.bind(this);
    }

    serializeData(data){
        return {
            text: this.state.text,
            type: this.state.type,
            choices: this.state.choices
        };
    }

    handleChangeText(event) {
        let validation_object;
        if (event.target.value.length === 0) {
            validation_object = {valid: false, msg:"Das ist ein Pflichtfeld"};
        } else {
            validation_object = {valid: true, msg:""}
        }
        this.setState({text: event.target.value, edited_once: true, validation_object:validation_object});
        this.props.setValidationState(validation_object.valid, this.serializeData(event.target.value));
        this.props.updateQuestion(this.props.i, {...this.state, text: event.target.value, edited_once: true, validation_object:validation_object});
    }

    handleChangeType(event) {
        this.setState({type: event.target.value});
        this.props.updateQuestion(this.props.i, {...this.state, type: event.target.value});
    }

    handleChangeRequired(event) {
        this.setState({required: event.target.checked});
        this.props.updateQuestion(this.props.i, {...this.state, required: event.target.checked});
    }

    handleChangeChoices(event) {
        this.setState({choices: event.target.value});
        this.props.updateQuestion(this.props.i, {...this.state, choices: event.target.value});
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

    removeQuestionSet(e) {
        this.props.removeQuestionSet(this.props.i);
    }

    buildMockInputData() {
        return {
            'text': this.state.text,
            'value': '',
            'required': this.state.required,
            'i': this.props.i,
            'choices': this.state.choices
        }
    }

    renderDefault() {
        return <p>No rendering available</p>
    }

    isChoicesType() {
        return ['SLQ', 'MLQ'].includes(this.state.type);
    }

    setValidationState() {
    }

    removeQuestion() {
        this.props.removeQuestion(this.state.key_id);
    }

    moveQuestionUp() {
        this.props.moveQuestionUp(this.props.i);
    }

    moveQuestionDown() {
        this.props.moveQuestionDown(this.props.i);
    }

    renderQuestionField() {


        switch(this.state.type) {
            case "MAL": // email
                return <MAL data={this.buildMockInputData()} setValidationState={this.setValidationState}  i={this.props.i} />;
            case "TME": // time
                return <TME data={this.buildMockInputData()} setValidationState={this.setValidationState}  i={this.props.i} />;
            case "DAT": // date
                return <DAT data={this.buildMockInputData()} setValidationState={this.setValidationState}  i={this.props.i} />;
            case "TXT": // textarea
                return <TXT data={this.buildMockInputData()} setValidationState={this.setValidationState}  i={this.props.i} />;
            case "CHR": // input type text
                return <CHR data={this.buildMockInputData()} setValidationState={this.setValidationState}  i={this.props.i} />;
            case "SLQ": // single choice
                return <SLQ data={this.buildMockInputData()} setValidationState={this.setValidationState}  i={this.props.i} />;
            case "MLQ": // multiple choice
                return <MLQ data={this.buildMockInputData()} setValidationState={this.setValidationState}  i={this.props.i} />;
            default:
                return this.renderDefault();
        }
    }

    render(){
        return (
            <div style={{borderStyle:'solid', margin: '15px', padding:'5px'}}>
                <ButtonToolbar>
                    <ButtonGroup bsSize="medium">
                        <Button onClick={this.moveQuestionUp}><span className="glyphicon glyphicon-chevron-up" aria-hidden="true"/> </Button>
                        <Button onClick={this.moveQuestionDown}><span className="glyphicon glyphicon-chevron-down" aria-hidden="true"/></Button>
                        <Button onClick={this.removeQuestion}><span className="glyphicon glyphicon-remove" aria-hidden="true"/></Button>
                    </ButtonGroup>
                </ButtonToolbar>


                Typ:
                <select value={this.state.type} onChange={this.handleChangeType}>
                    <option value="CHR">Einzeiliger Text</option>
                    <option value="TXT">Mehrzeiliger Text</option>
                    <option value="SLQ">Einfachauswahl</option>
                    <option value="MLQ">Mehrfachauswahl</option>
                    <option value="DAT">Datum</option>
                    <option value="TME">Uhrzeit</option>
                    <option value="MAL">E-Mail</option>
                </select>

                <div>
                    Frage:  <br/>
                    <input type="text" value={this.state.text} onChange={this.handleChangeText} /> <br/>
                    Pflichtfeld: <input type="checkbox" value={true} onChange={this.handleChangeRequired} /> <br/>
                    {this.isChoicesType() &&
                        <div>
                            Auswahlmöglichkeiten (Durch Kommas separiert) (z.B.Apfel, Ei, Meer) < br />
                            <input type="text" value={this.state.choices} onChange={this.handleChangeChoices} /> <br/>
                        </div>
                    }
                </div>

                <p>Vorschau</p>

                {this.renderQuestionField()}


            </div>
        );
    }
}

export default CreateQuestion;