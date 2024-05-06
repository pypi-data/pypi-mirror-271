import Circle from '@/components/Circle';
import Hero from '@/components/Hero';
import React, { useEffect, useRef } from 'react';
import Link from 'next/link';
const Home = () => {
  const containerRef = useRef(null);
  const hamburgerMenuRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    const hamburgerMenu = hamburgerMenuRef.current;

    const handleClick = () => {
      container.classList.toggle('active');
      document.getElementById('container').classList.toggle('bg-white');
      document.getElementById('container').classList.toggle('bg-opacity-10');
      document.getElementById('shadow1').classList.toggle('hidden')
      document.getElementById('shadow2').classList.toggle('hidden')
    };

    hamburgerMenu.addEventListener('click', handleClick);

    return () => {
      hamburgerMenu.removeEventListener('click', handleClick);
    };
  }, []);

  return (
    <div className="container" ref={containerRef}>

      <div className="navbar">
        <div className="menu">
          <h3 className="logo">
            Kuramoto<span> Oscillator</span>
          </h3>
          <div className="hamburger-menu" ref={hamburgerMenuRef}>
            <div className="bar"></div>
          </div>
        </div>

      </div>

      <div className="main-container">

        <div className="main ">

          <div id="container" className="container  !w-screen">
            <Hero />

          </div>

        </div>
        <div id="shadow1" className="shadow one hidden"></div>
        <div id="shadow2" className="shadow two hidden"></div>
      </div>

      <div className="links">
        <ul>
          <li>
            <a href="/" style={{ '--i': '0.05s' }}>
              Home
            </a>
          </li>
          <li>
            <a href="/Plotting" style={{ '--i': '0.1s' }}>
              Plotting
            </a>
          </li>
          <li>
            <a href="/AboutProject" style={{ '--i': '0.15s' }}>
              About Project
            </a>
          </li>
        </ul>
      </div>

      <style jsx>{`
       

        * {
          padding: 0;
          margin: 0;
          box-sizing: border-box;
        }
        
        body,
        button {
          font-family: "Poppins", sans-serif;
        }
        
        html {
          box-sizing: border-box;
        }
        
        *, *::before, *::after {
          margin: 0;
          padding: 0;
          box-sizing: inherit;
        }
        
        html, body {
          width: 100%;
          height: 100%;
        }
        
        body {
          background: #333;
          color: #fff;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
          font-size: 16px;
          line-height: 1.6;
        }
        
        .container {
          width: 100%;
          min-height: 100%;
          display: flex;
          justify-content: center;
          align-items: center;
        }
        
        .circles-wrapper {
          width: 200px;
          height: 200px;
        }
        
        .circle {
          border: 2px solid crimson;
          display: flex;
          justify-content: center;
          align-items: center;
          border-radius: 50%;
          position: absolute;
        }
        
        .circle::before {
          content: '';
          position: absolute;
          width: 12px;
          height: 12px;
          background: #fff;
          top: -6px;
          border-radius: 50%;
          box-shadow: 0 0 10px 6px rgba(237, 20, 61, .8);
        }
        
        .circle-lg {
          width: 200px;
          height: 200px;
          animation: rotateCircles 3s linear infinite;
        }
        
        .circle-lg-1 {
          width: 200px;
          height: 200px;
          animation: rotateCircles 4s linear infinite;
        }
        
        .circle-lg-2 {
          width: 200px;
          height: 200px;
          animation: rotateCircles 5s linear infinite;
        }
        
        .circle-lg-3 {
          width: 200px;
          height: 200px;
          animation: rotateCircles 6s linear infinite;
        }
        
        .circle-lg-4 {
          width: 200px;
          height: 200px;
          animation: rotateCircles 7s linear infinite;
        }
        
        .circle-lg-5 {
          width: 200px;
          height: 200px;
          animation: rotateCircles 8s linear infinite;
        }
        
        .circle-lg-6 {
          width: 200px;
          height: 200px;
          animation: rotateCircles 9s linear infinite;
        }
        
        .circle-lg-7 {
          width: 200px;
          height: 200px;
          animation: rotateCircles 10s linear infinite;
        }
        
        .circle-lg-8 {
          width: 200px;
          height: 200px;
          animation: rotateCircles 11s linear infinite;
        }
        
        .circle-md {
          width: 150px;
          height: 150px;
          animation: rotateCircles 3s linear infinite;
        }
        
        .circle-md::before {
          width: 10px;
          height: 10px;
        }
        
        .circle-sm {
          width: 100px;
          height: 100px;
          animation: rotateCircles 2.5s linear infinite;
        }
        
        .circle-sm::before {
          width: 10px;
          height: 10px;
        }
        
        
        @keyframes rotateCircles {
          from {
            transform: rotate(0);
          } to {
            transform: rotate(360deg);
          }
        }
        .container {
          min-height: 100vh;
          width: 100%;
          
          
          overflow-x: hidden;
          transform-style: preserve-3d;
        }
        
        .navbar {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          z-index: 10;
          height: 3rem;
        }
        
        .menu {
          max-width: 72rem;
          width: 100%;
          margin: 0 auto;
          padding: 0 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          color: #fff;
        }
        
        .logo {
          font-size: 1.1rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 2px;
          line-height: 4rem;
        }
        
        .logo span {
          font-weight: 300;
        }
        
        .hamburger-menu {
          height: 4rem;
          width: 3rem;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: flex-end;
        }
        
        .bar {
          width: 1.9rem;
          height: 1.5px;
          border-radius: 2px;
          background-color: #eee;
          transition: 0.5s;
          position: relative;
        }
        
        .bar:before,
        .bar:after {
          content: "";
          position: absolute;
          width: inherit;
          height: inherit;
          background-color: #eee;
          transition: 0.5s;
        }
        
        .bar:before {
          transform: translateY(-9px);
        }
        
        .bar:after {
          transform: translateY(9px);
        }
        
        .main {
          position: relative;
          width: 100%;
          left: 0;
          z-index: 5;
          overflow: hidden;
          transform-origin: left;
          transform-style: preserve-3d;
          transition: 0.5s;
        }
        
        header {
          min-height: 100vh;
          width: 100%;
          background: url("https://i.postimg.cc/vHtXVqkr/bg.jpg") no-repeat top center / cover;
          position: relative;
        }
        
        .overlay {
          position: absolute;
          width: 100%;
          height: 100%;
          top: 0;
          left: 0;
          
          display: flex;
          justify-content: center;
          align-items: center;
        }
        
        .inner {
          max-width: 35rem;
          text-align: center;
          color: #fff;
          padding: 0 2rem;
        }
        
        .title {
          font-size: 2.7rem;
        }
        
        .btn {
          margin-top: 1rem;
          padding: 0.6rem 1.8rem;
          background-color: #1179e7;
          border: none;
          border-radius: 25px;
          color: #fff;
          text-transform: uppercase;
          cursor: pointer;
          text-decoration: none;
        }
        
        .container.active .bar {
          transform: rotate(360deg);
          background-color: transparent;
        }
        
        .container.active .bar:before {
          transform: translateY(0) rotate(45deg);
        }
        
        .container.active .bar:after {
          transform: translateY(0) rotate(-45deg);
        }
        
        .container.active .main {
          animation: main-animation 0.5s ease;
          cursor: pointer;
          transform: perspective(1300px) rotateY(20deg) translateZ(310px) scale(0.5);
        }
        
        @keyframes main-animation {
          from {
            transform: translate(0);
          }
        
          to {
            transform: perspective(1300px) rotateY(20deg) translateZ(310px) scale(0.5);
          }
        }
        
        .links {
          position: absolute;
          width: 30%;
          right: 0;
          top: 0;
          height: 100vh;
          z-index: 2;
          display: flex;
          justify-content: center;
          align-items: center;
        }
        
        ul {
          list-style: none;
        }
        
        .links a {
          text-decoration: none;
          color: #eee;
          padding: 0.7rem 0;
          display: inline-block;
          font-size: 1rem;
          font-weight: 300;
          text-transform: uppercase;
          letter-spacing: 1px;
          transition: 0.3s;
          opacity: 0;
          transform: translateY(10px);
          animation: hide 0.5s forwards ease;
        }
        
        .links a:hover {
          color: #fff;
        }
        
        .container.active .links a {
          animation: appear 0.5s forwards ease var(--i);
        }
        
        @keyframes appear {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0px);
          }
        }
        
        @keyframes hide {
          from {
            opacity: 1;
            transform: translateY(0px);
          }
          to {
            opacity: 0;
            transform: translateY(10px);
          }
        }
        
        .shadow {
          position: absolute;
          width: 100%;
          height: 100vh;
          top: 0;
          left: 0;
          transform-style: preserve-3d;
          transform-origin: left;
          transition: 0.5s;
          background-color: white;
        }
        
        .shadow.one {
          z-index: -1;
          opacity: 0.15;
        }
        
        .shadow.two {
          z-index: -2;
          opacity: 0.1;
        }
        
        .container.active .shadow.one {
          animation: shadow-one 0.6s ease-out;
          transform: perspective(1300px) rotateY(20deg) translateZ(215px) scale(0.5);
        }
        
        @keyframes shadow-one {
          0% {
            transform: translate(0);
          }
        
          5% {
            transform: perspective(1300px) rotateY(20deg) translateZ(310px) scale(0.5);
          }
        
          100% {
            transform: perspective(1300px) rotateY(20deg) translateZ(215px) scale(0.5);
          }
        }
        
        .container.active .shadow.two {
          animation: shadow-two 0.6s ease-out;
          transform: perspective(1300px) rotateY(20deg) translateZ(120px) scale(0.5);
        }
        
        @keyframes shadow-two {
          0% {
            transform: translate(0);
          }
        
          20% {
            transform: perspective(1300px) rotateY(20deg) translateZ(310px) scale(0.5);
          }
        
          100% {
            transform: perspective(1300px) rotateY(20deg) translateZ(120px) scale(0.5);
          }
        }
        
        .container.active .main:hover + .shadow.one {
          transform: perspective(1300px) rotateY(20deg) translateZ(230px) scale(0.5);
        }
        
        .container.active .main:hover {
          transform: perspective(1300px) rotateY(20deg) translateZ(340px) scale(0.5);
        }
        
      `}</style>
    </div>
  );
};

export default Home;