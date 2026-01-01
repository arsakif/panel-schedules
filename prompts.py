"""
Prompts for Google Gemini AI to extract panel schedule data.
"""

PANEL_EXTRACTION_PROMPT = """
You are an expert in reading electrical engineering drawings. Analyze this image containing ONE electrical panel schedule/switchboard directory.

For the panel schedule in this image, extract:

**Panel Header Information:**
- Panel Name: Panel designation (e.g., "AP-1", "Panel A", "PC-LP-01-01")
- Panel Amperage of Lugs and Bus: The bus amperage rating (e.g., "400A", "225A")
- Panel Amperage of Main OCPD: Main circuit breaker or fuse rating if exists (e.g., "400A MCB", "200A MB"). If panel is MLO (Main Lugs Only), leave empty ""
- Panel Voltages: System voltage (e.g., "120/208V", "277/480V", "480Y/277")
- Panel Phases: Number of phases (e.g., "1Ph", "3Ph", "1", "3")
- Panel Wire: Wire configuration (e.g., "2W", "3W", "4W")
  * 2W = phase and neutral
  * 3W = either 3 phase only OR 2 phase + 1 neutral
  * 4W = 3 phase + 1 neutral
- Panel Pole(Circuit)#: Number of poles/circuits (e.g., "42", "60 poles"). For switchboards without pole designation, leave empty ""
- Panel Short Circuit Rating (KAIC): Short circuit rating (e.g., "22KAIC", "65,000", "100KAIC", "10,000AIC")
- Panel Enclosure Type: Enclosure type (e.g., "NEMA1", "NEMA3R", "Type 1", "NEMA4X")

**Circuits Information:**
For each circuit row in the panel:
- Circuit Number: Circuit number(s). Pay attention to #of poles - 1 pole=1 circuit#, 2 poles=2 circuit#s, 3 poles=3 circuit#s (e.g., "1", "2,4", "1,3,5")
- Load Description: What the circuit serves (e.g., "Lighting", "Receptacles", "HVAC Unit")
- OCP Size: Breaker/fuse rating (e.g., "20A", "30A", "100A")
- Poles: Number of poles (1, 2, or 3)
- Feeder: Cable size/type if specified (e.g., "3#10+1#10G in 3/4EMT", "#12/2"). If not given, leave empty ""

IMPORTANT READING ORDER: 
- If panel has TWO COLUMNS (left and right), read LEFT column from top to bottom FIRST
- Then read RIGHT column from top to bottom
- Keep circuits in the exact order they appear

Return TWO SEPARATE COMPACT JSON objects (no whitespace), one for panel header and one for circuits:

PANEL_HEADER:
{"panel_name":"PC-LP-01-01","bus_amperage":"400A","main_ocpd":"400A MCB","voltage":"208Y/120","phase":"3","wire":"4","poles":"42","kaic":"22,000","enclosure":"Type 1"}

CIRCUITS:
[{"circuit_number":"1,3,5","load_description":"Panel PC-LP-01-02","ocp_size":"250A","poles":"3","feeder":"3#4+1#8G in 1EMT"},{"circuit_number":"2","load_description":"Lighting","ocp_size":"20A","poles":"1","feeder":""}]

IMPORTANT: 
- Keep field order EXACTLY as listed above (panel_name, bus_amperage, main_ocpd, voltage, phase, wire, poles, kaic, enclosure)
- For circuits, keep order: circuit_number, load_description, ocp_size, poles, feeder
- Start with "PANEL_HEADER:" then the JSON
- On new line: "CIRCUITS:" then the JSON array
- If any field is not present: use ""
- If no circuits found: return empty array []

ONLY return the two labeled JSON structures, no other text.
"""
