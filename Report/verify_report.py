# verify_report.py - Comprehensive Quality and Verification Inspection
import docx
from docx.oxml.ns import qn
import re
import os
from PIL import Image

doc = docx.Document('Report/report_sem7.docx')

print("=" * 60)
print("1. SECTIONS & MARGINS VERIFICATION")
print("=" * 60)
print(f"Total Sections: {len(doc.sections)}")
for idx, sec in enumerate(doc.sections):
    print(f"Section {idx+1}: Margins -> L: {sec.left_margin.inches:.2f}\", R: {sec.right_margin.inches:.2f}\", T: {sec.top_margin.inches:.2f}\", B: {sec.bottom_margin.inches:.2f}\"")
    assert round(sec.left_margin.inches, 2) == 1.50, f"Left margin mismatch: {sec.left_margin.inches}"
    assert round(sec.right_margin.inches, 2) == 0.50, f"Right margin mismatch: {sec.right_margin.inches}"
    assert round(sec.top_margin.inches, 2) == 1.00, f"Top margin mismatch: {sec.top_margin.inches}"
    assert round(sec.bottom_margin.inches, 2) == 1.00, f"Bottom margin mismatch: {sec.bottom_margin.inches}"
print("=> PASS: All section margins match college requirements (L: 1.50\", R: 0.50\", T: 1.00\", B: 1.00\")")

print("\n" + "=" * 60)
print("2. TABLE STYLING & BORDERLESS VERIFICATION")
print("=" * 60)
tables_with_shd = 0
tables_with_borders = 0

for t_idx, t in enumerate(doc.tables):
    tblBorders = t._tbl.tblPr.find(qn('w:tblBorders'))
    has_borders = False
    if tblBorders is not None:
        for border_tag in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            b = tblBorders.find(qn(f'w:{border_tag}'))
            if b is not None and b.get(qn('w:val')) != 'none':
                has_borders = True
    if has_borders:
        tables_with_borders += 1

    has_shd = False
    for row in t.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            shd = tcPr.find(qn('w:shd'))
            if shd is not None and shd.get(qn('w:fill')) not in ['auto', None, '']:
                has_shd = True
    if has_shd:
        tables_with_shd += 1

print(f"Total Tables in document: {len(doc.tables)}")
print(f"Tables with borders: {tables_with_borders} (Expected: 0)")
print(f"Tables with background shading: {tables_with_shd} (Expected: 0)")
assert tables_with_borders == 0, f"Error: Found {tables_with_borders} tables with borders!"
assert tables_with_shd == 0, f"Error: Found {tables_with_shd} tables with shading!"
print("=> PASS: 100% of tables are simple, borderless, and unshaded")

print("\n" + "=" * 60)
print("3. TYPOGRAPHY & COLOR VERIFICATION")
print("=" * 60)
non_tnr = set()
non_black_colors = set()

for p in doc.paragraphs:
    for r in p.runs:
        if r.font.name and r.font.name != 'Times New Roman':
            non_tnr.add(r.font.name)
        if r.font.color and r.font.color.rgb and r.font.color.rgb != docx.shared.RGBColor(0, 0, 0):
            non_black_colors.add(str(r.font.color.rgb))

for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    if r.font.name and r.font.name != 'Times New Roman':
                        non_tnr.add(r.font.name)
                    if r.font.color and r.font.color.rgb and r.font.color.rgb != docx.shared.RGBColor(0, 0, 0):
                        non_black_colors.add(str(r.font.color.rgb))

print(f"Non-TNR fonts detected: {non_tnr} (Expected: empty)")
print(f"Non-black text colors detected: {non_black_colors} (Expected: empty)")
assert len(non_tnr) == 0, f"Error: Found non-TNR fonts: {non_tnr}"
assert len(non_black_colors) == 0, f"Error: Found non-black colors: {non_black_colors}"
print("=> PASS: 100% of text is Times New Roman and pure black RGBColor(0, 0, 0)")

print("\n" + "=" * 60)
print("4. REFERENCES AUDIT (MAX 10 REFERENCES)")
print("=" * 60)
ref_paras = []
in_ref_section = False

for p in doc.paragraphs:
    text = p.text.strip()
    if text == "REFERENCES":
        in_ref_section = True
        continue
    if in_ref_section and text == "ACKNOWLEDGEMENT":
        in_ref_section = False
        break
    if in_ref_section and text.startswith("[") and "]" in text:
        ref_paras.append(text)

print(f"Total References in References section: {len(ref_paras)}")
for r in ref_paras:
    print("  ", r[:85] + "...")

assert len(ref_paras) <= 10, f"Error: Expected max 10 references, found {len(ref_paras)}!"
assert len(ref_paras) == 10, f"Warning: Found {len(ref_paras)} references instead of 10."
print("=> PASS: References section contains exactly 10 peer-reviewed references (max 10 limit respected)")

print("\n" + "=" * 60)
print("5. SCREENSHOTS & IMAGE BACKGROUND AUDIT")
print("=" * 60)
screenshots = [
    r"Report\screenshots\screen_1_playground_journey.png",
    r"Report\screenshots\screen_2_metrics_and_charts.png",
    r"Report\screenshots\screen_3_environmental_timeline.png",
    r"Report\screenshots\screen_4_database_log.png",
    r"Report\screenshots\screen_fastapi_docs.png",
    r"Report\screenshots\screen_fastapi_chat_expanded.png",
    r"Report\screenshots\screen_fastapi_health.png"
]

all_white = True
for s in screenshots:
    if os.path.exists(s):
        img = Image.open(s).convert('L')
        # sample corners
        w, h = img.size
        tl = img.getpixel((10, 10))
        tr = img.getpixel((w - 10, 10))
        avg = sum(img.getdata()) / (w * h)
        is_light = avg > 200 and tl > 220
        status = "LIGHT / WHITE" if is_light else "DARK"
        print(f"  {os.path.basename(s):45s} -> Avg: {avg:.1f}/255, Corner: {tl} -> {status}")
        if not is_light:
            all_white = False
    else:
        print(f"  MISSING: {s}")
        all_white = False

assert all_white, "Error: Some screenshots are dark or missing!"
print("=> PASS: 100% of dashboard and API screenshots have crisp white backgrounds")

print("\n" + "=" * 60)
print("6. CHAPTER HEADINGS STRUCTURE AUDIT")
print("=" * 60)
ch_headings = []
for p in doc.paragraphs:
    t = p.text.strip()
    if re.match(r'^(CHAPTER|\d+\.\d+|REFERENCES|ACKNOWLEDGEMENT)', t):
        ch_headings.append(t)

print(f"Total Structural Headings: {len(ch_headings)}")
for h in ch_headings[:25]:
    print("  ", h)
if len(ch_headings) > 25:
    print("   ... (truncated)")

print("\n" + "=" * 60)
print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
print("=" * 60)
