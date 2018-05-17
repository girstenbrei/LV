import React, { Component } from 'react';
import './App.css';

import Login from "./components/pages/Login";
import AuthService from "./components/AuthService";
import {Route, Link, BrowserRouter, Redirect} from "react-router-dom";

import PublicEvents from "./components/pages/PublicEvents";
import AdministeredEvents from "./components/pages/AdministeredEvents";
import SignedUpEvents from "./components/pages/SignedUpEvents";
import EventDetail from "./components/pages/EventDetail";
import AdminEventDetail from "./components/pages/AdminEventDetail";
import Navbar from "./components/layoutComponents/Navbar";

class App extends Component {


    constructor(props) {
        super(props);

        const url = "http://localhost:8080";

        console.log("construct APP")

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

        console.log("check login")

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
        console.log("LOGOUT")
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

  render() {
      return (
          <BrowserRouter>
              <div className="wrapper">
                  <Navbar isLoggedIn={this.state.isLoggedIn} logoutHandler={this.logoutHandler}/>
                  {this.renderContent()}
              </div>
          </BrowserRouter>
      );
  }

}

export default App;
