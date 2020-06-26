# SORTS
A Subject-Object Resolution Test Suite of German minimal sentence pairs for morpho-syntactic and semantic model introspection

The SORTS test suite consists of 18,502 monotransitive clauses, annotated with 24 property classes. The test suite is available both in a raw gold standard and an annotated format for testing. The gold standard includes token forms along with subject and object head indices and head labels. The annotated format has been automatically annotated with the [sticker2](https://github.com/stickeritis/sticker2) software for lemmas, part of speech and topological fields and has been manually corrected.

## Property classes

|Property | Annotation |
| ------------- |:-------------|
|**_Word order_**|
|LK[V]MF[SO]|`LK[V]MF[SO]`|
|LK[V]MF[SO]Q|`LK[V]MF[SO]Q`|
|VF[S]LK[V]MF[O]|`VF[S]LK[V]MF[O]`|
|MF[SO]VC[V]|`MF[SO]VC[V]`|
|LK[V]MF[OS]|`LK[V]MF[OS]`|
|LK[V]MF[OS]Q|`LK[V]MF[OS]Q`|
|VF[O]LK[V]MF[S]|`VF[O]LK[V]MF[S]`|
|MF[OS]VC[V]|`MF[OS]VC[V]`|
|**_Morpho-syntax_**|
|Base case|`acc`|
|Dative object|`dat`|
|Case syncretism|`amb`|
|Pronoun subject|`spron`|
|Pronoun object|`opron`|
|Negated object|`oneg`|
|Auxiliary verb|`aux`|
|PP|`pp`|
|**_Semantics_**|
|Inanimate subject|`sinan`|
|Animate object|`oan`|
|Inverted animacy|`invan`|
|Ambiguous subject|`sinst`|
|Proper name subject|`sname`|
|SO directedness|`sodir`|
|Void object|`oempt`|
|Psych verb|`psy`|
|Light verb|`vlight`|
|Synonymous verb|`syn`|
|Idiom|`idm`|
