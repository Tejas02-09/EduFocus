import PyPDF2

pdf = PyPDF2.PdfReader(r'c:\Users\TEJAS\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\LocalState\sessions\FD8FCF8D0A88CE9B575D94CB33796A5A8E364714\transfers\2026-11\sca24mca040swathij (9-76) (2).pdf')

print("=== COMPLETE TEMPLATE STRUCTURE ===\n")
print(f"Total Pages: {len(pdf.pages)}\n")

chapters = {}
current_chapter = None

for i in range(len(pdf.pages)):
    text = pdf.pages[i].extract_text()
    lines = [l.strip() for l in text.split('\n')]
    
    for line in lines:
        if 'CHAPTER' in line:
            print(f"\n[Page {i+1}] {line}")
            current_chapter = line
            chapters[line] = []
        elif line and line[0].isdigit() and '.' in line and len(line) < 100:
            # Section headers
            if 'CHAPTER' not in line:
                print(f"  [Page {i+1}] {line}")
                if current_chapter:
                    chapters[current_chapter].append(line)
