def read_conll_file(filename):
    """Read a CoNLL-X file and return a list of sentences (each a list of lines)."""
    sentences = []
    current = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line:
                current.append(line)
            else:
                if current:
                    sentences.append(current)
                    current = []
        if current:
            sentences.append(current)
    return sentences


def extract_order_and_props(feats):
    """Extract 'order' and 'props' from FEATS column."""
    order = None
    props = None
    for feat in feats.split('|'):
        if feat.startswith('order:'):
            order = feat[len('order:'):]
        elif feat.startswith('props:'):
            props = feat[len('props:'):]
    return order, props


def build_sentence_key(sentence):
    """Return a tuple key: (order, props, set of surface forms)"""
    forms = set()
    order = None
    props = None

    for line in sentence:
        if line.startswith('#'):
            continue  # skip comments if any
        cols = line.split('\t')
        if len(cols) < 6:
            continue  # malformed line
        form = cols[1]
        feats = cols[5]

        # Extract once (all tokens should have same order/props)
        if order is None or props is None:
            order_tmp, props_tmp = extract_order_and_props(feats)
            if order_tmp is not None:
                order = order_tmp
            if props_tmp is not None:
                props = props_tmp

        forms.add(form)

    return (order, props, frozenset(forms))


def replace_sentences(original_file, fixes_file, output_file):
    original_sentences = read_conll_file(original_file)
    fix_sentences = read_conll_file(fixes_file)

    # Build fix map
    fix_map = {build_sentence_key(s): s for s in fix_sentences}

    output_sentences = []
    for orig in original_sentences:
        key = build_sentence_key(orig)
        if key in fix_map:
            output_sentences.append(fix_map[key])
        else:
            output_sentences.append(orig)

    # Write merged output
    with open(output_file, 'w', encoding='utf-8') as f:
        for sentence in output_sentences:
            for line in sentence:
                f.write(line + '\n')
            f.write('\n')


# Takes an original conll file and replaces all sentences by those contained in a fixed conll file. All sentences not
# contained in the fixer file are preserved.
if __name__ == '__main__':
    original_file = "/german/gold/german_part-amb_gold_all-heads.conll"
    original_file2 = "/Users/patricia/Code/SORTS/german/gold/german_part-amb_gold.conll"
    fix_file = "/Users/patricia/Code/SORTS/german/pp/pp_part-amb_all-heads.conll"
    fix_file2 = "/Users/patricia/Code/SORTS/german/pp/pp_part-amb.conll"
    orig_fixed_file = "/Users/patricia/Code/SORTS/german/gold/german_part-amb_gold_all-heads_fixed-pp.conll"
    orig_fixed_file2 = "/Users/patricia/Code/SORTS/german/gold/german_part-amb_gold_fixed-pp.conll"
    replace_sentences(original_file, fix_file, orig_fixed_file)
