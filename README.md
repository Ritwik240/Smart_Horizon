# Constraint Optimization Agent
## SH-AGR-001 — Autonomous Farm-to-Field Advisory System

---

## What This Agent Does
Receives **risk signals** (from sensor / weather / imagery agents) and outputs
an **optimized action plan** per field — selecting the best combination of
actions (irrigate, fertilize, spray, scout) within hard constraints:

| Constraint | Source |
|---|---|
| Budget (₹) | Farm operator input |
| Water quota (L) | Irrigation authority / operator |
| Weather window | OpenWeatherMap API |
| Crop stage rules | Agronomy knowledge base |
| Safe spray conditions | Wind speed + rain probability |
| Time-window non-overlap | ILP constraint |

---

## File Structure
```
constraint_optimization_agent/
├── agent.py            ← Core ILP optimization engine
├── data_adapters.py    ← API connectors + teammate interfaces
├── demo.py             ← End-to-end demo
├── requirements.txt    ← Python dependencies
└── README.md
```

---

## Quick Start
```bash
pip install -r requirements.txt
python demo.py
```

---

## Integration with Teammate Modules

### If your teammate outputs sensor data:
```python
from data_adapters import TeammateRiskAdapter
risks = TeammateRiskAdapter.from_sensor_agent(sensor_output_dict)
```

### If your teammate outputs imagery/drone data:
```python
risks += TeammateRiskAdapter.from_imagery_agent(imagery_output_dict)
```

### Then run the optimizer:
```python
from agent import ConstraintOptimizationAgent, FieldConstraints
agent = ConstraintOptimizationAgent()
plan = agent.run(risks, weather_windows, constraints)
print(plan.to_dict())   # JSON-serializable output
```

---

## Real-Time APIs Required

| API | Use | Cost | Key Required |
|---|---|---|---|
| [OpenWeatherMap](https://openweathermap.org/api) | Weather windows | Free (1000 calls/day) | ✅ Register free |
| [NASA POWER](https://power.larc.nasa.gov/) | ET₀, solar radiation | Free | ❌ No key |
| [data.gov.in](https://data.gov.in/) | Mandi market prices | Free | ✅ Register free |
| [SoilGrids](https://rest.isric.org/soilgrids/v2.0/) | Soil nutrient data | Free | ❌ No key |
| [Sentinel Hub](https://www.sentinel-hub.com/) | Satellite NDVI | Freemium | ✅ Free trial |
| [IMD](https://mausam.imd.gov.in/) | India weather data | Free | Request access |

### .env file (create this):
```
OPENWEATHER_API_KEY=your_key_here
DATA_GOV_IN_API_KEY=your_key_here
SENTINEL_HUB_CLIENT_ID=your_id
SENTINEL_HUB_CLIENT_SECRET=your_secret
```

---

## Output Schema (JSON)
```json
{
  "field_id": "FIELD_001",
  "actions": [
    {
      "type": "irrigate",
      "cost_inr": 2000,
      "water_liters": 12500,
      "start": "2024-06-01T05:00:00",
      "end": "2024-06-01T09:00:00",
      "notes": "Risk: water_stress | Severity: 0.64"
    }
  ],
  "total_cost_inr": 5750,
  "total_water_liters": 12500,
  "expected_risk_reduction": 0.812,
  "status": "Optimal",
  "warnings": [],
  "generated_at": "2024-06-01T04:30:00"
}
```

---

## How to Extend

**Add a new action type:**
1. Add to `ActionType` enum in `agent.py`
2. Add cost/water to `ActionGenerator.ACTION_COSTS`
3. Map it in `ActionGenerator.RISK_ACTION_MAP`

**Add a new constraint (e.g., labor hours):**
```python
# In ConstraintOptimizationEngine.optimize():
prob += lpSum(candidates[i].duration_hours * x[i] for i in range(n)) <= max_labor_hours
```

**Expose as REST API (FastAPI):**
```python
from fastapi import FastAPI
from agent import ConstraintOptimizationAgent
app = FastAPI()

@app.post("/optimize")
def optimize(payload: dict):
    # parse payload → run agent → return plan.to_dict()
    ...
```
