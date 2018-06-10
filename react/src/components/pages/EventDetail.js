import React, { Component } from "react";
import QuestionSet from "../QuestionSet";
import EventCard from "../EventCard";

import '../styles/EventDetail.css'

class EventDetail extends Component {
    constructor(props) {
        super(props);
        console.log(props);

        const {match: {params}} = props;



        this.state = {
            event : {},
            slug: params.slug,
            isValid : false,
            question_set_states: [],
            question_set_data: [],
        };

        this.getEvent();

        this.setValidationState = this.setValidationState.bind(this);
        this.submitForm = this.submitForm.bind(this);
    }


    setValidationState(index, value, serialized_data) {
        let new_states = this.state.question_set_states.slice(0);
        let new_data = this.state.question_set_data.slice(0);

        new_states[index] = value;
        new_data[index] = serialized_data;

        var all_true = new_states.every((val) => val === true);
        this.setState({
            question_set_states: new_states,
            question_set_data: new_data,
            isValid: all_true
        })
    }

    getEvent() {
        this.props.globalState.auth.fetch(this.props.globalState.url + '/api/event/' + this.state.slug + "/signup/")
            .then((response) => {

                let empty_states = new Array(response.question_sets.length);
                for (var i=0; i<empty_states.length; i++) {
                    empty_states[i] = false;
                }

                this.setState({event: response});
            })
            .catch(err => alert(err));
    }

    renderQuestionSets () {
        const questionSets = this.state.event.question_sets.map((questionSet, i) =>
            <QuestionSet key={'qs' + i} i={i} data={questionSet} setValidationState={this.setValidationState} />
        );
        return (
            <div>{questionSets}</div>
        );
    }

    submitForm(e) {
        e.preventDefault();

        // make a copy
        let submitData = JSON.parse(JSON.stringify(this.state.event));

        for (var i=0; i<submitData.question_sets.length; i++) {
            for (var j=0; j<submitData.question_sets[i].questions.length; j++) {
                submitData.question_sets[i].questions[j].value = this.state.question_set_data[i][j];
            }
        }

        console.log(submitData)

        const url = this.props.globalState.url + '/api/event/' + this.state.slug + "/signup/";

        console.log(url);

        this.props.globalState.auth.fetch(url
            ,
            {
                method: 'POST',
                body: JSON.stringify(submitData)
            }
        ).then((response) => {
            console.log(response);

            alert("Danke für die Anmeldung. Du wirst eine E-Mail erhalten.");

            window.location.href = '/yourEvents';
            //this.setState({event: response});
        }).catch(err => alert(err));

    }

    // The styling of the components comes from: https://codepen.io/jonnitto/pen/OVmvPB
    render() {
        if(this.state.event.details) {
            return (
                <div className="container">
                    <div className="row">
                        <div className="col-xs-12 col-sm-12 col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8">

                            <EventCard key="1" data={this.state.event.details} hideLoginButton={true}/>

                            <form className="form-card" onSubmit={this.submitForm}>

                                {this.renderQuestionSets()}
                                {(this.state.isValid) ?
                                    <button className="btn btn-primary btn-lg pull-right submit-button active" onClick={this.submitForm}>Anmelden</button>
                                    :
                                    <button  className="btn btn-primary btn-lg pull-right submit-button disabled" onClick={this.submitForm} disabled>Anmelden</button>}

                            </form>

                        </div>
                    </div>
                </div>
            );
        } else {
            return (
                <div>
                    <h2>LOADING</h2>
                </div>
            );
        }
    }
}

export default EventDetail;
