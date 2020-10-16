extern crate tools;
extern crate clap;

use tools::*;

use clap::{App, Arg};
use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
    let matches = App::new("tools")
        .version("1.0")
        .author("DiveFish")
        .about("Tools to generate and work with the SORTS test suite.")
        .arg(
            Arg::with_name("INPUT")
                .help("Sets the input file to use")
                .required(true)
                .index(1),
        )
        .arg(
            Arg::with_name("OUTPUT")
                .help("Sets the output file to use")
                .required(true)
                .index(2),
        )
        .get_matches();

    let input_file = matches.value_of("INPUT").unwrap();
    let output_file = matches.value_of("OUTPUT").unwrap();

    let (triples, properties) = extract_sent_parts(&input_file);
    let (templates, templates_aux, templates_pp, templates_aux_pp) = generate_templates_german();
    generate_sents_from_templates(
        &triples,
        &properties,
        &templates,
        &templates_aux,
        &templates_pp,
        &templates_aux_pp,
        "Deshalb",
        "Weil",
        output_file,
    ).unwrap_or_else(|err| println!("{:?}", err));
}

/// Extract sentence constituents from file.
///
/// `properties` includes the property combination,
/// e.g. ambiguous sentences with a PP carry the property amb-pp.
///
/// Possible input word orders: <S V O> or <S VAUX O V> or <S V O PP> or <S VAUX O PP>
/// Standardized output word order: <S V O (VAUX)(PP)>
fn extract_sent_parts(file: &str) -> (Vec<Vec<String>>, Vec<String>) {
    let mut sent_parts = Vec::new();
    let mut properties = Vec::new();

    let f = File::open(&file).expect("Could not open file.");
    for l in BufReader::new(f).lines() {
        let mut l = l.unwrap();
        l = l.trim().to_string();
        let line = l.split("\t").collect::<Vec<_>>();

        if line.len() == 7 {    // Sentence includes AUX and PP
            sent_parts.push(vec![line[0].to_owned(), line[2].to_owned(), line[5].to_owned(), line[4].to_owned(), line[3].to_owned(), line[6].to_owned()]);
            properties.push(line[1].to_owned());
        } else if line.len() == 6 {
            if line[5].split(" ").collect::<Vec<_>>().len() > 1 { // Sentence includes PP
                sent_parts.push(vec![line[0].to_owned(), line[2].to_owned(), line[3].to_owned(), line[4].to_owned(), line[5].to_owned()]);
                properties.push(line[1].to_owned());
            } else {    // Sentence includes AUX
                sent_parts.push(vec![line[0].to_owned(), line[2].to_owned(), line[5].to_owned(), line[4].to_owned(), line[3].to_owned()]);
                properties.push(line[1].to_owned());
            }
        } else if line.len() == 5 {
            sent_parts.push(vec![line[0].to_owned(), line[2].to_owned(), line[3].to_owned(), line[4].to_owned()]);
            properties.push(line[1].to_owned());
        } else {
            eprintln!("Sentence length {} not supported.", line.len());
            eprintln!("{:?}", line);
        }
    }
    (sent_parts, properties)
}

/// German word order templates.
fn generate_templates_german() -> (Vec<Vec<String>>, Vec<Vec<String>>, Vec<Vec<String>>, Vec<Vec<String>>) {
    let s = "S".to_owned();
    let v = "V".to_owned();
    let o = "O".to_owned();
    let v_aux = "VAUX".to_owned();
    let pp = "PP".to_owned();

    let mut templates = Vec::new();
    templates.push(vec![s.clone(), v.clone(), o.clone()]);
    templates.push(vec![o.clone(), v.clone(), s.clone()]);
    templates.push(vec!["Deshalb".to_owned(), v.clone(), s.clone(), o.clone()]);
    templates.push(vec!["Deshalb".to_owned(), v.clone(), o.clone(), s.clone()]);
    templates.push(vec![v.clone(), s.clone(), o.clone(), "?".to_owned()]);
    templates.push(vec![v.clone(), o.clone(), s.clone(), "?".to_owned()]);
    templates.push(vec!["Weil".to_owned(), s.clone(), o.clone(), v.clone()]);
    templates.push(vec!["Weil".to_owned(), o.clone(), s.clone(), v.clone()]);

    let mut templates_aux = Vec::new();
    templates_aux.push(vec![s.clone(), v_aux.clone(), o.clone(), v.clone()]);
    templates_aux.push(vec![o.clone(), v_aux.clone(), s.clone(), v.clone()]);
    templates_aux.push(vec!["Deshalb".to_owned(), v_aux.clone(), s.clone(), o.clone(), v.clone()]);
    templates_aux.push(vec!["Deshalb".to_owned(), v_aux.clone(), o.clone(), s.clone(), v.clone()]);
    templates_aux.push(vec![v_aux.clone(), s.clone(), o.clone(), v.clone(), "?".to_owned()]);
    templates_aux.push(vec![v_aux.clone(), o.clone(), s.clone(), v.clone(), "?".to_owned()]);
    templates_aux.push(vec!["Weil".to_owned(), s.clone(), o.clone(), v.clone(), v_aux.clone()]);
    templates_aux.push(vec!["Weil".to_owned(), o.clone(), s.clone(), v.clone(), v_aux.clone()]);

    let mut templates_pp = Vec::new();
    templates_pp.push(vec![s.clone(), v.clone(), pp.clone(), o.clone()]);
    templates_pp.push(vec![o.clone(), v.clone(), pp.clone(), s.clone()]);
    templates_pp.push(vec!["Deshalb".to_owned(), v.clone(), pp.clone(), s.clone(), o.clone()]);
    templates_pp.push(vec!["Deshalb".to_owned(), v.clone(), pp.clone(), o.clone(), s.clone()]);
    templates_pp.push(vec![v.clone(), pp.clone(), s.clone(), o.clone(), "?".to_owned()]);
    templates_pp.push(vec![v.clone(), pp.clone(), o.clone(), s.clone(), "?".to_owned()]);
    templates_pp.push(vec!["Weil".to_owned(), pp.clone(), s.clone(), o.clone(), v.clone()]);
    templates_pp.push(vec!["Weil".to_owned(), pp.clone(), o.clone(), s.clone(), v.clone()]);

    let mut templates_aux_pp = Vec::new();
    templates_aux_pp.push(vec![s.clone(), v_aux.clone(), pp.clone(), o.clone(), v.clone()]);
    templates_aux_pp.push(vec![o.clone(), v_aux.clone(), pp.clone(), s.clone(), v.clone()]);
    templates_aux_pp.push(vec!["Deshalb".to_owned(), v_aux.clone(), pp.clone(), s.clone(), o.clone(), v.clone()]);
    templates_aux_pp.push(vec!["Deshalb".to_owned(), v_aux.clone(), pp.clone(), o.clone(), s.clone(), v.clone()]);
    templates_aux_pp.push(vec![v_aux.clone(), pp.clone(), s.clone(), o.clone(), v.clone(), "?".to_owned()]);
    templates_aux_pp.push(vec![v_aux.clone(), pp.clone(), o.clone(), s.clone(), v.clone(), "?".to_owned()]);
    templates_aux_pp.push(vec!["Weil".to_owned(), pp.clone(), s.clone(), o.clone(), v.clone(), v_aux.clone()]);
    templates_aux_pp.push(vec!["Weil".to_owned(), pp.clone(), o.clone(), s.clone(), v.clone(), v_aux.clone()]);

    (templates, templates_aux, templates_pp, templates_aux_pp)
}