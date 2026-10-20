"""
Injects the Digital Twin view, navigation button, and JavaScript controllers into web_ui/index.html.
"""

import shutil

NAV_BUTTON = """        <button class="nav-btn" id="nav-digital-twin" onclick="switchView('digital-twin'); initDigitalTwinView();" style="color: #0284c7; font-weight: 700;"><i class="fa-solid fa-heart-pulse"></i> Digital Twin</button>
"""

DIGITAL_TWIN_VIEW = """
    <!-- ==================== DIGITAL TWIN MULTIMODAL VIEW ==================== -->
    <section id="view-digital-twin" class="view-section">
      <!-- Digital Twin Header Banner -->
      <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1.5rem;">
          <div>
            <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(2, 132, 199, 0.2); border: 1px solid #0284c7; color: #38bdf8; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">
              <i class="fa-solid fa-microchip"></i> Digital Twin Challenge 2026 • Happiest Health Showcase
            </div>
            <h2 style="font-size: 1.85rem; font-weight: 800; margin: 0 0 0.5rem 0; letter-spacing: -0.02em;">🫁 PulmoTwin: Cardiopulmonary Virtual Replica</h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin: 0; max-width: 650px; line-height: 1.5;">
              Dynamic patient physiology simulation pairing continuous wearable telemetry with ABDM/FHIR longitudinal health records. Predicts acute adverse respiratory exacerbations 4 to 24 hours before onset.
            </p>
          </div>
          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <button id="btn-refresh-dt" class="btn-dt" aria-label="Sync Telemetry" onclick="refreshDigitalTwinData()" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 8px; font-weight: 600; font-size: 0.85rem; cursor: pointer; display: flex; align-items: center; gap: 6px;">
              <i class="fa-solid fa-arrows-rotate"></i> Sync Telemetry
            </button>
            <a href="/docs/Digital_Twin_Challenge_2026_Pitch_Deck.pdf" target="_blank" style="background: #0284c7; color: white; padding: 8px 16px; border-radius: 8px; font-weight: 600; font-size: 0.85rem; text-decoration: none; display: flex; align-items: center; gap: 6px;">
              <i class="fa-solid fa-file-pdf"></i> Pitch Deck (PDF)
            </a>
          </div>
        </div>

        <!-- Patient Demographics Ribbon -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);">
          <div>
            <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Virtual Patient</div>
            <div style="font-weight: 700; font-size: 1rem;" id="dt-patient-name">Kabir Roy (Age 28, Male)</div>
          </div>
          <div>
            <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">ABHA ID / EHR</div>
            <div style="font-weight: 700; font-size: 1rem; color: #38bdf8;">91-4582-7819-2041</div>
          </div>
          <div>
            <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Baseline Spirometry</div>
            <div style="font-weight: 700; font-size: 1rem;">FEV1: 68.5% (PB: 450 L/m)</div>
          </div>
          <div>
            <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Current Twin Status</div>
            <div style="font-weight: 700; font-size: 1rem; color: #10b981;" id="dt-status-badge">STABLE / CONTROLLED</div>
          </div>
        </div>
      </div>

      <!-- Real-Time Wearable Telemetry Stream Gauges -->
      <h3 style="font-size: 1.25rem; font-weight: 700; color: #0f172a; margin-bottom: 1rem; display: flex; align-items: center; gap: 8px;">
        <i class="fa-solid fa-satellite-dish" style="color: #0284c7;"></i> Live Wearable Telemetry Stream
        <span style="font-size: 0.75rem; font-weight: 600; background: #ecfdf5; color: #059669; padding: 2px 8px; border-radius: 12px; border: 1px solid #a7f3d0;">
          <i class="fa-solid fa-circle" style="font-size: 6px; animation: pulse 1.5s infinite;"></i> STREAMING
        </span>
      </h3>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
        <!-- Heart Rate -->
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <div style="display: flex; justify-content: space-between; align-items: center; color: #64748b; font-size: 0.85rem; margin-bottom: 0.5rem;">
            <span>Heart Rate (PPG)</span>
            <i class="fa-solid fa-heart" style="color: #ef4444;"></i>
          </div>
          <div style="font-size: 1.85rem; font-weight: 800; color: #0f172a;" id="dt-val-hr">74 <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">bpm</span></div>
          <div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;">Normal Sinus Rhythm</div>
        </div>

        <!-- SpO2 -->
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <div style="display: flex; justify-content: space-between; align-items: center; color: #64748b; font-size: 0.85rem; margin-bottom: 0.5rem;">
            <span>Blood Oxygen (SpO2)</span>
            <i class="fa-solid fa-droplet" style="color: #0284c7;"></i>
          </div>
          <div style="font-size: 1.85rem; font-weight: 800; color: #0f172a;" id="dt-val-spo2">98.2 <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">%</span></div>
          <div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;">Optimal Oxygenation</div>
        </div>

        <!-- Respiratory Rate -->
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <div style="display: flex; justify-content: space-between; align-items: center; color: #64748b; font-size: 0.85rem; margin-bottom: 0.5rem;">
            <span>Respiratory Rate</span>
            <i class="fa-solid fa-lungs" style="color: #8b5cf6;"></i>
          </div>
          <div style="font-size: 1.85rem; font-weight: 800; color: #0f172a;" id="dt-val-rr">16 <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">brpm</span></div>
          <div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;">Eupneic / Controlled</div>
        </div>

        <!-- Peak Flow PEF -->
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <div style="display: flex; justify-content: space-between; align-items: center; color: #64748b; font-size: 0.85rem; margin-bottom: 0.5rem;">
            <span>Peak Flow (PEF)</span>
            <i class="fa-solid fa-wind" style="color: #10b981;"></i>
          </div>
          <div style="font-size: 1.85rem; font-weight: 800; color: #0f172a;" id="dt-val-pef">385 <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">L/min</span></div>
          <div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;" id="dt-val-zone">GREEN ZONE (85.5% PB)</div>
        </div>
      </div>

      <!-- Physiological State & Biomechanics -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #0f172a; font-weight: 700;">
            <i class="fa-solid fa-dna" style="color: #0284c7;"></i> Virtual Organ Biomechanics
          </h4>
          <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 8px 0; color: #64748b;">Airway Resistance (R<sub>aw</sub>)</td>
              <td style="padding: 8px 0; font-weight: 700; text-align: right;" id="dt-raw">2.15 cmH2O/(L/s)</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 8px 0; color: #64748b;">Dynamic Lung Compliance (C<sub>dyn</sub>)</td>
              <td style="padding: 8px 0; font-weight: 700; text-align: right;" id="dt-cdyn">64.5 mL/cmH2O</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 8px 0; color: #64748b;">Alveolar-Arterial O2 Gradient (A-a DO2)</td>
              <td style="padding: 8px 0; font-weight: 700; text-align: right;" id="dt-aado2">12.4 mmHg</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 8px 0; color: #64748b;">Autonomic Sympathetic Tone</td>
              <td style="padding: 8px 0; font-weight: 700; text-align: right;" id="dt-sympathetic">0.22 (Relaxed)</td>
            </tr>
            <tr>
              <td style="padding: 8px 0; color: #64748b;">Exacerbation Risk Index (ERI)</td>
              <td style="padding: 8px 0; font-weight: 700; text-align: right; color: #10b981;" id="dt-eri">0.24 (Controlled)</td>
            </tr>
          </table>
        </div>

        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #0f172a; font-weight: 700;">
            <i class="fa-solid fa-hospital-user" style="color: #0284c7;"></i> Longitudinal ABDM EHR Baseline
          </h4>
          <div style="font-size: 0.88rem; line-height: 1.6; color: #334155;">
            <div><b>Primary Diagnosis:</b> Moderate Persistent Bronchial Asthma (ICD-10 J45.40)</div>
            <div><b>Comorbidities:</b> Allergic Rhinitis (Moderate), GERD (Mild)</div>
            <div><b>Blood Eosinophils:</b> 380 / µL (High Eosinophilic Phenotype)</div>
            <div><b>Fractional Exhaled Nitric Oxide (FeNO):</b> 42.0 ppb</div>
            <div><b>Current Regimen:</b> Budesonide + Formoterol 200/6 mcg DPI (SMART)</div>
            <div style="margin-top: 0.75rem; padding: 6px 12px; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.8rem; color: #64748b;">
              <i class="fa-solid fa-shield-halved"></i> ABDM Care Context: Connected via HL7 FHIR R4 Bundle
            </div>
          </div>
        </div>
      </div>

      <!-- Counterfactual "What-If" Simulation Sandbox -->
      <div style="background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.75rem; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.25rem;">
          <div>
            <h4 style="margin: 0; font-size: 1.2rem; font-weight: 800; color: #0f172a;">
              <i class="fa-solid fa-flask-vial" style="color: #0284c7;"></i> Counterfactual "What-If" Simulation Sandbox
            </h4>
            <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.85rem;">
              Test candidate interventions in virtual reality to simulate outcomes before applying them physically.
            </p>
          </div>
          <button id="btn-run-whatif" class="btn-dt" aria-label="Run What If Simulation" onclick="executeWhatIfSimulation()" style="background: #0284c7; color: white; border: none; padding: 9px 18px; border-radius: 8px; font-weight: 700; font-size: 0.9rem; cursor: pointer; display: flex; align-items: center; gap: 6px;">
            <i class="fa-solid fa-play"></i> Run Simulation
          </button>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
          <label style="display: flex; align-items: flex-start; gap: 10px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; cursor: pointer;">
            <input type="checkbox" id="whatif-hepa" checked style="margin-top: 3px;">
            <div>
              <div style="font-weight: 700; font-size: 0.9rem; color: #0f172a;">Indoor HEPA Filter</div>
              <div style="font-size: 0.75rem; color: #64748b;">Reduces effective PM2.5 exposure by 75% between 18:00 and 22:00</div>
            </div>
          </label>

          <label style="display: flex; align-items: flex-start; gap: 10px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; cursor: pointer;">
            <input type="checkbox" id="whatif-inhaler" checked style="margin-top: 3px;">
            <div>
              <div style="font-weight: 700; font-size: 0.9rem; color: #0f172a;">Proactive SMART Inhaler</div>
              <div style="font-size: 0.75rem; color: #64748b;">2 puffs Formoterol/Budesonide taken at 17:00 prior to smog spike</div>
            </div>
          </label>

          <label style="display: flex; align-items: flex-start; gap: 10px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; cursor: pointer;">
            <input type="checkbox" id="whatif-exercise" style="margin-top: 3px;">
            <div>
              <div style="font-weight: 700; font-size: 0.9rem; color: #0f172a;">Reschedule Evening Run</div>
              <div style="font-size: 0.75rem; color: #64748b;">Shift exercise to morning safe window (06:30 - 08:30)</div>
            </div>
          </label>
        </div>

        <!-- Simulation Comparison Output -->
        <div id="whatif-results-box" style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 1rem; color: #166534; font-size: 0.9rem;">
          <div style="font-weight: 700; margin-bottom: 0.25rem;">
            <i class="fa-solid fa-circle-check"></i> Simulation Result: Combined Proactive Protocol Selected
          </div>
          <div id="whatif-results-text">
            Simulated trajectory demonstrates a <b>66.7% reduction in peak adverse exacerbation risk</b> (ERI collapses from 0.84 RED down to 0.28 GREEN). Airway resistance is maintained safely below 3.0 cmH2O/(L/s) throughout the night.
          </div>
        </div>
      </div>
    </section>
"""

