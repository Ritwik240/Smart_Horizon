import sys
import os
from datetime import datetime, timedelta

# Fix imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 🧠 PLANNER IMPORTS
from planner.agent import (
    ConstraintOptimizationAgent,
    RiskSignal,
    WeatherWindow,
    FieldConstraints
)

# 🌾 EXECUTOR
from executor.agents.executor_agent import executor_agent

# 👀 MONITORING
from monitoring.feedback_agent import monitoring_agent


def run_system():

    print("\n🚀 STARTING AGRI AGENT SYSTEM\n")

    # ─────────────────────────────────────
    # 1️⃣ SENSOR DATA (FIXED)
    # ─────────────────────────────────────

    sensor_data = {
        "soil_moisture": 35,
        "temperature": 32,   # ✅ REQUIRED for monitoring
        "air_temp": 32,      # ✅ REQUIRED for executor
        "humidity": 70,
        "nitrogen": 40,
        "phosphorus": 30,
        "potassium": 35,
        "soil_ph": 6.5
    }

    # ─────────────────────────────────────
    # 2️⃣ PLANNER INPUT
    # ─────────────────────────────────────

    risks = [
        RiskSignal(
            risk_type="water_stress",
            severity=0.8,
            affected_field_id="field_1",
            confidence=0.9
        ),
        RiskSignal(
            risk_type="nutrient_gap",
            severity=0.6,
            affected_field_id="field_1",
            confidence=0.85
        )
    ]

    weather_windows = [
        WeatherWindow(
            field_id="field_1",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=6),
            wind_speed_kmh=10,
            rain_probability=0.2,
            temperature_c=30,
            is_spray_safe=True,
            is_irrigation_needed=True
        )
    ]

    constraints = FieldConstraints(
        field_id="field_1",
        total_budget_inr=10000,
        max_water_liters=10000,
        crop_stage="vegetative",
        area_hectares=1.0
    )

    # ─────────────────────────────────────
    # 3️⃣ RUN PLANNER
    # ─────────────────────────────────────

    print("🧠 Running Planner...\n")

    planner = ConstraintOptimizationAgent()
    plan = planner.run(risks, weather_windows, constraints)

    plan_dict = plan.to_dict()

    print("📋 PLAN:")
    print(plan_dict)

    # ─────────────────────────────────────
    # 4️⃣ EXTRACT ACTIONS
    # ─────────────────────────────────────

    actions = [a["type"] for a in plan_dict["actions"]]

    print("\n⚙️ ACTIONS TO EXECUTE:")
    print(actions)

    # ─────────────────────────────────────
    # 5️⃣ RUN EXECUTOR
    # ─────────────────────────────────────

    print("\n🌾 Running Executor...\n")

    result = executor_agent(actions, sensor_data)

    print("✅ EXECUTION RESULT:")
    print(result)

    # ─────────────────────────────────────
    # 6️⃣ RUN MONITORING
    # ─────────────────────────────────────

    print("\n👀 Running Monitoring Agent...\n")

    feedback = monitoring_agent(
        data={
            "sensor_data": sensor_data,
            "weather": {"rain_forecast": 0.2}
        },
        risks=[r.risk_type for r in risks],
        plan=plan_dict,
        actions=result
    )

    print("📊 FEEDBACK:")
    print(feedback)

    print("\n🎯 SYSTEM COMPLETE\n")


if __name__ == "__main__":
    run_system()