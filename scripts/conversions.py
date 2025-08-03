import csv
import sys


def conll2tsv(conll_file: str, tsv_file: str):
    """
    This function converts conll files into the corresponding tsv representation.
    See examples for this in the Dutch and German gold folders.
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


def get_verb_pos(word_order, subj_pos, obj_pos, words, props, language="de"):
    has_aux = "aux" in props
    is_psy = "psy" in props
    longer_args = {"Staf", "Han", "Essent", "NPO", "Bertolt", "Günter"}
    dutch_kopjes = {"kopje", "kopjes"}

    last_idx = len(words)
    last_word_idx = last_idx - 1
    penultimate_word_idx = last_word_idx - 1

    if has_aux:
        if word_order in {
            "VF[S]LK[V]MF[O]",
            "VF[O]LK[V]MF[S]",
            "VF[ADV]LK[V]MF[SO]",
            "VF[ADV]LK[V]MF[OS]",
            "LK[V]MF[SO]",
            "LK[V]MF[OS]"
        }:
            return last_word_idx
        elif word_order in {"MF[SO]VC[V]", "MF[OS]VC[V]"}:
            if language == "nl":
                return last_word_idx
            else:
                return penultimate_word_idx
        else:
            raise ValueError(f"Unknown word order pattern with aux: {word_order}")

    # TODO: For psy OVS orders (not aux), the koffie exception also holds

    # --- Regular (non-aux or Dutch) logic ---
    if word_order == "VF[S]LK[V]MF[O]":
        subject_word = words[subj_pos - 1] if subj_pos - 1 < len(words) else ""
        if subject_word in longer_args:
            return subj_pos + 2
        return subj_pos + 1

    elif word_order == "VF[O]LK[V]MF[S]":
        obj_word = words[obj_pos - 1] if obj_pos - 1 < len(words) else ""

        # Dutch exception: kopje/kopjes
        if language == "nl" and obj_word.lower() in dutch_kopjes:
            return obj_pos + 2

        if is_psy and obj_word in longer_args:
            return obj_pos + 2
        return obj_pos + 1

    elif word_order in ("VF[ADV]LK[V]MF[SO]", "VF[ADV]LK[V]MF[OS]"):
        return 2
    elif word_order in ("LK[V]MF[SO]", "LK[V]MF[OS]"):
        return 1
    elif word_order in ("MF[SO]VC[V]", "MF[OS]VC[V]"):
        return last_word_idx
    else:
        raise ValueError(f"Unknown word order pattern: {word_order}")


def tsv2conll(input_path, output_path, format="conll", language="de"):
    """
    This function converts tsv files into the corresponding conll representation.
    See examples for this in the Dutch and German gold folders.

    """
    if format not in {"conll", "conllu"}:
        raise ValueError("format must be either 'conll' or 'conllu'")

    with open(input_path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
        reader = csv.DictReader(f_in, delimiter='\t')

        for row in reader:
            word_order = row['Word Order']
            props = row['Other Properties']
            subj_pos = int(row['Subject Position'])
            obj_pos = int(row['Object Position'])
            words = row['Sentence'].strip().split()

            sep = "=" if format == "conllu" else ":"
            metadata = f"order{sep}{word_order}|props{sep}{props}"

            verb_pos = get_verb_pos(word_order, subj_pos, obj_pos, words, props, language)

            for idx, word in enumerate(words):
                token_id = idx + 1
                head = "_"
                dep = "_"

                if token_id == verb_pos:
                    head = "0"
                    dep = "verb"
                elif token_id == subj_pos:
                    head = str(verb_pos)
                    dep = "nsubj"
                elif token_id == obj_pos:
                    head = str(verb_pos)
                    dep = "obj"

                f_out.write(f"{token_id}\t{word}\t_\t_\t_\t{metadata}\t{head}\t{dep}\t_\t_\n")
            f_out.write("\n")


def conll2conllu(input_path: str, output_path: str):
    with open(input_path, encoding="utf-8") as f_in, open(output_path, "w", encoding="utf-8") as f_out:
        for line in f_in:
            if line.strip() == "":
                f_out.write("\n")
                continue

            columns = line.rstrip("\n").split("\t")
            if len(columns) >= 6:
                columns[5] = columns[5].replace(":", "=")
            f_out.write("\t".join(columns) + "\n")


if __name__ == "__main__":
    conll2tsv(sys.argv[1], sys.argv[2])
