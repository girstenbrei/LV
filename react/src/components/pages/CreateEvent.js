import React, { Component } from "react";
import {Button, ButtonGroup, ButtonToolbar, Thumbnail} from "react-bootstrap";
import DateTime from 'react-datetime';

import "../styles/react-datetime.css"
import CreateQuestionSet from "../CreateQuestionSet";


class CreateEvent extends Component {
    constructor(props) {
        super(props);

        this.state = {
            name: '',
            signup_from: '',
            signup_to: '',
            change_signup_after_submit: false,
            multiple_signups_per_person: false,
            description: '',
            start_datetime: '',
            end_datetime: '',
            post_address: '',
            analog_submission_required: false,

            question_sets: [],
            question_sets_data: [],
        };

        this.render_count = 0;


        this.addQuestionSet = this.addQuestionSet.bind(this);
        this.saveEvent = this.saveEvent.bind(this);
        this.removeQuestionSet = this.removeQuestionSet.bind(this);
        this.moveQuestionSetUp = this.moveQuestionSetUp.bind(this);
        this.moveQuestionSetDown = this.moveQuestionSetDown.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.updateQuestionSet = this.updateQuestionSet.bind(this);

    }

    addQuestionSet(e) {
        this.setState(prevState => (
            {
                question_sets: prevState.question_sets.concat([
                    {
                        title: '',
                        description: '',
                        key_id: this.render_count
                    }
                ]),
                question_sets_data: prevState.question_sets_data.concat([
                    {
                        title: '',
                        description: '',
                        key_id: this.render_count,
                        questions_data: []
                    }
                ]),
            }
            )
        )

        this.render_count++;
    }

    handleChange(e) {
        console.log(e);
        let change = {};
        change[e.target.name] = e.target.value;
        this.setState(change)
    }

    saveEvent(e) {
        e.preventDefault();

        let submit_data = {
            name: this.state.name,
            signup_to: this.state.signup_to,
            signup_type: this.state.signup_type,
            change_signup_after_submit: this.state.change_signup_after_submit,
            multiple_signups_per_person: this.state.multiple_signups_per_person,
            description: this.state.description,
            start_datetime: this.state.start_datetime,
            signup_from: this.state.signup_from,
            end_datetime: this.state.end_datetime,
            post_address: this.state.post_address,
            question_sets: []
        };

        this.state.question_sets_data.forEach((question_set) => {
            var qs = {
                label: question_set.title,
                description: question_set.description,
                questions: []
            };

            console.log(question_set);

            question_set.questions_data.forEach((q) => {
                var question = {
                    type: q.type,
                    text: q.text,
                    choices: q.choices,
                    required: q.required
                };

                qs.questions.push(question);
            });


            submit_data.question_sets.push(qs);
        });


        let submitData = JSON.stringify(submit_data);
        console.log(submitData);

        const url = this.props.globalState.url + '/api/event/new/';

        console.log(url);

        this.props.globalState.auth.fetch(url
            ,
            {
                method: 'POST',
                body: submitData
            }
        ).then((response) => {
            console.log(response);

            alert("Das Event wurde erstellt.");

            window.location.href = '/yourEvents';
            //this.setState({event: response});
        }).catch(err => {console.log(err); alert(err)});

    }

    removeQuestionSet(question_set_index) {

        console.log("Remove Question Set", question_set_index);

        var sets = this.state.question_sets.slice();
        var sets_data = this.state.question_sets_data.slice();

        var new_sets = sets.filter((o) => o['key_id'] !== parseInt(question_set_index));
        var new_sets_data = sets_data.filter((o) => o['key_id'] !== parseInt(question_set_index));

        this.setState({
            question_sets: new_sets,
            question_sets_data: new_sets_data,
        });

    }

    moveQuestionSetUp(question_set_index) {
        var i = parseInt(question_set_index);
        if (i === 0) {
            return;
        }

        var sets = this.state.question_sets.slice();
        var elem = sets[i];
        sets[i] = sets[i-1];
        sets[i-1] = elem;

        var sets_data = this.state.question_sets_data.slice();
        var elem2 = sets_data[i];
        sets_data[i] = sets_data[i-1];
        sets_data[i-1] = elem2;

        this.setState({
            question_sets: sets,
            question_sets_data: sets_data,
        });
    }

