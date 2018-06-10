import React, { Component } from "react";
import {Button, ButtonGroup, ButtonToolbar, Thumbnail} from "react-bootstrap";
import CreateQuestion from "./CreateQuestion";

class CreateQuestionSet extends Component {
    constructor(props) {
        super(props);
        this.state = {
            title: props.data.title || "",
            description: props.data.description || "",
            edited_once: false,
            validation_object: {valid:false, msg:""},
            questions: [],
            questions_data: [],
            key_id: parseInt(this.props.key_id)

        };

        this.render_count = 0;

        this.handleChangeTitle = this.handleChangeTitle.bind(this);
        this.handleChangeDescription = this.handleChangeDescription.bind(this);
        this.removeQuestionSet = this.removeQuestionSet.bind(this);
        this.addQuestion = this.addQuestion.bind(this);
        this.moveQuestionSetUp = this.moveQuestionSetUp.bind(this);
        this.moveQuestionSetDown = this.moveQuestionSetDown.bind(this);

        this.removeQuestion = this.removeQuestion.bind(this);
        this.moveQuestionUp = this.moveQuestionUp.bind(this);
        this.moveQuestionDown = this.moveQuestionDown.bind(this);
        this.updateQuestion = this.updateQuestion.bind(this);
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
        this.props.updateQuestionSet(this.props.position, {...this.state, title: event.target.value, edited_once: true, validation_object:validation_object});
    }

    handleChangeDescription(event) {
        let validation_object;
        validation_object = {valid: true, msg:""}

        this.setState({description: event.target.value, edited_once: true, validation_object:validation_object});
        this.props.setValidationState(validation_object.valid, this.serializeData(event.target.value))
        this.props.updateQuestionSet(this.props.position, {...this.state,
            description: event.target.value, edited_once: true, validation_object:validation_object})
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

    updateQuestion(i, question_state) {

        let qs = this.state.questions_data;
        qs[i] = question_state;

        this.setState({
            questions_data: qs
        });

        this.props.updateQuestionSet(this.props.position, {...this.state, questions_data: qs});
    }

    removeQuestion(i) {
        var i = parseInt(i);

        console.log("Remove Question", i);

        var quests = this.state.questions.slice();
        let quests_data = this.state.questions_data;
        var new_quests = quests.filter((o) => o['key_id'] !== i);
        var new_quests_data = quests_data.filter((o) => o['key_id'] !== i);

        this.setState({
            questions: new_quests,
            questions_data: new_quests_data
        });

        this.props.updateQuestionSet(this.props.position, {...this.state, questions: new_quests, questions_data: new_quests_data});

    }

    moveQuestionUp(i) {
        var i = parseInt(i);
        if (i === 0) {
            return;
        }

        var sets = this.state.questions.slice();
        var data_sets = this.state.questions_data.slice();

        var elem = sets[i];
        sets[i] = sets[i-1];
        sets[i-1] = elem;

        var elem2 = data_sets[i];
        data_sets[i] = data_sets[i-1];
        data_sets[i-1] = elem2;

        this.setState({
            questions: sets,
            questions_data: data_sets
        });

        this.props.updateQuestionSet(this.props.position, {...this.state, questions: sets, questions_data: data_sets});


    }

    moveQuestionDown(i) {
        var i = parseInt(i);
        if (i+1 === this.state.questions.length) {
            console.log(this.state.questions.length)
            return;
        }

        var sets = this.state.questions.slice();
        var data_sets = this.state.questions_data.slice();

        var elem = sets[i];
        sets[i] = sets[i+1];
        sets[i+1] = elem;

        var elem2 = data_sets[i];
        data_sets[i] = data_sets[i+1];
        data_sets[i+1] = elem2;

        this.setState({
            questions: sets,
            questions_data: data_sets
        });

        this.props.updateQuestionSet(this.props.position, {...this.state, questions: sets, questions_data: data_sets});
    }

    setValidationState() {}


    renderQuestions() {
        const listItems = this.state.questions.map((question, i) =>
            <CreateQuestion key={question.key_id}
                            key_id={question.key_id}
                            i={i}
                            data={question}
                            setValidationState={this.setValidationState}
                            removeQuestion={this.removeQuestion}
                            moveQuestionUp={this.moveQuestionUp}
                            moveQuestionDown={this.moveQuestionDown}
                            updateQuestion={this.updateQuestion}

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
                            key_id: this.render_count
                        }
                    ]),
                    questions_data: prevState.questions_data.concat([
                        {
                            text: '',
                            type: '',
                            key_id: this.render_count
                        }
                    ]),

                }
            )
        )

        let q = this.state.questions.concat([
            {
                text: '',
                type: '',
                key_id: this.render_count
            }
        ]);

        let q_data = this.state.questions_data.concat([
            {
                text: '',
                type: '',
                key_id: this.render_count
            }
        ]);

        this.render_count++;

        this.props.updateQuestionSet(this.props.position, {...this.state, questions: q, questions_data: q_data});
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
                    <input type="text" onChange={this.handleChangeTitle}/> <br/>
                    Beschreibung <br/>
                    <input type="text" onChange={this.handleChangeDescription}/> <br/>
                </div>

                {this.renderQuestions()}


                <hr/>
                <Button onClick={this.addQuestion}><span className="glyphicon glyphicon-plus" aria-hidden="true"/> Neue Frage</Button>


            </Thumbnail>
        );
    }
}

export default CreateQuestionSet;