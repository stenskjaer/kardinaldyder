# -*- coding: utf-8 -*-


# author: Author name
# corpus_dir: Directory containing correctly formatted corpora
# corpus_subdir: Optional subdir used in stead of author as corpus dir
# filename_addon: Ending of corpus filename
author = "aischylos"
corpus_dir = "../../kardinaldyderne/private-korpus/Corpora"
corpus_subdir = ""
filename_prefix = ""
filename_addon = "-corpus-stripped.txt"


# terms: Søgetermer, liste. Formatteret: [' ανδρει',' ηνορε',' αδροτ',' ανδρειοτ']
# exceptions: Søgetermer som skal udelukkes. Formatteres som søgetermer.
# bar_baseline: Koordinat for diagramlinjens grundlinje.
terms = " φρον, φρο\[ν"
exceptions = " φρονημ, φροντισα,  φροντιζ, φροντισ{ε"
bar_baseline = 0

# freq_factor: Frekvensfaktor anvendt i statistiske beregninger
# width_factor: Bredden på diagrammet
# diagram_bars: Antal diagramlinjer
# granularity: Hvor fint skal den skelne mellem linjernes placering?
freq_factor = 10000
width_factor = 10
diagram_bars = 7
granularity = 4

# Diagram settings
diagram_variables = {
    'test': 'hello world!',
    'heavyrulewidth'	: "line width=0.08em",
    'lightrulewidth'	: "line width=0.05em",
    'outer_limit_left'	: -1.5,
    'outer_limit_right'	: width_factor + 1.5,
    'outer_limit_top'	: (diagram_bars * 0.5) + 0.75,
    'outer_limit_bottom': -0.65,
    'inner_limit_left'	: 0,
    'inner_limit_right'	: width_factor,
    'inner_limit_top'	: diagram_bars * 0.5,
    'inner_limit_bottom': 0,
    'header_baseline'	: (diagram_bars * 0.5) + 0.35,
    'header_baseline_descender': (diagram_bars * 0.5) + 0.3,
    'bars'		: diagram_bars,
    }