    moveQuestionSetDown(question_set_index) {
        var i = parseInt(question_set_index);
        if (i+1 === this.state.question_sets.length) {
            return;
        }

        var sets = this.state.question_sets.slice();
        var elem = sets[i];
        sets[i] = sets[i+1];
        sets[i+1] = elem;

        var sets2 = this.state.question_sets_data.slice();
        var elem2 = sets2[i];
        sets2[i] = sets2[i+1];
        sets2[i+1] = elem2;

        this.setState({
            question_sets: sets,
            question_sets_data: sets2,
        });
    }

    setValidationState() {}

    updateQuestionSet(i, state) {
        let qs_data = this.state.question_sets_data;
        qs_data[i] = state;

        this.setState({
            question_sets_data: qs_data
        })
    }

    renderQuestionSets() {
        const listItems = this.state.question_sets.map((question_set, i) =>
            <CreateQuestionSet key={`cqs${question_set.key_id}`}
                               i={`${question_set.key_id}`}
                               key_id={`${question_set.key_id}`}
                               position={i}
                               data={question_set}
                               setValidationState={this.setValidationState}
                               removeQuestionSet={this.removeQuestionSet}
                               moveQuestionSetDown={this.moveQuestionSetDown}
                               moveQuestionSetUp={this.moveQuestionSetUp}
                               updateQuestionSet={this.updateQuestionSet}
            />
        );
        return (
            <div>{listItems}</div>
        );
    }

    render() {


        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="col-xs-12 col-sm-12 col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8">
                            <div>
                                <h2>Neue Veranstaltung</h2>
                                <br />


                                <Thumbnail className="EventCard">
                                    <h3>Generell</h3>

                                    Name der Veranstaltung
                                    <br/>
                                    <input name="name" type="text" value={this.state.name} onChange={this.handleChange}/>
                                    <br/>
                                    Beschreibung
                                    <br/>
                                    <textarea name="description" value={this.state.description} onChange={this.handleChange}></textarea>
                                    <br/>

                                    Start Signup:
                                    <DateTime name="signup_from" value={this.state.signup_from} onChange={(e) => {this.handleChange({target: {name: 'signup_from', value:e }})}}/>
                                    End Signup:
                                    <DateTime name="signup_to" value={this.state.signup_to} onChange={(e) => {this.handleChange({target: {name: 'signup_to', value:e }})}}/>
                                    Start Event:
                                    <DateTime name="start_datetime" value={this.state.start_datetime} onChange={(e) => {this.handleChange({target: {name: 'start_datetime', value:e }})}}/>
                                    End Event:
                                    <DateTime name="end_datetime" value={this.state.end_datetime} onChange={(e) => {this.handleChange({target: {name: 'end_datetime', value:e }})}}/>

                                    <br/>

                                    Per Post? <input  name="analog_submission_required" onChange={this.handleChange} type="checkbox"/>

                                    <br/>
                                    Post-Adresse
                                    <br/>

                                    <textarea name="post_address" value={this.state.post_address} onChange={this.handleChange}> </textarea>

                                    <br/>
                                    Nur über Link erreichbar? &nbsp;
                                    <input type="checkbox" />
                                    <br/>
                                    Daten im Nachhinein ändern? &nbsp;
                                    <input type="checkbox"/>
                                    <br/>



                                </Thumbnail>

                            </div>

                            {this.renderQuestionSets()}

                            <Thumbnail className="EventCard">
                                <ButtonToolbar>
                                    <ButtonGroup bsSize="large">
                                        <Button><span className="glyphicon glyphicon-search" aria-hidden="true"/> Katalog der Fragenkarten</Button>
                                        <Button onClick={this.addQuestionSet}><span className="glyphicon glyphicon-plus" aria-hidden="true"/> Neue Fragenkarte</Button>
                                        <Button onClick={this.saveEvent}><span className="glyphicon glyphicon-ok" aria-hidden="true"/> Speichern!</Button>
                                    </ButtonGroup>
                                </ButtonToolbar>
                            </Thumbnail>



                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default CreateEvent;