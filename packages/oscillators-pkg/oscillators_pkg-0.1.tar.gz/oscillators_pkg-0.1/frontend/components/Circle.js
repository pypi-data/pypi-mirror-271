import React from 'react'

export default function Circle() {
    return (
        <div className='relative overflow-hidden w-screen'>
            
            <div className="container">
                <div className="circles-wrapper">
                    <div className="circle circle-lg blur">
                        <div className="circle circle-lg-1 blur">
                            <div className="circle circle-lg-2 blur"></div>
                        </div>
                    </div>
                    <div className="circle circle-lg-3 blur">
                        <div className="circle circle-lg-4 blur">
                            <div className="circle circle-lg-5 blur"></div>
                        </div>
                    </div>
                    <div className="circle circle-lg-6 blur">
                        <div className="circle circle-lg-7 blur">
                            <div className="circle circle-lg-8 blur"></div>
                        </div>
                    </div>
                </div>
            </div>
            <style jsx>
                {`
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
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                      }
                      
                      .circles-wrapper {
                        width: 450px;
                        height: 450px;
                      }
                      
                      .circle {
                        border: 0.1px solid white;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        border-radius: 50%;
                        position: absolute;
                        filter: blur(2px); /* Add blur effect */
                      }
                      
                      .circle::before {
                        content: '';
                        position: absolute;
                        width: 12px;
                        height: 12px;
                        background:white;
                        top: -6px;
                        border-radius: 50%;
                        box-shadow: 0 0 10px 6px white;
                        filter: blur(2px); /* Add blur effect */
                      }
                      
                      .circle-lg {
                        width: 450px;
                        height: 450px;
                        animation: rotateCircles 3s linear infinite;
                      }
                      
                      .circle-lg-1 {
                        width: 450px;
                        height: 450px;
                        animation: rotateCircles 4s linear infinite;
                      }
                      
                      .circle-lg-2 {
                        width: 450px;
                        height: 450px;
                        animation: rotateCircles 5s linear infinite;
                      }
                      
                      .circle-lg-3 {
                        width: 450px;
                        height: 450px;
                        animation: rotateCircles 6s linear infinite;
                      }
                      
                      .circle-lg-4 {
                        width: 450px;
                        height: 450px;
                        animation: rotateCircles 7s linear infinite;
                      }
                      
                      .circle-lg-5 {
                        width: 450px;
                        height: 450px;
                        animation: rotateCircles 8s linear infinite;
                      }
                      
                      .circle-lg-6 {
                        width: 450px;
                        height: 450px;
                        animation: rotateCircles 9s linear infinite;
                      }
                      
                      .circle-lg-7 {
                        width: 450px;
                        height: 450px;
                        animation: rotateCircles 10s linear infinite;
                      }
                      
                      .circle-lg-8 {
                        width: 450px;
                        height: 450px;
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
                      
                      .blur {
                        filter: blur(2px); /* Add blur effect */
                      }
                `}
            </style>
        </div>
    )
}