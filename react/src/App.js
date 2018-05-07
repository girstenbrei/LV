import React, { Component } from 'react';
import './App.css';

import Login from "./components/Login";
import AuthService from "./components/AuthService";
import {Route, Link, BrowserRouter, Redirect} from "react-router-dom";

import PublicEvents from "./components/PublicEvents";
import AdministeredEvents from "./components/AdministeredEvents";
import SignedUpEvents from "./components/SignedUpEvents";
import EventDetail from "./components/EventDetail";
import AdminEventDetail from "./components/AdminEventDetail";

class App extends Component {


    constructor(props) {
        super(props);

        const url = "http://localhost:8080";

        this.state = {
            isLoggedIn: false,
            loginChecked: false,
            url: url,
            auth: new AuthService(url)
        }


        if(!this.state.loginChecked) {
            this.checkLogin();
        }

        this.changeAppState = this.changeAppState.bind(this);
        this.logoutHandler = this.logoutHandler.bind(this);
    }

    checkLogin()  {
        this.state.auth.refresh()
            .then(() => {
                this.setState({
                    isLoggedIn: true,
                    loginChecked: true
                })
            })
            .catch((err) => {
                this.setState({
                    isLoggedIn: false,
                    loginChecked: true
                })
            });
    }

    changeAppState(data) {
        console.log('changeAppState', data);
        this.setState(data);
    }

    logoutHandler(e) {
        this.state.auth.logout();
        this.changeAppState({isLoggedIn:false});
    }

    renderContent() {
        return <div id="content">
            <Route exact path="/" render={() => (<Redirect to="/publicEvents" />)}/>
            <Route exact path="/publicEvents"
                   render={(props) => (<PublicEvents {...props} globalState={this.state} changeAppState={this.changeAppState}/>)}/>
            <Route path="/publicEvents/:slug"
                   render={(props) => (<EventDetail {...props} globalState={this.state} changeAppState={this.changeAppState}/>)}/>
            <Route exact path="/administeredEvents"
                   render={(props) => (<AdministeredEvents {...props} globalState={this.state} changeAppState={this.changeAppState}/>)}/>
            <Route path="/administeredEvents/:id" component={AdminEventDetail}/>
            <Route path="/yourEvents"
                   render={(props) => (<SignedUpEvents {...props} globalState={this.state} changeAppState={this.changeAppState}/>)}/>
            {(this.state.isLoggedIn) ?
                <Route exact path="/login" render={() => (<Redirect to="/publicEvents"/>)}/>
                :
                <Route path="/login"
                       render={() => (<Login globalState={this.state} changeAppState={this.changeAppState}/>)}/>
            }
        </div>

    }

    renderHeader() {
        return(
            <nav className="navbar navbar-light bg-light">
                <span className="navbar-brand mb-0 h1">Digitale Anmeldung</span>
            </nav>
        );
    }

    renderSideNav() {
        return <nav id="sidebar">

            <div className="sidebar-header">
                <h3>Menu</h3>
            </div>

            {(this.state.isLoggedIn)
            ?
            <ul className="list-unstyled components">
                <li className="active"><Link to="/publicEvents">Public Events</Link></li>
                <li><Link to="/administeredEvents">Administered Events</Link></li>
                <li><Link to="/yourEvents">Your Events</Link></li>
                <li><Link onClick={this.logoutHandler} to="/">Logout</Link></li>
            </ul>
            :
            <ul className="list-unstyled components">
                <li className="active"><Link to="/publicEvents">Public Events</Link></li>
                <li><Link to="/login">Login</Link></li>
            </ul>}
        </nav>
    }

    renderWrapper(){
        return <BrowserRouter>
            <div className="wrapper">
                {this.renderSideNav()}
                {this.renderContent()}
            </div>
        </BrowserRouter>
    }


    collectComponents() {
        return <div>
            {this.renderHeader()}
            {this.renderWrapper()}
        </div>
    }

  render() {
      return this.collectComponents();
  }
}

export default App;