JS_CONTROLLER = """
    // ==================== DIGITAL TWIN CONTROLLER ====================
    async function initDigitalTwinView() {
      await refreshDigitalTwinData();
    }

    async function refreshDigitalTwinData() {
      try {
        const res = await fetch('/api/digital-twin/state/1');
        const data = await res.json();
        if (data.success && data.digital_twin) {
          const dt = data.digital_twin;
          const p = dt.physiological_metrics;
          const w = dt.wearable_telemetry;
          const s = dt.digital_twin_status;

          document.getElementById('dt-patient-name').innerText = `${dt.patient_name} (Age ${dt.age}, Male)`;
          document.getElementById('dt-val-hr').innerHTML = `${w.heart_rate_bpm} <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">bpm</span>`;
          document.getElementById('dt-val-spo2').innerHTML = `${w.spo2_percent} <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">%</span>`;
          document.getElementById('dt-val-rr').innerHTML = `${w.respiratory_rate_brpm} <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">brpm</span>`;
          document.getElementById('dt-val-pef').innerHTML = `${w.current_pef_lpm} <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">L/min</span>`;
          document.getElementById('dt-val-zone').innerText = `${w.clinical_zone} (${w.pef_percent_predicted}% PB)`;

          document.getElementById('dt-raw').innerText = `${p.airway_resistance_cmH2O_L_s} cmH2O/(L/s)`;
          document.getElementById('dt-cdyn').innerText = `${p.dynamic_lung_compliance_mL_cmH2O} mL/cmH2O`;
          document.getElementById('dt-aado2').innerText = `${p.aa_oxygen_gradient_mmHg} mmHg`;
          document.getElementById('dt-sympathetic').innerText = `${p.sympathetic_autonomic_tone} (${p.sympathetic_autonomic_tone < 0.4 ? 'Relaxed' : 'Elevated'})`;
          document.getElementById('dt-eri').innerText = `${s.exacerbation_risk_index} (${s.clinical_status})`;
          document.getElementById('dt-eri').style.color = s.status_color;
          document.getElementById('dt-status-badge').innerText = s.clinical_status;
          document.getElementById('dt-status-badge').style.color = s.status_color;
        }
      } catch (err) {
        console.warn('Error fetching digital twin state:', err);
      }
    }

    async function executeWhatIfSimulation() {
      const useHepa = document.getElementById('whatif-hepa').checked;
      const useInhaler = document.getElementById('whatif-inhaler').checked;

      const scenarios = [
        {"name": "Custom Candidate Protocol", "use_hepa_filter": useHepa, "take_reliever": useInhaler, "doses": 2}
      ];

      try {
        const res = await fetch('/api/digital-twin/what-if/1', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({scenarios: scenarios})
        });
        const data = await res.json();
        if (data.success) {
          const summary = data.summary_recommendation;
          const box = document.getElementById('whatif-results-box');
          const text = document.getElementById('whatif-results-text');
          box.style.display = 'block';
          text.innerHTML = `<b>Virtual Twin Recommendation:</b> ${summary}`;
        }
      } catch (err) {
        console.warn('Error running what-if simulation:', err);
      }
    }
"""

def patch_frontend():
    with open("web_ui/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add nav button
    if 'id="nav-digital-twin"' not in html:
        agent_btn_marker = '<button class="nav-btn active" id="nav-agent"'
        html = html.replace(agent_btn_marker, NAV_BUTTON + agent_btn_marker, 1)

    # 2. Add Digital Twin view section
    if 'id="view-digital-twin"' not in html:
        user_view_marker = '<section id="view-user" class="view-section">'
        html = html.replace(user_view_marker, DIGITAL_TWIN_VIEW + "\n" + user_view_marker, 1)

    # 3. Add controller JS before closing </script>
    if "function initDigitalTwinView" not in html:
        closing_script = "</script>"
        # Insert before the last </script>
        last_idx = html.rfind(closing_script)
        if last_idx != -1:
            html = html[:last_idx] + JS_CONTROLLER + "\n" + html[last_idx:]

    with open("web_ui/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Also copy to root index.html
    shutil.copyfile("web_ui/index.html", "index.html")
    print("Frontend successfully updated with Digital Twin view and controllers!")

if __name__ == "__main__":
    patch_frontend()
