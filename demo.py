"""
Demo: Constraint Optimization Agent
====================================
Run with: python demo.py
"""

from datetime import datetime, timedelta
from agent import (
    ConstraintOptimizationAgent,
    RiskSignal, WeatherWindow, FieldConstraints, ActionType
)
from data_adapters import TeammateRiskAdapter, WeatherAdapter
import json

def run_demo():
    print("\n" + "="*60)
    print("   FARM CONSTRAINT OPTIMIZATION AGENT — DEMO")
    print("="*60 + "\n")

    # ── Step 1: Simulate teammate sensor/imagery outputs ──────
    sensor_output = {
        "field_id": "FIELD_001",
        "soil_moisture_percent": 16.0,   # Dry! threshold=25
        "ndvi": 0.35,                    # Low vegetation health
        "temperature_c": 36.5,
    }
    imagery_output = {
        "field_id": "FIELD_001",
        "pest_detection_score": 0.78,    # High pest risk
        "disease_detection_score": 0.30,
    }

    risks = []
    risks += TeammateRiskAdapter.from_sensor_agent(sensor_output)
    risks += TeammateRiskAdapter.from_imagery_agent(imagery_output)

    print(f"[Input] Risks detected: {len(risks)}")
    for r in risks:
        print(f"  • {r.risk_type.upper()} | Severity: {r.severity:.2f} | Confidence: {r.confidence:.2f}")

    # ── Step 2: Mock weather windows ──────────────────────────
    now = datetime.utcnow()
    weather_windows = [
        WeatherWindow(
            field_id="FIELD_001",
            start_time=now + timedelta(hours=1),
            end_time=now + timedelta(hours=5),
            wind_speed_kmh=10.0,
            rain_probability=0.05,
            temperature_c=30.0,
            is_spray_safe=True,
            is_irrigation_needed=True,
        ),
        WeatherWindow(
            field_id="FIELD_001",
            start_time=now + timedelta(hours=8),
            end_time=now + timedelta(hours=12),
            wind_speed_kmh=22.0,          # Too windy for spraying
            rain_probability=0.40,
            temperature_c=27.0,
            is_spray_safe=False,
            is_irrigation_needed=False,
        ),
    ]

    # ── Step 3: Define field constraints ─────────────────────
    constraints = FieldConstraints(
        field_id="FIELD_001",
        total_budget_inr=8000,
        max_water_liters=12000,
        crop_stage="vegetative",
        area_hectares=2.5,
        forbidden_actions=[ActionType.HARVEST],  # Not harvest time
        priority=1,
    )

    print(f"\n[Constraints] Budget: ₹{constraints.total_budget_inr} | Water: {constraints.max_water_liters}L | Area: {constraints.area_hectares} ha")

    # ── Step 4: Run the optimization agent ───────────────────
    agent = ConstraintOptimizationAgent()
    plan = agent.run(risks, weather_windows, constraints)

    # ── Step 5: Print results ─────────────────────────────────
    print("\n" + "─"*60)
    print(f"[OPTIMIZED PLAN] Field: {plan.field_id}")
    print(f"  Status           : {plan.optimization_status}")
    print(f"  Total Cost       : ₹{plan.total_cost_inr:,.0f}")
    print(f"  Total Water      : {plan.total_water_liters:,.0f} L")
    print(f"  Expected Risk ↓  : {plan.expected_risk_reduction:.1%}")
    print(f"  Actions Selected : {len(plan.selected_actions)}")

    print("\n  Recommended Actions:")
    for i, action in enumerate(plan.selected_actions, 1):
        print(f"  {i}. {action.action_type.value.upper()}")
        print(f"     Cost: ₹{action.cost_inr:,.0f} | Water: {action.water_liters:.0f}L")
        print(f"     Window: {action.time_window_start.strftime('%H:%M')} → {action.time_window_end.strftime('%H:%M')} UTC")
        print(f"     Notes: {action.notes}")

    if plan.warnings:
        print("\n  ⚠ Warnings:")
        for w in plan.warnings:
            print(f"    - {w}")

    # ── Step 6: JSON output (for orchestration layer) ─────────
    print("\n  JSON Output (for orchestrator):")
    print(json.dumps(plan.to_dict(), indent=2))


if __name__ == "__main__":
    run_demo()
