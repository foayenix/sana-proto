# SANA Platform - Investor Demo Guide

This guide provides a step-by-step walkthrough for demonstrating the SANA Health Platform to investors and stakeholders.

---

## Pre-Demo Checklist

- [ ] Flutter app running on device/simulator
- [ ] Backend server running (optional - app uses mock data)
- [ ] Device in presentation mode (Do Not Disturb enabled)
- [ ] Screen sharing ready if presenting remotely

---

## Demo Flow (10-15 minutes)

### 1. Opening - The Problem (1 minute)

**Talking Point:** "Complementary and Alternative Medicine is a $100B+ market, but it lacks two critical things: measurable outcomes and practitioner credibility. SANA solves both."

### 2. Client Health Graph (2-3 minutes)

**Navigate to:** Health Graph tab

**Key Points:**
- **SANA Health Score**: "This is a holistic score across 6 wellness dimensions - physical, mental, emotional, social, sleep, and energy."
- **Radar Chart**: "Unlike single-metric health apps, we capture the full picture."
- **Biological Age**: "We calculate biological vs chronological age - this client is 38 but has a biological age of 32."
- **Top 3 Levers**: "AI-generated, personalized recommendations for maximum impact."
- **12-Month Timeline**: "Track progress over time with annotated events like 'Started acupuncture'."

**Demo Data Story:** Sarah joined SANA at score 50, now at 78 - a 56% improvement over 12 months.

### 3. AI Journal - SIRM (2 minutes)

**Navigate to:** Journal tab

**Key Points:**
- **4 AI Personas**: "Users can choose a therapist, philosopher, poet, or evidence-based coach."
- **Context-Aware**: "The AI connects to their wellness data - notice it mentions their anxiety score."
- **Compare All Responses**: Tap to show how each persona responds differently.

**Talking Point:** "This isn't a chatbot - it's therapeutic AI that understands their complete health picture."

### 4. Practitioner Profile & SANA Index (2 minutes)

**Navigate to:** Home > Tap practitioner card > View Profile

**Key Points:**
- **SANA Index Score**: "This is our secret sauce - an outcome-weighted quality metric."
- **Score Breakdown**:
  - "20% credentials - verified education and licenses"
  - "20% volume - treatment experience"
  - "**40% measured outcomes** - this is the key differentiator"
  - "10% data quality, 10% satisfaction"
- **Condition-Specific Outcomes**: "This practitioner has 78% improvement rate for anxiety across 180 clients."

**Talking Point:** "The SANA Index creates accountability. Practitioners can't just claim they're effective - we measure it."

### 5. Evidence Dashboard (1-2 minutes)

**Navigate to:** Profile > Evidence Dashboard

**Key Points:**
- **Practitioner Analytics**: "Practitioners see their outcome data, benchmark against peers."
- **Evidence Generation**: "Every session contributes to the CAM evidence base - 12,450+ research-grade data points."

**Talking Point:** "We're not just a booking platform - we're building the scientific evidence for integrative medicine."

### 6. Enterprise Integration (2 minutes)

**Navigate to:** Profile > Enterprise Dashboard

#### NHS Social Prescribing Tab:
- **ROI Calculator**: "We demonstrate NHS cost savings - £124,000 in this example."
- **Bi-directional Referrals**: "GPs can refer patients to verified practitioners and see outcomes."

#### Corporate Wellness Tab:
- **Business Impact**: "Reduced sick days, increased productivity, better retention."
- **Department Analytics**: "HR can see which departments benefit most."

**Talking Point:** "We have two B2B revenue streams: NHS social prescribing and corporate wellness programs."

### 7. Research Portal (1 minute)

**Navigate to:** Profile > Research Portal

**Key Points:**
- **Dataset Access**: "Institutions can query anonymized datasets for research."
- **Export Formats**: "FHIR, REDCap, CSV - all GDPR Article 89 compliant."

**Talking Point:** "We monetize data ethically - anonymized, consented, research-grade data for academic institutions."

### 8. Closing - The Vision (1 minute)

**Return to:** Home screen

**Closing Points:**
- "SANA creates a flywheel: better data leads to better outcomes leads to more practitioners leads to more data."
- "We're not replacing healthcare - we're making complementary medicine measurable and accountable."

---

## Likely Questions & Answers

### Technical Questions

**Q: How do you measure outcomes?**
A: We use validated Patient-Reported Outcome Measures (PROMs) like WHO-5, DASS-21, and condition-specific assessments. Clients complete brief check-ins that track improvement over time.

**Q: Is this real AI or rule-based?**
A: The prototype demonstrates the UX. Production would use fine-tuned LLMs with RAG for evidence retrieval, trained on therapeutic communication patterns.

**Q: How do you handle data privacy?**
A: GDPR compliant, with explicit consent for data use. Research data is anonymized and aggregated. We never sell identifiable health data.

### Business Questions

**Q: What's your revenue model?**
A: Four streams:
1. SaaS subscriptions for practitioners (monthly fee)
2. Transaction fees on bookings (10-15%)
3. Enterprise contracts (NHS, corporate wellness)
4. Research data licensing (anonymized datasets)

**Q: Who are your competitors?**
A: Mindbody, Fresha, and Jane App handle booking but don't measure outcomes. We're building the "outcomes layer" for CAM.

**Q: What's your go-to-market?**
A: Start with practitioners (supply), then consumers (demand), then enterprise. We're initially focused on UK market with NHS integration as a differentiator.

### Prototype Questions

**Q: Is this connected to real data?**
A: This is a demonstration prototype with simulated data. It shows the complete user experience and data architecture we're building toward.

**Q: How far along is development?**
A: The Flutter app and API structure are complete. Production deployment requires: payment integration, real practitioner onboarding, and ML model training on outcome data.

---

## Demo Data Highlights

Use these specific data points during your demo:

| Metric | Value | Context |
|--------|-------|---------|
| Client health score journey | 50 → 78 | 12-month improvement |
| Practitioner SANA Index | 87/100 | Top 8% of platform |
| Outcome improvement (anxiety) | 48% | Across 180 clients |
| NHS cost savings | £124,000 | Annual estimate |
| Research data points | 12,450+ | Contributed to evidence base |
| Corporate enrollment | 71% | Employee participation |

---

## Troubleshooting

**App crashes or freezes:**
- Restart the app
- Use backup screenshots if needed

**Charts not rendering:**
- Ensure device has sufficient memory
- Try portrait orientation

**Questions you can't answer:**
- "That's a great question - let me follow up with specifics after this meeting."

---

## Post-Demo Follow-up

After the demo, send:
1. This demo guide for reference
2. Links to algorithm documentation
3. Financial projections (if appropriate)
4. Next steps for due diligence

---

*SANA Health Platform - Demonstration Prototype*
*All data shown is simulated for demonstration purposes*
