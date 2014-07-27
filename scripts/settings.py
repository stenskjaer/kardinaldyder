# -*- coding: utf-8 -*-


# author: Author name
# corpus_dir: Directory containing correctly formatted corpora
# corpus_subdir: Optional subdir used instead of author as corpus dir
# filename_addon: Ending of corpus filename
# output_folder: The folder where the finished .tex-file can be put.
# output_name: Filename of output .tex (excluding ending).
# output_addon: If specified, adds the addon between name and ending.
author = "antifon-orat"
corpus_dir = "../../kardinaldyderne/private-korpus/Corpora"
corpus_subdir = ""
filename_prefix = ""
filename_addon = "-corpus-stripped.txt"
output_folder = "../../kardinaldyderne/source/figures/dispersions"
output_name = author
output_addon = ""


# terms: Søgetermer, liste. Formatteret: [' ανδρει',' ηνορε',' αδροτ',' ανδρειοτ']
# exceptions: Søgetermer som skal udelukkes. Formatteres som søgetermer.
# bar_baseline: Koordinat for diagramlinjens grundlinje.
terms = [
    ['ἀνδρει-',
     '[τκ]?ανδρει, [ηα]νορε, αν?δρ(ει)?οτ',
     'ανδρεικ'],
    ['δικαι-',
     'δικαι',
     'δικαιο[γπ], δικαις'],
    ['σοφ-',
     'σοφ',
     'σοφι[σζ], σοφοκ, σοφαιν'],
    ['σωφρ-',
     'ε?σωφρ, \[σωφρ',
     'σωφρονι[σζκ]'],
    ['φρον-',
     '[πε]?φρον',
     'ε?φροντι[ζσ], φρονημ, ε?φροντισ[αε]'],
    ['ὁσι-',
     'οσι',
     ''],
    ['εὐσεβ-',
     'ευσεβ',
     ''],
]


# freq_factor: Frekvensfaktor anvendt i statistiske beregninger
# width_factor: Bredden på diagrammet
# diagram_bars: Antal diagramlinjer
# granularity: Hvor fint skal den skelne mellem linjernes placering?
freq_factor = 10000
width_factor = 8
granularity = 4
bar_baseline = 0

# Diagram settings
diagram_variables = {
    'heavyrulewidth'	: "line width=0.08em",
    'lightrulewidth'	: "line width=0.05em",
    'outer_limit_left'	: -1.5,
    'outer_limit_right'	: width_factor + (width_factor * 0.15),
    'outer_limit_bottom': -0.55,
    'inner_limit_left'	: 0,
    'inner_limit_right'	: width_factor,
    'inner_limit_bottom': 0,
    'author'		: author
    }







