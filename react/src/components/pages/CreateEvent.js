import React, { Component } from "react";
import EventCard from "../EventCard";
import {Button, ButtonGroup, ButtonToolbar, Thumbnail} from "react-bootstrap";
import DateTime from 'react-datetime';

import "../styles/react-datetime.css"
import CHR from "../controlledComponents/CHR";
import CreateQuestionSet from "../CreateQuestionSet";


class CreateEvent extends Component {
    constructor(props) {
        super(props);

        this.state = {
            question_sets: []
        };

        this.render_count = 0


        this.addQuestionSet = this.addQuestionSet.bind(this);
        this.removeQuestionSet = this.removeQuestionSet.bind(this);
        this.moveQuestionSetUp = this.moveQuestionSetUp.bind(this);
        this.moveQuestionSetDown = this.moveQuestionSetDown.bind(this);

    }

    addQuestionSet(e) {
        this.setState(prevState => (
            {
                question_sets: prevState.question_sets.concat([
                    {
                        title: '',
                        description: '',
                        key_id: this.render_count++
                    }
                ])
            }
            )
        )
    }

    removeQuestionSet(question_set_index) {

        console.log("Remove Question Set", question_set_index);

        var sets = this.state.question_sets.slice();
        console.log(sets)
        var new_sets = sets.filter((o) => o['key_id'] !== parseInt(question_set_index));
        console.log(new_sets);

        this.setState({
            question_sets: new_sets
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

        this.setState({
            question_sets: sets
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

        this.setState({
            question_sets: sets
        });
    }

    setValidationState() {}

    renderQuestionSets() {
        const listItems = this.state.question_sets.map((question_set, i) =>
            <CreateQuestionSet key={`cqs${question_set.key_id}`}
                               i={`${question_set.key_id}`}
                               position={i}
                               data={question_set}
                               setValidationState={this.setValidationState}
                               removeQuestionSet={this.removeQuestionSet}
                               moveQuestionSetDown={this.moveQuestionSetDown}
                               moveQuestionSetUp={this.moveQuestionSetUp}
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
                                    <input type="text" />
                                    <br/>
                                    Beschreibung
                                    <br/>
                                    <textarea></textarea>
                                    <br/>

                                    Start Signup:
                                    <DateTime />
                                    End Signup:
                                    <DateTime />
                                    Start Event:
                                    <DateTime />
                                    End Event:
                                    <DateTime />

                                    <br/>

                                    Per Post? <input type="checkbox"/>

                                    <br/>
                                    Post-Adresse
                                    <br/>

                                    <textarea></textarea>

                                    <br/>
                                    Nur über Link erreichbar? &nbsp;
                                    <input type="checkbox"/>
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
                                        <Button><span className="glyphicon glyphicon-ok" aria-hidden="true"/> Speichern!</Button>
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