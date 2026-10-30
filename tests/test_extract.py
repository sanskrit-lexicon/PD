import fitz

doc = fitz.open('GA.pdf')
fonts = set()
for page in doc:
    for f in page.get_fonts():
        fonts.add(f[3]) # Font name
print(f"Fonts used: {fonts}")
