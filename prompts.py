"""
Prompts for Google Gemini AI to extract panel schedule data.
"""

PANEL_EXTRACTION_PROMPT = """
You are an expert in reading electrical engineering drawings. Analyze this image containing ONE electrical panel schedule/switchboard directory.

For the panel schedule in this image, extract:

**Panel Header (top of the table):**
- Panel Name/Designation (e.g., "AP-1", "Panel A", "PC-LP-01-01")
- Main Rating (e.g., "100A MLO", "200A MCB", "400A")
- Voltage (e.g., "120V/208V", "208Y/120", "277V/480V")
- Phase (e.g., "3Ph", "3", "1Ph")
- Wire (e.g., "4W", "3W", "4", "3")
- Number of Poles (e.g., "42 poles", "42")
- KAIC Rating (e.g., "22KAIC", "22,000 AMPS")
- Enclosure Type (e.g., "NEMA1", "NEMA3R", "Type 1")

**Circuits:**
For each circuit row in the panel:
- Load Description: What the circuit serves
- OCP Size: Breaker/fuse rating (e.g., "20A", "30A", "100A")
- Poles: Number of poles (1, 2, or 3)
- Feeder: Cable size/type if given (otherwise empty "")
- Circuit Number: Circuit number if given (otherwise empty "")

IMPORTANT ORDER: 
- If panel has TWO COLUMNS (left and right), read LEFT column from top to bottom FIRST
- Then read RIGHT column from top to bottom
- Keep circuits in the exact order they appear

Return COMPACT JSON (no whitespace):
{"panels":[{"panel_header":{"panel_name":"PC-LP-01-01","main_rating":"400A MCB","voltage":"208Y/120","phase":"3","wire":"4","poles":"","kaic":"22,000","enclosure":"Type 1"},"circuits":[{"load_description":"Panel PC-LP-01-02","ocp_size":"250A","poles":"3","feeder":"","circuit_number":"1"},{"load_description":"Lighting","ocp_size":"20A","poles":"1","feeder":"","circuit_number":"2"}]}]}

If any field is not present: use ""
If no panel found: return {"panels":[]}

ONLY return valid JSON, no other text.
"""
