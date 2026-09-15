import { useState, useEffect } from "react";
import { getStockAnalysis, getSymbols } from "../api/client";

function SearchBar({ setAnalysis }) {

    const [symbol, setSymbol] = useState("");
    const [loading, setLoading] = useState(false);
    const [symbols, setSymbols] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);

    useEffect(() => {

        async function loadSymbols() {

            try {
                setSymbols(await getSymbols());
            }
            catch (error) {
                console.error(error);
            }
        }

        loadSymbols();

    }, []);

    const filteredSymbols = symbols.filter((item) =>
        item.startsWith(symbol.toUpperCase())
    );

    async function analyzeStock() {

        const finalSymbol = symbol.trim().toUpperCase();

        if (!finalSymbol) return;

        setShowSuggestions(false);

        setLoading(true);

        try {
            setAnalysis(await getStockAnalysis(finalSymbol));
        }
        catch (error) {
            console.error(error);

            setAnalysis({
                error: "Failed to connect to server."
            });
        }
        finally {
            setLoading(false);
        }
    }

    return (
        <>

            <input
                type="text"
                placeholder="Enter NSE Symbol (e.g. RELIANCE)"
                value={symbol}
                onChange={(event) => {
                setSymbol(event.target.value);
                setShowSuggestions(true);
                }}
                onKeyDown={(event) => {
                    if (event.key === "Enter") {
                        analyzeStock();
                    }
                }}
            />

            {
                showSuggestions &&
                symbol &&
                filteredSymbols.length > 0 &&
                <div className="suggestions">

                    {
                        filteredSymbols.slice(0, 8).map((item) => (

                            <div
                                className="suggestion"
                                key={item}
                                onClick={() => {
                                    setSymbol(item);
                                    setShowSuggestions(false);
                                }}
                            >

                                {item}

                            </div>

                        ))
                    }

                </div>
            }

            <button
                onClick={analyzeStock}
                disabled={loading}
            >
                {loading ? "Analyzing..." : "Analyze"}
            </button>

        </>
    );
}

export default SearchBar;
