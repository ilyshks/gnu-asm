
with open("test.txt", "r", encoding="utf-8") as infile, open("test.bin", "wb") as outfile:
    text = infile.read()
    text = text.replace('\n', '\r\n')
    outfile.write(text.encode("utf-8"))
