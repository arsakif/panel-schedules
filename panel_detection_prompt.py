"""
Additional prompts for panel detection and bounding box extraction.
"""

PANEL_DETECTION_PROMPT = """
You are an expert in reading electrical engineering drawings. Analyze this image and find ALL electrical panel schedules/switchboard directories.

CRITICAL INSTRUCTIONS FOR BOUNDARIES:
Panel schedules have circuit numbers in columns on the FAR LEFT and FAR RIGHT sides - these are often OUTSIDE the main table border. YOU MUST INCLUDE THESE!

When defining the bounding box:
- x1 (left edge): Start BEFORE the leftmost circuit number column (not at the table border)
- x2 (right edge): End AFTER the rightmost circuit number column (not at the table border)
- y1 (top edge): Include the complete panel header
- y2 (bottom edge): Include the last circuit row completely

WHAT CIRCUIT NUMBERS LOOK LIKE:
- Usually single or double digit numbers (1, 2, 3... or 1-3, 2-4, etc.)
- Located in thin columns on far left and far right
- May be outside the thick table border
- Critical data that MUST be captured

IDENTIFICATION RULES:
- Panel schedules have solid rectangular borders
- Ignore revision clouds (cloud-shaped markings)
- Look for headers with panel names like "PC-LP-01-01", "PC-HP-02-01"
- Each panel is a separate table

For each panel, return:
1. Panel Name from header
2. Bounding box as percentages (0-100%)

EXAMPLE: If you see circuit numbers "1, 2, 3" on far left and "2, 4, 6" on far right of a panel, your bounding box MUST extend to include those number columns, not just the main table.

Return COMPACT JSON:
{"panels":[{"panel_name":"PC-LP-01-01","bbox":{"x1":4.5,"y1":10.0,"x2":49.5,"y2":85.0}},{"panel_name":"PC-LP-01-02","bbox":{"x1":50.5,"y1":10.0,"x2":95.5,"y2":85.0}}]}

If no panels: {"panels":[]}

ONLY return valid JSON.
"""
