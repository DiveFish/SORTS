import argparse
import csv


def get_verb_pos(word_order, subj_pos, obj_pos, words, props):
    has_aux = "aux" in props
    last_word_idx = len(words) - 1  # penultimate token = last word

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
        elif word_order in {
            "MF[SO]VC[V]",
            "MF[OS]VC[V]"
        }:
            return last_word_idx - 1
        else:
            raise ValueError(f"Unknown word order pattern with aux: {word_order}")

    # Non-aux cases
    if word_order == "VF[S]LK[V]MF[O]":
        return subj_pos + 1
    elif word_order == "VF[O]LK[V]MF[S]":
        return obj_pos + 1
    elif word_order in ("VF[ADV]LK[V]MF[SO]", "VF[ADV]LK[V]MF[OS]"):
        return 2
    elif word_order in ("LK[V]MF[SO]", "LK[V]MF[OS]"):
        return 1
    elif word_order in ("MF[SO]VC[V]", "MF[OS]VC[V]"):
        return last_word_idx
    else:
        raise ValueError(f"Unknown word order pattern: {word_order}")

    # If SVO and subj in  (Günter, Bertolt), subject pos + 2 --> außer bei psy, dort OVS


def tsv2conll(input_path, output_path, format="conll"):
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

            verb_pos = get_verb_pos(word_order, subj_pos, obj_pos, words, props)

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


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("testsuite_file", type=str)
    argparser.add_argument("conll_file", type=str)
    argparser.add_argument("--conll_type", "-t", default="x", choices=["x", "u"])
    args = argparser.parse_args()

    if args.conll_type == "u" and "_u" not in args.conll_file:
        raise ValueError("A conll-U file must have '_u' as its basename ending.")

    tsv2conll(args.testsuite_file, args.conll_file, args.conll_type)
