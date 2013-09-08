<?php 
header('Content-Type: text/html;charset=UTF-8');


$filename = "/wordlist/transform.txt";


$dir = '/Users/Michael/Dropbox/Filologi/Projects/Books/Kardinaldyderne/Ordstudier/tools/DB'.$filename;
$content = file_get_contents($dir);



$content = str_replace("(", "[", $content);
$content = str_replace(")", "]", $content);
$content = str_replace(": ", ",", $content);


$content = preg_replace("/\[([^\[\]]++|(?R))*+\]/","",$content); // Remove parentheses
$content = preg_replace('/(^\s.*?|\n\s.*?)\n/', '\1->', $content); // Convert [space]lemma[return] to [lemma]->
$content = preg_replace('/\n\s/', ";", $content ); 	// Convert [return][space] to ;
$content = preg_replace( '/\s+/', "", $content ); 	// Remove excessive whitespace
//$content = str_replace(", ", "\r", $content);

$search =  explode(",","ά,ὰ,ᾶ,ἀ,ἄ,ἂ,ἆ,ἁ,ἅ,ἃ,ἇ,ᾱ,ᾰ,έ,ὲ,ἐ,ἔ,ἒ,ἑ,ἕ,ἓ,ή,ὴ,ῆ,ἠ,ἤ,ἢ,ἦ,ἡ,ἥ,ἣ,ἧ,ί,ὶ,ῖ,ἰ,ἴ,ἲ,ἶ,ἱ,ἵ,ἳ,ἷ,ϊ,ΐ,ῒ,ῗ,ό,ὸ,ὀ,ὄ,ὂ,ὁ,ὅ,ὃ,ύ,ὺ,ῦ,ὐ,ὔ,ὒ,ὖ,ὑ,ὕ,ὓ,ὗ,ϋ,ΰ,ῢ,ῧ,ώ,ὼ,ῶ,ὠ,ὤ,ὢ,ὦ,ὡ,ὥ,ὣ,ὧ,ᾳ,ᾴ,ᾲ,ᾷ,ᾀ,ᾄ,ᾂ,ᾆ,ᾁ,ᾅ,ᾃ,ᾇ,ῃ,ῄ,ῂ,ῇ,ᾐ,ᾔ,ᾒ,ᾖ,ᾑ,ᾕ,ᾓ,ᾗ,ῳ,ῴ,ῲ,ῷ,ᾠ,ᾤ,ᾢ,ᾦ,ᾡ,ᾥ,ᾣ,ᾧ,ῤ,ῥ,Ἀ,Ἄ,Ἂ,Ἆ,Ἁ,Ἅ,Ἃ,Ἇ,Ἐ,Ἔ,Ἒ,Ἑ,Ἕ,Ἓ,Ἠ,Ἤ,Ἢ,Ἦ,Ἡ,Ἥ,Ἣ,Ἧ,Ἰ,Ἴ,Ἲ,Ἶ,Ἱ,Ἵ,Ἳ,Ἷ,Ὀ,Ὄ,Ὂ,Ὁ,Ὅ,Ὃ,Ὑ,Ὕ,Ὓ,Ὗ,Ὠ,Ὤ,Ὢ,Ὦ,Ὡ,Ὥ,Ὣ,Ὧ,ᾈ,ᾌ,ᾊ,ᾎ,ᾉ,ᾍ,ᾋ,ᾏ,ᾘ,ᾜ,ᾚ,ᾞ,ᾙ,ᾝ,ᾛ,ᾟ,ᾨ,ᾬ,ᾪ,ᾮ,ᾩ,ᾭ,ᾫ,ᾯ,Ῥ,Α,Β,Γ,Δ,Ε,Ζ,Η,Θ,Ι,Κ,Λ,Μ,Ν,Ξ,Ο,Π,Ρ,Σ,Τ,Υ,Φ,Χ,Ψ,Ω");
$replace = explode(",","α,α,α,α,α,α,α,α,α,α,α,α,α,ε,ε,ε,ε,ε,ε,ε,ε,η,η,η,η,η,η,η,η,η,η,η,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ι,ο,ο,ο,ο,ο,ο,ο,ο,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,υ,ω,ω,ω,ω,ω,ω,ω,ω,ω,ω,ω,αι,αι,αι,αι,αι,αι,αι,αι,αι,αι,αι,αι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ρ,ρ,α,α,α,α,α,α,α,α,ε,ε,ε,ε,ε,ε,η,η,η,η,η,η,η,η,ι,ι,ι,ι,ι,ι,ι,ι,ο,ο,ο,ο,ο,ο,υ,υ,υ,υ,ω,ω,ω,ω,ω,ω,ω,ω,αι,αι,αι,αι,αι,αι,αι,αι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ηι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ωι,ρ,α,β,γ,δ,ε,ζ,η,θ,ι,κ,λ,μ,ν,ξ,ο,π,ρ,σ,τ,υ,φ,χ,ψ,ω");
$content = str_replace($search, $replace, $content); // Removes diacritics

$content = str_replace(";", "\r", $content);


file_put_contents($dir, $content);



echo "<pre>";
echo $content;
echo "</pre>";

?> 