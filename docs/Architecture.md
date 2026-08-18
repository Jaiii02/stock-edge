# StockEdge Architecture

## Current Architecture

User
↓
Stock Symbol
↓
Peer Group Engine
↓
Fundamental Engine
↓
Technical Engine
↓
Verdict Engine
↓
API Response

---

# Target Architecture

User
↓
Stock Symbol
↓
Peer Group Engine
↓
Fundamental Layer
↓
Technical Layer
↓
Macro Layer
↓
Explainability Layer
↓
Confidence Engine
↓
Verdict Engine
↓
React Frontend

---

# Peer Group Logic

Input Stock

↓

Find Industry

↓

Find Market Cap Band

↓

Construct Peer Universe

↓

Run Scoring

---

# Scoring Logic

Fundamental Score
60%

Technical Score
25%

Macro Score
15%

↓

Combined Score

↓

Verdict

Buy / Watch / Avoid

---

# Output Structure

Fundamental Score

Technical Score

Macro Environment

Strengths

Weaknesses

Confidence

Verdict