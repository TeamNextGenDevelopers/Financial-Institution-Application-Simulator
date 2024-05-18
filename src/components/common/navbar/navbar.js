import React from "react";
import './navbar.css';
import { Link } from "react-router-dom";


function NavigationB () {
  return (
    <header className="header">
        <Link to='/home'><a href='/home' className="logo">T Bank Inc.</a></Link>
        <nav className="navbar">
            <a href="/home">Home</a>
            <a href="/">About</a>
            <a href="/">Documentation</a>
            <a href="/">Contact</a>
            

        </nav>
        
    </header>
  );
}

export default NavigationB;
