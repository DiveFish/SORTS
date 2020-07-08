# SORTS
A Subject-Object Resolution Test Suite of German minimal sentence pairs for morpho-syntactic and semantic model introspection.

The SORTS test suite consists of 18,502 monotransitive clauses, annotated with the following property classes:

|Property | Annotation |
|:------------- |:-------------|
|Base case|`acc`|
|**_1. Word order_**|
|VSO|`LK[V]MF[SO]`|
|VSO (question)|`LK[V]MF[SO]Q`|
|SVO|`VF[S]LK[V]MF[O]`|
|SOV|`MF[SO]VC[V]`|
|VOS|`LK[V]MF[OS]`|
|VOS (question)|`LK[V]MF[OS]Q`|
|OVS|`VF[O]LK[V]MF[S]`|
|OSV|`MF[OS]VC[V]`|
|**_2. Morpho-syntax_**|
|Dative object|`dat`|
|Subject-object case syncretism|`amb`|
|Pronoun subject|`spron`|
|Pronoun object|`opron`|
|Negated object|`oneg`|
|Auxiliary verb|`aux`|
|Prepositional phrase|`pp`|
|**_3. Semantics_**|
|Inanimate subject|`sinan`|
|Animate object|`oan`|
|Inverted animacy|`invan`|
|Ambiguous institutional subject|`sinst`|
|Proper name subject|`sname`|
|Subject-object directedness|`sodir`|
|Void object|`oempt`|
|Psych verb with experiencer object|`psy`|
|Light verb construction|`vlight`|
|Synonymous verb|`syn`|
|Idiom|`idm`|

## Sentence variations
Sentences with particular properties can be extracted from the test suite using the full word order and property annotations as in this example:

|Variations | Property | Full annotation |
|:------------- |:-------------|:-------------|
|0| Base sentence, e.g. SVO order |`order:VF[S]LK[V]MF[O]\|props:base-acc`|
|1| Base sentence, e.g. SVO order with auxiliary verb|`order:VF[S]LK[V]MF[O]\|props:base-aux`|
|2| Base sentence, e.g. SVO order with auxiliary verb and synonym of main verb |`order:VF[S]LK[V]MF[O]\|props:aux-syn`|

### Additional annotations
[Gold standard](https://github.com/DiveFish/SORTS/tree/master/gold)
- Subject head index and label
- Object head index and label

[Annotated](https://github.com/DiveFish/SORTS/tree/master/annotated) (automatically annotated using [sticker2](https://github.com/stickeritis/sticker2))
- Lemmas, part of speech and topological fields (manually corrected)
- Morphological information

### Test suite subsets
- `german_part-ambiguous_gold.conll`: only the `amb` variant displays case syncretism between subject and object
- `german_ambiguous_gold.conll`: all sentences display case syncretism between subject and object; no `dat` and `amb` variants

### In progress
- The Dutch translation of this test suite - will be interesting since Dutch only allows subject-object disambiguation via subject-verb agreement, no case marking!
- A PP attachment test suite - more brain teasers for NLP systems...
