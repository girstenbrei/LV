import React, { Component } from "react";
import {Button, ButtonGroup, ButtonToolbar, Thumbnail} from "react-bootstrap";
import CHR from "./controlledComponents/CHR";
import Question from "./Question";
import CreateQuestion from "./CreateQuestion";

class CreateQuestionSet extends Component {
    constructor(props) {
        super(props);
        this.state = {
            title: props.data.title || "",
            description: props.data.description || "",
            edited_once: false,
            validation_object: {valid:false, msg:""},
            questions: props.data.questions || []

        };

        this.handleChangeTitle = this.handleChangeTitle.bind(this);
        this.removeQuestionSet = this.removeQuestionSet.bind(this);
        this.addQuestion = this.addQuestion.bind(this);
        this.moveQuestionSetUp = this.moveQuestionSetUp.bind(this);
        this.moveQuestionSetDown = this.moveQuestionSetDown.bind(this);
    }

    serializeData(data){
        return data;
    }


    handleChangeTitle(event) {
        let validation_object;
        if (event.target.value.length === 0) {
            validation_object = {valid: false, msg:"Das ist ein Pflichtfeld"};
        } else {
            validation_object = {valid: true, msg:""}
        }
        this.setState({title: event.target.value, edited_once: true, validation_object:validation_object});
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

    removeQuestionSet(e) {
        this.props.removeQuestionSet(this.props.i);
    }

    moveQuestionSetUp(e) {
        this.props.moveQuestionSetUp(this.props.position);
    }

    moveQuestionSetDown(e) {
        this.props.moveQuestionSetDown(this.props.position);
    }

    removeQuestion(i) {
        console.log("remove question ", i)
    }

    setValidationState() {}


    renderQuestions() {
        const listItems = this.state.questions.map((question, i) =>
            <CreateQuestion key={'quest'+i} i={i} data={question} setValidationState={this.setValidationState}
                               removeQuestion={this.removeQuestion}

            />
        );
        return (
            <div>{listItems}</div>
        );
    }

    addQuestion(e) {
        this.setState(prevState => (
                {
                    questions: prevState.questions.concat([
                        {
                            text: '',
                            type: '',
                        }
                    ])
                }
            )
        )
    }

     render(){
        return (
            <Thumbnail className="EventCard">
                <ButtonToolbar>
                    <ButtonGroup bsSize="medium">
                        <Button onClick={this.moveQuestionSetUp}><span className="glyphicon glyphicon-chevron-up" aria-hidden="true"/> </Button>
                        <Button onClick={this.moveQuestionSetDown}><span className="glyphicon glyphicon-chevron-down" aria-hidden="true"/></Button>
                        <Button onClick={this.removeQuestionSet}><span className="glyphicon glyphicon-remove" aria-hidden="true"/></Button>
                    </ButtonGroup>
                </ButtonToolbar>

                <div>
                    Titel:  <br/>
                    <input type="text" /> <br/>
                    Beschreibung <br/>
                    <input type="text"/> <br/>
                </div>

                {this.renderQuestions()}


                <hr/>
                <Button onClick={this.addQuestion}><span className="glyphicon glyphicon-plus" aria-hidden="true"/> Neue Frage</Button>


            </Thumbnail>
        );
    }
}

export default CreateQuestionSet;