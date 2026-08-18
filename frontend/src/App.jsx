import { useState } from "react";
import SearchBar from "./components/SearchBar";
import Analysis from "./components/Analysis";
import "./App.css";

function App() {
    const [analysis, setAnalysis] = useState(null);

    return (
        <div className="container">
            <SearchBar setAnalysis={setAnalysis} />
            <Analysis analysis={analysis} />
        </div>
    );
}

export default App;