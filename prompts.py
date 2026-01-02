"""
Prompts for Google Gemini AI to extract panel schedule data.
"""

PANEL_EXTRACTION_PROMPT = """
You are an expert in reading electrical engineering drawings. Analyze this image containing ONE electrical panel schedule/switchboard directory.

For the panel schedule in this image, extract:

**Panel Header Information:**
1- Panel Name: Panel designation (e.g., "AP-1", "Panel A", "PC-LP-01-01")
2- Panel Amperage of Lugs and Bus: The bus amperage rating (e.g., "400A", "225A")
3- Panel Amperage of Main OCPD: Main circuit breaker or fuse rating if exists (e.g., "400A MCB", "200A MB"). If panel is MLO (Main Lugs Only), leave empty ""
4- Panel Voltages: System voltage (e.g., "120/208V", "277/480V", "480Y/277")
5- Panel Phases: Number of phases ALWAYS format as number+"ph" (e.g., "1ph", "2ph", "3ph")
6- Panel Wire: Wire configuration ALWAYS format as number+"w" (e.g., "2w", "3w", "4w")
  * 2w = phase and neutral
  * 3w = either 3 phase only OR 2 phase + 1 neutral
  * 4w = 3 phase + 1 neutral
7- Panel Pole(Circuit)#: Number of poles/circuits (e.g., "42", "60 poles"). For switchboards without pole designation, leave empty ""
8- Panel Short Circuit Rating (KAIC): Short circuit rating (e.g., "22KAIC", "65,000", "100KAIC", "10,000AIC")
9- Panel Enclosure Type: Enclosure type (e.g., "NEMA1", "NEMA3R", "Type 1", "NEMA4X")

**Circuits Information:**
For each circuit row in the panel:
1- Load Description: What the circuit serves (e.g., "Lighting", "Receptacles", "HVAC Unit")
2- OCP Size: Breaker/fuse rating (e.g., "20A", "30A", "100A")
3- Poles: Number of poles (1, 2, or 3)
4- Feeder: Cable size/type if specified (e.g., "3#10+1#10G in 3/4EMT", "#12/2"). If not given, leave empty ""
5- Circuit Number: Circuit number(s). Pay attention to #of poles - 1 pole=1 circuit#, 2 poles=2 circuit#s, 3 poles=3 circuit#s (e.g., "1", "2,4", "1,3,5")
IMPORTANT READING ORDER: 
- If panel has TWO COLUMNS (left and right), read LEFT column from top to bottom FIRST
- Then read RIGHT column from top to bottom
- Keep circuits in the exact order they appear
- If the load description is spare or space ignore that circuit and do not include it in the output
- If the load description is empty ignore that circuit and do not include it in the output

Return TWO SEPARATE COMPACT JSON objects (no whitespace), one for panel header and one for circuits:

please use the same order as the column order from left to right in the JSON structure.
PANEL_HEADER:
{{"panel_name":"", "bus_amperage":"", "main_ocpd":"", "voltage":"", "phase":"", "wire":"", "poles":"", "kaic":"", "enclosure":""}}


please use the same order as the column order from left to right in the JSON structure.
CIRCUITS:
[{"load_description":"", "ocp_size":"", "poles":"", "feeder":"", "circuit_number":""}, ...]

IMPORTANT: 
- Keep field order EXACTLY as listed above (panel_name, bus_amperage, main_ocpd, voltage, phase, wire, poles, kaic, enclosure)
- For circuits, keep order: load_description, ocp_size, poles, feeder, circuit_number
- Start with "PANEL_HEADER:" then the JSON
- On new line: "CIRCUITS:" then the JSON array
- If any field is not present: use ""
- If no circuits found: return empty array []

ONLY return the two labeled JSON structures, no other text.
"""
