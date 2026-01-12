# 🏗️ Cosmic Explorer: Architectural Blueprint (Developer Guide)

This document provides a technical overview of the "Scientific Masterclass" architecture for developers looking to maintain, scale, or deploy this platform within educational institutions.

## 1. The "Persona-Agentic" AI Architecture
The platform uses what we call a **Persona-Agentic** architecture.

*   **Is it Agentic?**: Yes, in the sense that the AI (The Maestro) maintains a specific "Scientific Worldview" and orchestrates the user's educational journey. It doesn't just answer questions; it monitors the current astronomical state and "decodes" it for the student.
*   **Decoupled Intelligence**: The AI logic is isolated in `utils/ai_engine.py`. It uses **Phase-Based Prompting**:
    *   **Phase I**: Conceptual Grounding.
    *   **Phase II**: Technical Taxonomy.
    *   **Phase III**: Contextual Decoding (The current sky).

## 2. The L3 Hybrid Stack
The application is organized into three distinct layers:

### Layer 1: The Computation Engine (Python/Flask)
*   **Source of Truth**: NASA JPL Ephemeris data processed via specialized physics libraries.
*   **Logic**: Handled in `utils/panchanga.py` and `utils/skyshot.py`.
*   **Security**: Oracle Linux 9 / OCI Hardened. SELinux-compliant and strictly stateless (no database).

### Layer 2: The Visualization Layer (Three.js)
*   **Dynamics**: Individual 3D modules (Zodiac Aligner, Samvatsara Resonance) are built as standalone HTML/JS templates using Three.js.
*   **Integration**: These are injected into the `insights.html` report using a **Metadata-Driven Framing System**. This ensures each 3D simulation gets exactly the canvas height and coordinate system it requires.

### Layer 3: The Interaction Layer (Vanilla JS)
*   **Reactive Terms**: Any technical term in the report is "Reactive." Clicking it triggers `triggerVisualHighlight()`, which creates a symbiotic link between the AI-generated text and the 3D simulators.

## 3. Organizational Roadmap for Schools
To make this available to large-scale educational institutions, follow this roadmap:

### Step 1: LTI / SSO Integration
Current version uses a simple "Converter" entry point. For schools:
- Replace the converter with an **LTI (Learning Tools Interoperability)** bridge to connect with Canvas/Blackboard.
- Implement **OIDC/SSO** for student identity tracking.

### Step 2: Content Multitenancy
- Upgrade the `app.py` wrapper to support teacher-created "Classrooms."
- Allow teachers to set "Simulation Constraints" (e.g., locking the app to only show the "Great Drift" simulator for a specific lesson).

### Step 3: API Decoupling
- Currently, Gemini iscalled synchronously. For high-volume student traffic, implement a **Task Queue (Celery/Redis)** to handle AI requests asynchronously, preventing UI blocking during peak usage.

## 4. Tech Stack Summary
- **Backend**: Python 3.9 (Flask).
- **Frontend**: HTML5, Vanilla CSS3 (Custom Tokens), JavaScript (ES6+).
- **Graphics**: Three.js (WebGL).
- **AI**: Google Gemini 2.0 Flash (via `google-generativeai` SDK).
- **Deployment**: Nginx (Reverse Proxy) + Gunicorn + Oracle Linux 9.

---
*Created for the V6.0.1 Scientific Masterclass Release.*
