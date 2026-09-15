import { useState } from "react";
import SearchBar from "./components/SearchBar";
import Analysis from "./components/Analysis";
import "./App.css";

function App() {
    const [analysis, setAnalysis] = useState(null);
    const [status, setStatus] = useState("idle");
    const [error, setError] = useState(null);

    return (
        <div className="container">
            <SearchBar
                setAnalysis={setAnalysis}
                setStatus={setStatus}
                setError={setError}
            />
            {status === "idle" && <p>Enter a stock symbol to begin.</p>}
            {status === "loading" && <p>Loading analysis...</p>}
            {status === "error" && (
                <div className="error-message">
                    <p>{error}</p>
                    <p>Check the symbol and try again.</p>
                </div>
            )}
            {status === "success" && <Analysis analysis={analysis} />}
        </div>
    );
}

export default App;
