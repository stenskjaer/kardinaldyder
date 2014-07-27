<?php 

$author = "andokides";
$corpus_dir = "../../kardinaldyderne/private-korpus/Corpora";
$corpus_subdir = "";

// Set dir
if ($corpus_subdir) {
    $dir = $corpus_dir.DIRECTORY_SEPARATOR.$corpus_subdir;
} else {
    $dir = $corpus_dir.DIRECTORY_SEPARATOR.$author;
}

$corpus_file = $dir .DIRECTORY_SEPARATOR. $author . "-corpus.txt";


if (file_exists($corpus_file)) {
    $content = file_get_contents($corpus_file);

    $search =  explode(",","ά,ὰ,ᾶ,ἀ,ἄ,ἂ,ἆ,ἁ,ἅ,ἃ,ἇ,ᾱ,ᾰ,έ,ὲ,ἐ,ἔ,ἒ,ἑ,ἕ,ἓ,ή,ὴ,ῆ,ἠ,ἤ,ἢ,ἦ,ἡ,ἥ,ἣ,ἧ,ί,ὶ,ῖ,ἰ,ἴ,ἲ,ἶ,ἱ,ἵ,ἳ,ἷ,ϊ,ΐ,ῒ,ῗ,ό,ὸ,ὀ,ὄ,ὂ,ὁ,ὅ,ὃ,ύ,ὺ,ῦ,ὐ,ὔ,ὒ,ὖ,ὑ,ὕ,ὓ,ὗ,ϋ,ΰ,ῢ,ῧ,ώ,ὼ,ῶ,ὠ,ὤ,ὢ,ὦ,ὡ,ὥ,ὣ,ὧ,ᾳ,ᾴ,ᾲ,ᾷ,ᾀ,ᾄ,ᾂ,ᾆ,ᾁ,ᾅ,ᾃ,ᾇ,ῃ,ῄ,ῂ,ῇ,ᾐ,ᾔ,ᾒ,ᾖ,ᾑ,ᾕ,ᾓ,ᾗ,ῳ,ῴ,ῲ,ῷ,ᾠ,ᾤ,ᾢ,ᾦ,ᾡ,ᾥ,ᾣ,ᾧ,ῤ,ῥ,Ἀ,Ἄ,Ἂ,Ἆ,Ἁ,Ἅ,Ἃ,Ἇ,Ἐ,Ἔ,Ἒ,Ἑ,Ἕ,Ἓ,Ἠ,Ἤ,Ἢ,Ἦ,Ἡ,Ἥ,Ἣ,Ἧ,Ἰ,Ἴ,Ἲ,Ἶ,Ἱ,Ἵ,Ἳ,Ἷ,Ὀ,Ὄ,Ὂ,Ὁ,Ὅ,Ὃ,Ὑ,Ὕ,Ὓ,Ὗ,Ὠ,Ὤ,Ὢ,Ὦ,Ὡ,Ὥ,Ὣ,Ὧ,ᾈ,ᾌ,ᾊ,ᾎ,ᾉ,ᾍ,ᾋ,ᾏ,ᾘ,ᾜ,ᾚ,ᾞ,ᾙ,ᾝ,ᾛ,ᾟ,ᾨ,ᾬ,ᾪ,ᾮ,ᾩ,ᾭ,ᾫ,ᾯ,Ῥ,Α,Β,Γ,Δ,Ε,Ζ,Η,Θ,Ι,Κ,Λ,Μ,Ν,Ξ,Ο,Π,Ρ,Σ,Τ,Υ,Φ,Χ,Ψ,Ω");
    $replace = explode(",","α,α,α,α,α,α,α,α,α,α,α,α,α,ε,ε,ε,ε,ε,ε,ε,ε,η,η,η,η,η,η,η,η,η,η,η,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ο,ο,ο,ο,ο,ο,ο,ο,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,ω,ω,ω,ω,ω,ω,ω,ω,ω,ω,ω,αι,αι,αι,αι,αι,αι,αι,αι,αι,αι,αι,αι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ρ,ρ,α,α,α,α,α,α,α,α,ε,ε,ε,ε,ε,ε,η,η,η,η,η,η,η,η,ι,ι,ι,ι,ι,ι,ι,ι,ο,ο,ο,ο,ο,ο,υ,υ,υ,υ,ω,ω,ω,ω,ω,ω,ω,ω,αι,αι,αι,αι,αι,αι,αι,αι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ρ,α,β,γ,δ,ε,ζ,η,θ,ι,κ,λ,μ,ν,ξ,ο,π,ρ,σ,τ,υ,φ,χ,ψ,ω");
    $new_content = str_replace($search, $replace, $content); 			// Removes diacritics

    $new_name = dirname($corpus_file) .DIRECTORY_SEPARATOR. basename($corpus_file, ".txt") . "-stripped.txt";

    file_put_contents($new_name, $new_content);
    print "Content printed to $new_name";




//    print $new_content;
} else {
    print "File $corpus_file does not exist. You need to generate it with the compile_corpus.php-file";
    die();
}

?> 