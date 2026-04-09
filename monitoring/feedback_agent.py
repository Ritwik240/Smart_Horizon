
# 6. MONITORING + FEEDBACK AGENT
import ollama

# GLOBAL MEMORY
history = []
performance_log = []

def monitoring_agent(data, risks, plan, actions):
    global history, performance_log

    # INPUT EXTRACTION
    soil = data["sensor_data"]["soil_moisture"]
    temp = data["sensor_data"]["temperature"]
    rain = data["weather"]["rain_forecast"]

    status = "normal"
    feedback = []
    updated_plan = plan.copy()
    escalation = False

    # 1. STATUS DETECTION
  
    if "water_stress" in risks:
        feedback.append("Low soil moisture detected")
        status = "alert"

    if "heat_stress" in risks:
        feedback.append("High temperature detected")
        status = "alert"

    if not feedback:
        feedback.append("Conditions are within optimal range")

    # 2. TREND ANALYSIS
  
    trend = "no_data"

    if len(history) > 0:
        last = history[-1]

        if soil > last["soil"]:
            trend = "improving"
        elif soil < last["soil"]:
            trend = "worsening"
        else:
            trend = "stable"

    # 3. CONTEXT-AWARE LEARNING
    performance = "neutral"

    if trend == "improving":
        performance = "success"

    elif trend == "worsening":

        #Environmental factor: rain
        if rain:
            performance = "environmental"
            feedback.append("Moisture change influenced by rainfall")

        #Environmental factor: extreme heat
        elif temp > 38:
            performance = "environmental"
            feedback.append("Extreme heat affecting soil moisture")

        #True failure
        else:
            performance = "failure"

    else:
        performance = "stable"

    performance_log.append(performance)
    # 4. SMART PLAN UPDATE
    if performance == "failure":
        updated_plan.append("Increase irrigation duration")
        feedback.append("Previous plan ineffective → increasing irrigation")

    elif performance == "environmental":
        updated_plan.append("Adjust irrigation timing (early morning/evening)")
        feedback.append("Adjusting plan due to environmental stress")

    elif performance == "success":
        feedback.append("Plan is effective → continue current strategy")
        
    # 5. SMART ESCALATION
   
    # Only count TRUE failures
    recent_failures = [p for p in performance_log[-3:] if p == "failure"]

    if len(recent_failures) >= 2:
        escalation = True
        feedback.append("Repeated failures detected → escalate to expert")

    # 6. STORE MEMORY
    history.append({
        "soil": soil,
        "temperature": temp,
        "trend": trend,
        "performance": performance
    })

    # 7. LLM ADVICE (SAFE FALLBACK)
    prompt = f"""
You are an agricultural expert.

Farm Data:
- Soil Moisture: {soil}%
- Temperature: {temp}°C
- Rain Forecast: {rain}

Trend: {trend}
Performance: {performance}

Current Plan: {', '.join(plan)}
Updated Plan: {', '.join(updated_plan)}

Give short, practical, farmer-friendly advice.
"""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        advice = response["message"]["content"]
    except:
        advice = "[LLM unavailable] Follow updated plan."

    # 8. RETURN STRUCTURED OUTPUT
    return {
        "status": status,
        "feedback": feedback,
        "trend": trend,
        "performance": performance,
        "updated_plan": updated_plan,
        "escalation": escalation,
        "advice": advice
    }
