data = [
    ("Ala ma kota.", [("Attribute", "Ala"), ("Deontic", "kota")]),
    ("Kot ma Alę.", [("Deontic", "Kot"), ("Attribute", "Alę")]),
]

with open("test_mae.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    f.write("<ADICO_test_1>\n")

    f.write("<TEXT><![CDATA[")
    for x, _ in data:
        f.write(x + "\n")
    f.write("]]></TEXT>\n")

    f.write("<TAGS>\n")
    offset = 0
    id = 0
    for sentence, sentence_tags in data:
        for tag, text in sentence_tags:
            start = sentence.find(text)
            real_start = offset + start
            real_stop = real_start + len(text)
            spans = f"{real_start}~{real_stop}"
            f.write(f'<{tag} id="x{id}" spans="{spans}" text="{text}" />\n')
            id += 1
        offset += len(sentence) + 1
    f.write("</TAGS>\n")

    f.write("</ADICO_test_1>")

with open("test_mae.xml", "r") as f:
    print(f.read())
