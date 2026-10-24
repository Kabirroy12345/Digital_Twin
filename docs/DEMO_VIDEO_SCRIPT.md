<!--
================================================================================
PulmoTwin: Multimodal Cardiopulmonary Digital Twin (Happiest Health Summit 2026)
Team Lead: Kabir Roy (rakeshkabir@gmail.com) | Digital Twin Challenge 2026
Updated: October 2026 • Certified Clean Submission
================================================================================
-->

# 🎥 PulmoTwin: Minimum 20-Minute Official Demo Walkthrough & Video Script
### Happiest Health — Digital Twin Challenge 2026
**Summit**: Reimagining & Reforming Healthcare in India Summit 2026, Bengaluru  
**Project**: PulmoTwin — Multimodal Cardiopulmonary Digital Twin for Proactive Adverse Event Forecasting & Personalized Clinical Intervention  
**Team**: Kabir Roy (Team Lead, rakeshkabir@gmail.com)  
**Official Video Link**: [https://www.youtube.com/watch?v=i7NJstq8_ZE](https://www.youtube.com/watch?v=i7NJstq8_ZE)  
**Live Interactive Cockpit**: [https://kabirroy12345.github.io/Digital_Twin/](https://kabirroy12345.github.io/Digital_Twin/)  

---

## 📺 Video Overview & Timestamps (Total Duration: 21:00)

| Timestamp | Phase | Topic Covered | On-Screen Action |
|:---|:---|:---|:---|
| **00:00 – 02:30** | **Part 1: The Healthcare Crisis in India** | India's 37.9M asthma burden & reactive healthcare failure | Opening title slide, urban smog statistics, Delhi/Bengaluru AQI spikes |
| **02:30 – 05:00** | **Part 2: Two Data Streams Fusion** | Virtual patient replica concept: Longitudinal EHR + Wearables/IoT | Architecture diagram, FHIR R4 / ABDM schema & wearable ingestion pipeline |
| **05:00 – 08:00** | **Part 3: Live System Walkthrough** | Warm Ivory web UI overview, Open-Meteo GPS sync, bilingual intake | Overview navigation, live GPS sync, patient vitals & 2-way GINA synthesis |
| **08:00 – 11:00** | **Part 4: Real-Time Wearable Telemetry** | Continuous PPG (HR, HRV, SpO2, Resp Rate, PEF) & BLE Smart Inhaler | Live wearable telemetry stream, autonomic stress index, zone badges |
| **11:00 – 13:30** | **Part 5: 24-Hour Forward Simulation** | Predicting acute adverse events before onset | Interactive trajectory graph, airway resistance ($R_{aw}$), decompensation timing |
| **13:30 – 16:00** | **Part 6: Counterfactual "What-If" Engine** | In silico clinical testing of interventions | "What-If" sandbox: HEPA air purifier vs prophylactic MART inhaler comparison |
| **16:00 – 18:00** | **Part 7: Safety Rails & HITL Governance** | GINA clinical rules, DPDP Act 2023 compliance, 108/112 SOS | Live test of acute emergency phrase in Hindi ("सांस नहीं आ रही") & SOS protocol |
| **18:00 – 21:00** | **Part 8: Dynamic Physician Console & CDS** | Real-time cohort triage, sign-off queue, Bengaluru sensor grid | Dr. Sarah Mitchell console, GINA 2026 matrix, clinical PDF download, wrap-up |

---

## Detailed Spoken Script & Screen Directions

### [00:00 – 02:15] Part 1: Problem Statement & Clinical Motivation
**Screen**: High-resolution opening slide showing PulmoTwin branding, Happiest Health Summit logo, and Indian urban air pollution statistics.
> **Narrator**:  
> *"Hello esteemed members of the Happiest Health jury, faculty mentors, and fellow innovators. Welcome to our presentation of **PulmoTwin** for the Digital Twin Challenge 2026.*  
> *Today in India, over 37.9 million people suffer from bronchial asthma, and chronic obstructive pulmonary diseases are the second leading cause of mortality. Yet across our metros and tier-2 cities, healthcare remains fundamentally **reactive**. Patients check the Air Quality Index only after coughing or chest tightness begins. By the time wheezing escalates into severe nocturnal dyspnea, airway resistance has already surged by over 400%, and the patient lands in an emergency room.*  
> *The central thesis of our project answers the call of the Happiest Health Summit: **The future of medicine must be proactive, not reactive.** Today, we present PulmoTwin: a dynamic, multimodal physiological Digital Twin that simulates patient respiratory and autonomic dynamics, forecasting acute adverse health events 4 to 24 hours before they happen."*

---

### [02:15 – 04:30] Part 2: What is PulmoTwin? Architectural Foundation
**Screen**: Mermaid/PDF Architecture diagram highlighting the three pillars: EHR Prior, Wearable Stream, and Dynamic Physical Simulation.
> **Narrator**:  
> *"What exactly is a Digital Twin in healthcare? It is not just a statistical classifier or a passive dashboard. It is a **living computational replica** of an individual human's physiology.*  
> *PulmoTwin integrates three foundational data streams:*  
> *1. **Longitudinal Electronic Health Records (EHR)**: Modeled strictly on Ayushman Bharat Digital Mission (ABDM) and HL7 FHIR R4 standards. It ingests baseline spirometry (FEV1, FVC, personal best PEF), inflammatory biomarkers like blood eosinophils and FeNO, documented allergens, and past exacerbation histories.*  
> *2. **Real-Time Wearable Telemetry**: Continuous photoplethysmography (PPG) capturing Heart Rate, Heart Rate Variability (rMSSD), blood oxygen saturation (SpO2), respiratory rate, and connected BLE smart inhaler actuation logs.*  
> *3. **Hyperlocal Atmospheric Telemetry**: Real-time 48-hour environmental dispersion data via Open-Meteo APIs tracking PM2.5, PM10, Nitrogen Dioxide, Sulphur Dioxide, Ozone, and ambient thermal inversion layers."*

---

### [04:30 – 07:15] Part 3: Live Application Walkthrough & User Experience
**Screen**: Switch to browser at `http://localhost:7860`. Show the modern, responsive Editorial design system.
> **Narrator**:  
> *"Let us transition into the live working prototype. Here on our dashboard, we see patient Kabir Roy, a 28-year-old software engineer living in New Delhi diagnosed with moderate persistent asthma.*  
> *Notice our top status pill: PulmoTwin is synchronizing in real time with the Open-Meteo atmospheric monitoring network for Delhi coordinates. Ambient AQI is currently 178 with PM2.5 at 82.4 µg/m³. The system instantly calculates the patient's **Safest Daylight Window**—today between 06:30 and 08:30 AM—when particulate settling is minimal.*  
> *Notice the bilingual toggle: with a single click, our entire interface, clinical prompts, and alert dialogues dynamically translate between English and Hindi, ensuring accessibility across India's linguistic diversity."*

---

### [07:15 – 10:00] Part 4: Real-Time Wearable Telemetry & Physiological Metrics
**Screen**: Zoom into the Digital Twin Vitals Panel. Show continuous telemetry gauges for Heart Rate, SpO2, Respiratory Rate, and Peak Expiratory Flow.
> **Narrator**:  
> *"Now let us examine the core physiological engine. Unlike generic health apps, PulmoTwin models underlying biomechanical parameters:*  
> *- **Airway Resistance ($R_{aw}$)**: Currently calibrated at 2.85 cmH₂O/(L/s), moderately elevated above normal baseline.*  
> *- **Dynamic Lung Compliance ($C_{dyn}$)**: 58.2 mL/cmH₂O.*  
> *- **Autonomic Sympathetic Tone**: Derived from real-time HRV (rMSSD). Notice that as particulate exposure intensifies, HRV drops while heart rate elevates—a known autonomic precursor to bronchospasm.*  
> *- **Smart Inhaler Telemetry**: PulmoTwin tracks canister dose countdown and inhalation technique via connected sensor telemetry."*

---

### [10:00 – 12:45] Part 5: 24-Hour Forward Physiological Projection
**Screen**: Scroll to the "24-Hour Predictive Trajectory" interactive chart. Hover over the evening hours showing the risk spike.
> **Narrator**:  
> *"Here is the defining capability of our Digital Twin: **Forward Predictive Simulation**.*  
> *Looking at the 24-hour horizon, ambient PM2.5 is forecasted to spike from 85 to 215 µg/m³ between 18:00 and 22:00 due to winter evening temperature inversions. Using differential equations of airway inflammation and clearance kinetics, the Digital Twin projects Kabir's physiological state forward in time.*  
> *Notice: At 19:00, without intervention, his airway resistance is projected to cross 6.5 cmH₂O/(L/s), dropping his PEF below 60% and pushing his **Exacerbation Risk Index (ERI)** into the RED zone at 0.82.*  
> *Crucially: PulmoTwin identifies this crisis **8 hours before it occurs**, providing actionable lead time for preventative intervention."*

---

### [12:45 – 15:15] Part 6: Counterfactual "What-If" Simulation Engine
**Screen**: Toggle the "What-If Simulation Sandbox". Enable "Indoor HEPA Air Purifier" and "Proactive Reliever Inhaler (2 Puffs)", then click "Run Simulation".
> **Narrator**:  
> *"How do we prevent this predicted event? In our **Counterfactual Sandbox**, clinicians and patients can test interventions virtually before applying them physically.*  
> *Let us simulate Scenario A: The patient stays indoors with a HEPA air purifier active during the 18:00–21:00 smog peak. Let us also test Scenario B: Taking 2 puffs of prescribed Budesonide/Formoterol maintenance inhaler at 17:00.*  
> *We click 'Run Counterfactual Simulation'. Instantly, the twin plots the comparative trajectories side-by-side. Notice the result: Under the combined intervention, the peak Exacerbation Risk Index collapses from 0.82 down to 0.28—a **65.8% reduction in acute risk**! Airway resistance remains safe in the green zone throughout the night."*

---

### [15:15 – 16:45] Part 7: Deterministic Clinical Safety Rails & Human-in-the-Loop Governance
**Screen**: Open the chat assistant. Type or voice input in Hindi: *"सांस नहीं आ रही है, इनहेलर काम नहीं कर रहा"* ("Cannot breathe, inhaler is not working").
> **Narrator**:  
> *"In healthcare AI, patient safety is paramount. PulmoTwin rejects the unpredictability of black-box LLMs. We implement **Deterministic Dual-Layer Safety Rails**.*  
> *Let us demonstrate: I will enter an acute emergency distress phrase in Hindi: 'सांस नहीं आ रही है, इनहेलर काम नहीं कर रहा'.*  
> *Observe: The system **completely bypasses the LLM**. Zero API latency. It immediately triggers the Red-Flag Emergency Protocol, displays immediate upright posture and rescue instructions in Hindi, and provides direct one-tap calling buttons for **108 Ambulance** and **112 Emergency Dispatch**.*  
> *Furthermore, for routine external actions—such as dispatching an SMS alert to a caregiver or adjusting a calendar—all actions are held in a **Zero-Trust Human Approval Queue**. The agent proposes; the patient retains sovereign authority to approve or decline."*

---

### [16:45 – 18:30] Part 8: Clinical Consultation Summary & The Summit Vision
**Screen**: Click "Generate Doctor Consultation Summary (PDF)". Open the generated ReportLab PDF showing standardized GINA metrics.
> **Narrator**:  
> *"Finally, PulmoTwin closes the loop with the physician. With one tap, it synthesizes a 30-day longitudinal clinical report formatted as a clean, standardized PDF for outpatient consultation.*  
> *It details 30-day symptom episodes, total reliever puffs used, peak flow dynamics, and environmental trigger correlations—empowering doctors to accurately calibrate GINA Step therapy without relying on imperfect patient recall.*  
> *In summary, PulmoTwin demonstrates that when we combine longitudinal EHR baselines, streaming wearable vitals, and predictive physiological simulation, we can transform chronic respiratory care across India from reactive crisis management into proactive prevention.*  
> *Thank you, Happiest Health, for championing the Digital Twin Challenge 2026. We look forward to meeting the jury at the Bengaluru Summit!"*

---
*(End of Video)*
