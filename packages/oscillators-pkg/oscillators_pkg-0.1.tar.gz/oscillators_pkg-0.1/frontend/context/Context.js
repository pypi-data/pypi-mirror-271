import { createContext, useEffect, useState } from "react";
import { useContext } from "react"; // Import useContext
import axios from "axios";

export const Context = createContext();

export const ContextProvider = ({ children }) => {
    const [forward_r1, setforward_r1] = useState(null);
    const [forward_r2, setforward_r2] = useState(null);
    const [forward_lambda1, setforward_lambda1] = useState(null);
    const [backward_r1, setbackward_r1] = useState(null);
    const [backward_r2, setbackward_r2] = useState(null);
    const [backward_lambda1, setbackward_lambda1] = useState(null);
    const [type, settype] = useState('Forward')
    const [theta, settheta] = useState(null)
    const [time, settime] = useState(null)

    const ContextData = {
        forward_r1,
        setforward_r1,
        forward_r2,
        setforward_r2,
        forward_lambda1,
        setforward_lambda1,
        backward_r1,
        setbackward_r1,
        backward_r2,
        setbackward_r2,
        backward_lambda1,
        setbackward_lambda1,
        type,
        settype,
        theta,settheta,
        time,settime
    };

    return (
        <Context.Provider value={ContextData}>
            {children}
        </Context.Provider>
    );
};

// Custom hook to consume the context
export const useContextData = () => useContext(Context);
