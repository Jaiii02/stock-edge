const labels = {
    roe: "ROE", pe: "P/E", peg: "PEG", ev_ebitda: "EV/EBITDA",
    fcf_yield: "FCF Yield", price_to_book: "Price to Book",
    revenue_growth: "Revenue Growth", earnings_growth: "Earnings Growth",
    operating_margin: "Operating Margin", gross_margin: "Gross Margin",
    net_debt_ebitda: "Net Debt / EBITDA", fcf_conversion: "FCF Conversion",
    forward_pe: "Forward P/E",
};

function MetricsCard({ title, section }) {
    return (
        <div className="card">
            <h2>{title}</h2>
            <p><strong>Score:</strong> {section.score}/10</p>
            <p><strong>Confidence:</strong> {section.confidence_level}</p>
            <hr />
            {Object.entries(section.metrics).map(([key, value]) => (
                <div className="metric" key={key}>
                    <span>{labels[key] || key}</span>
                    <span>{value ?? "NA"}</span>
                </div>
            ))}
        </div>
    );
}

function Analysis({ analysis }) {
    if (!analysis) return null;

    const scoreClass = analysis.overall_score >= 8
        ? "score-green"
        : analysis.overall_score >= 5 ? "score-yellow" : "score-red";

    return (
        <>
            <div className="header">
                <h1>{analysis.symbol}</h1>
                <h2 className={`badge ${analysis.recommendation.toLowerCase()}`}>
                    {analysis.recommendation}
                </h2>
                <h3>Overall Score:
                    <span className={scoreClass}> {analysis.overall_score}/10</span>
                </h3>
                <p className="metadata">
                    Confidence: {analysis.overall_confidence.level} · Model: {analysis.scoring_model_version}
                </p>
            </div>

            {analysis.warnings?.length > 0 && (
                <div className="warning-message">
                    {analysis.warnings.map((warning) => <p key={warning}>⚠ {warning}</p>)}
                </div>
            )}

            <div className="cards">
                <MetricsCard title="Business Quality" section={analysis.business_quality} />
                <MetricsCard title="Valuation" section={analysis.valuation} />
            </div>

            <div className="section">
                <h2>Strengths</h2>
                {analysis.strengths.length === 0 ? <p>None</p> : analysis.strengths.map((item) => (
                    <p className="green" key={item}>✓ {item}</p>
                ))}
            </div>

            <div className="section">
                <h2>Weaknesses</h2>
                {analysis.weaknesses.length === 0 ? <p>None</p> : analysis.weaknesses.map((item) => (
                    <p className="red" key={item}>✗ {item}</p>
                ))}
            </div>
        </>
    );
}

export default Analysis;
