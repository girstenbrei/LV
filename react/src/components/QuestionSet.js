import React, { Component } from "react";
import Question from "./Question";


class QuestionSet extends Component {
    constructor(props) {
        super(props);

        let empty_states = new Array(this.props.data.questions.length);
        for (var i=0; i<empty_states.length; i++) {
            empty_states[i] = false;
        }

        this.state = {
            questions_states: empty_states,
            question_data: new Array(this.props.data.questions.length),
            isValid: false
        };

        this.setValidationState = this.setValidationState.bind(this);

    }

    setValidationState(index, value, serialized_data) {
        let new_states = this.state.questions_states.slice(0);
        let new_data = this.state.question_data.slice(0);

        new_states[index] = value;
        new_data[index] = serialized_data;
        var all_true = new_states.every((val) => val === true);
        this.setState({
            questions_states: new_states,
            question_data: new_data,
            isValid: all_true
        })
        this.props.setValidationState(this.props.i, all_true, new_data)
    }

    renderQuestions () {
        const questions = this.props.data.questions.map((question, i) =>
            <Question key={'q'+i} i={i} data={question}  setValidationState={this.setValidationState}/>
        );
        return (
            <div>{questions}</div>
        );
    }

    render() {
        return (
            <div>
                <h2>{this.props.data.label}</h2>
                <p>{this.props.data.description}</p>

                {this.renderQuestions()}

            </div>
        );
    }
}

export default QuestionSet;