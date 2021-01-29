import csv
import sys


def conll_to_tsv(conll_file: str, tsv_file: str):
    """
    This function converts conll files into the corresponding TSV representation.
    See examples for this in the dutch and German gold folders.
    """
    ID = 0
    TOKEN = 1
    PROPS = 5
    SYN_ROLE = 7

    with open(conll_file) as conll, open(tsv_file, "w") as tsv:
        tsv_writer = csv.writer(tsv, delimiter="\t")
        header = ["Word Order", "Other Properties", "Subject Position", "Object Position", "Sentence"]
        tsv_writer.writerow(header)

        sent_out = []
        subj_pos = None
        obj_pos = None
        sentence = ""

        for line in conll.readlines():
            line = line.strip()
            # If an empty line is found, the old sentence is written to the file 
            # and the sentence data is reset.
            if not line:
                sent_out.extend([subj_pos, obj_pos, sentence.rstrip()])
                tsv_writer.writerow(sent_out)
                sent_out = []
                sentence = ""
                subj_pos = None
                obj_pos = None

            else:
                # Add properties to new TSV file.
                line = line.split("\t")
                if not sentence:
                    props = line[PROPS].split("|")
                    word_order = props[0].split(":")[1]
                    other_props = props[1].split(":")[1]
                    sent_out.extend([word_order, other_props])

                # Determine Subject and Object Position
                if line[SYN_ROLE] == "nsubj":
                    subj_pos = line[ID]
                if line[SYN_ROLE] == "obj":
                    obj_pos = line[ID]

                # Extend sentence by next token.
                sentence += line[TOKEN] + " "


if __name__ == "__main__":
    conll_to_tsv(sys.argv[1], sys.argv[2])
