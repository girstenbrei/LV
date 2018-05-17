import React, { Component } from "react";
import {NavLink} from "react-router-dom";

class Navbar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <nav className="navbar navbar-default">
                <div className="container-fluid">
                    <div className="navbar-header">
                        <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                            <span className="sr-only">Toggle navigation</span>
                            <span className="icon-bar"></span>
                            <span className="icon-bar"></span>
                            <span className="icon-bar"></span>
                        </button>
                        <a className="navbar-brand" href="/">Digitale Anmeldung</a>
                    </div>

                    <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                        <ul className="nav navbar-nav">
                            <li><NavLink activeClassName="active" to="/publicEvents">Public Events</NavLink></li>
                            {this.props.isLoggedIn && <li><NavLink activeClassName="active" to="/administeredEvents">Administered Events</NavLink></li>}
                            {this.props.isLoggedIn && <li><NavLink activeClassName="active" to="/yourEvents">Your Events</NavLink></li>}
                            {this.props.isLoggedIn && <li><NavLink activeClassName="active" onClick={this.props.logoutHandler} to="/logout">Logout</NavLink></li>}
                            {!this.props.isLoggedIn && <li><NavLink activeClassName="active" to="/login">Login</NavLink></li>}
                        </ul>


                    </div>
                </div>
            </nav>
        );
    }
}

export default Navbar;