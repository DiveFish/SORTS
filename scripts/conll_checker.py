import os


def extract_feature(features_str, key):
    for item in features_str.split("|"):
        if item.startswith(f"{key}:"):
            return item.split(":", 1)[1]
    return None


def format_values(values):
    return sorted(v if v is not None else "[MISSING]" for v in values)


def process_single_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        sentence_tokens = []
        orders = set()
        props = set()
        indices = []
        heads = []
        deprels = []
        head_errors = []
        sentence_index = 1
        cols_in_file = None

        for line in f:
            line = line.strip()

            # End of sentence
            if line == "":
                mismatches = []

                # Feature mismatches
                if len(orders) > 1:
                    mismatches.append(f"order: {format_values(orders)}")
                if len(props) > 1:
                    mismatches.append(f"props: {format_values(props)}")

                # ID checks
                if indices:
                    if None in indices:
                        mismatches.append("indices: [MALFORMED]")
                    elif len(indices) != len(set(indices)):
                        mismatches.append("duplicate IDs in sentence")
                    else:
                        expected = list(range(1, len(indices) + 1))
                        if sorted(indices) != expected:
                            mismatches.append(f"indices not consecutive: {sorted(indices)}")

                # HEAD checks if file has enough columns
                if cols_in_file and cols_in_file >= 7:
                    if indices and heads and None not in indices and None not in heads:
                        max_idx = max(indices)

                        # HEAD errors
                        for i, (idx, h) in enumerate(zip(indices, heads)):
                            if h == idx:
                                head_errors.append(f"HEAD=ID at token {idx}")
                            if h > max_idx:
                                head_errors.append(f"HEAD>{max_idx} at token {idx} (head={h})")
                            if h < 0:
                                head_errors.append(f"HEAD<0 at token {idx} (head={h})")
                            if h == max_idx:
                                mismatches.append(f"HEAD points to last token ID {max_idx} (from token {idx})")

                        if head_errors:
                            mismatches.extend(head_errors)

                    # Deprel multiplicity check
                    if deprels:
                        nsubj_count = deprels.count("nsubj")
                        obj_count = deprels.count("obj")
                        if nsubj_count > 1:
                            mismatches.append(f"multiple nsubj ({nsubj_count})")
                        if obj_count > 1:
                            mismatches.append(f"multiple obj ({obj_count})")

                    # Specific DEPREL → verb/root HEAD check
                    try:
                        token_info = list(zip(indices, heads, deprels))
                        verb_heads = {idx for idx, _, rel in token_info if rel in {"root", "verb"}}
                        target_deprels = {"nsubj", "obj", "obl", "mark", "advmod", "punct", "aux"}
                        for idx, head, rel in token_info:
                            if rel in target_deprels and head not in verb_heads:
                                mismatches.append(f"{rel} at token {idx} doesn't attach to verb/root (head={head})")
                    except Exception as e:
                        mismatches.append(f"[ERROR during deprel-head check: {e}]")

                # Print mismatches
                if mismatches:
                    print(f"[{os.path.basename(file_path)}] Sentence {sentence_index} – mismatches: {', '.join(mismatches)}")
                    print("  " + " ".join(sentence_tokens))
                    print()

                # Reset for next sentence
                sentence_index += 1
                sentence_tokens = []
                orders.clear()
                props.clear()
                indices = []
                heads = []
                deprels = []
                head_errors = []
                continue

            # Parse line
            cols = line.split("\t")

            # Detect column count once per file
            if cols_in_file is None and len(cols) >= 1:
                cols_in_file = len(cols)

            if len(cols) < 1:
                print(f"[ERROR] Malformed line in {os.path.basename(file_path)}, sentence {sentence_index}: {line}")
                continue

            token = cols[1] if len(cols) > 1 else "[MISSING]"
            feats = cols[5] if len(cols) > 5 else ""
            sentence_tokens.append(token)

            # ID
            try:
                idx = int(cols[0])
            except (ValueError, IndexError):
                print(f"[ERROR] Invalid ID in {os.path.basename(file_path)}, sentence {sentence_index}: '{cols[0] if len(cols) > 0 else ''}'")
                idx = None
            indices.append(idx)

            # HEAD
            head = None
            if cols_in_file >= 7 and len(cols) > 6:
                head_val = cols[6]
                if head_val == "_":
                    head = None
                else:
                    try:
                        head = int(head_val)
                    except ValueError:
                        print(f"[ERROR] Invalid HEAD in {os.path.basename(file_path)}, sentence {sentence_index}: '{head_val}'")
                        head = None
            heads.append(head)

            # DEPREL
            deprel = cols[7] if len(cols) > 7 else None
            deprels.append(deprel)

            # Extract features
            orders.add(extract_feature(feats, "order"))
            props.add(extract_feature(feats, "props"))


def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".conll"):
            full_path = os.path.join(directory_path, filename)
            process_single_file(full_path)


if __name__ == "__main__":
    directory = "/Users/patricia/Code/SORTS/dutch/gold/"
    process_directory(directory)
