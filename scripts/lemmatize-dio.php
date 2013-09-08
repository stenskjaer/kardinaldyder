<?php 
header('Content-Type: text/html;charset=UTF-8');

	function utf8($num)
	{
		$num = hexdec($num);
		if($num<=0x7F)       return chr($num);
		if($num<=0x7FF)      return chr(($num>>6)+192).chr(($num&63)+128);
		if($num<=0xFFFF)     return chr(($num>>12)+224).chr((($num>>6)&63)+128).chr(($num&63)+128);
		if($num<=0x1FFFFF)   return chr(($num>>18)+240).chr((($num>>12)&63)+128).chr((($num>>6)&63)+128).chr(($num&63)+128);
		return '';
	}
	
	//Conversions array : "BETACODE" => "UNICODE-HEX"
	//I made three different arrays for now : $letters, $diacritics and $puncts
	$letters = array(
	"*A" => "0391",
	"A" => "03B1",
	"*B" => "0392",
	"B" => "03B2",
	"*C" => "039E",
	"C" => "03BE",
	"*D" => "0394",
	"D" => "03B4",
	
	"*E" => "0395",
	"E" => "03B5",
	"*F" => "03A6",
	"F" => "03C6",
	"*G" => "0393",
	"G" => "03B3",
	"*H" => "0397",
	"H" => "03B7",
	"*I" => "0399",
	"I" => "03B9",
	"*K" => "039A",
	"K" => "03BA",
	"*L" => "039B",
	"L" => "03BB",
	"*M" => "039C",
	"M" => "03BC",
	"*N" => "039D",
	"N" => "03BD",
	"*O" => "039F",
	"O" => "03BF",
	"*P" => "03A0",
	"P" => "03C0",
	"*Q" => "0398",
	"Q" => "03B8",
	"*R" => "03A1",
	"R" => "03C1",
	"*S" => "03A3",
	"S" => "03C3",
	"S1" => "03C3",
	"S2" => "03C2",
	"*S3" => "03F9",
	"S3" => "03F2",
	"*T" => "03A4",
	"T" => "03C4",
	"*U" => "03A5",
	"U" => "03C5",
	"*V" => "03DC",
	"V" => "03DD",
	"*W" => "03A9",
	"W" => "03C9",
	"*X" => "03A7",
	"X" => "03C7",
	"*Y" => "03A8",
	"Y" => "03C8",
	"*Z" => "0396",
	"Z" => "03B6",
	);
	$diacritics = array(
	")" => "0313" ,
	"(" => "0314" ,
	"/" => "0301" ,
	"=" => "0342" ,
	"\\" => "0300" ,
	"+" => "0308" ,
	"|" => "0345" ,
	"?" => "0323"
	);
	
	$puncts = array(
		"." => "002E" ,
		"," => "002C" ,
		":" => "00B7" ,
		";" => "003B" ,
		"'" => "2019" ,
		"-" => "2010" ,
		"_" => "2014"
	);
	
	function convertFromBetaCode($s) // $s as string to convert from BETACODE to HEX
	{
		global $letters, $diacritics, $puncts;
		//$s = str_replace("\r", "\\r", str_replace("\n", "\\n", $s)); // Problems where e\n is understood as ~ "e<br />"
		$end = "";//This var is used for Majs : diacritics are written before majs so we create a var to add after the maj. 
		$string = "";//Set the return string
		for($k = 0; $k < strlen($s); $k++)//We make a loop for every chars
		{
			$v = strtoupper($s[$k]);//We go to upper because BETACODE is written for uppercase
			if($v == "*")//If there's a *, it's a maj. * can't be treated alone
			{
				$next = $k+1;//Next char ID
				//If next char is a letter
				if(isset($letters[$v.strtoupper($s[$next])]))
				{
					$string .= utf8($letters[$v.strtoupper($s[$next])]);
					$k=$next;//We go to next char
				}
				//If next char is diacritics, as diac are written before letter when it's uppercase
				elseif(isset($diacritics[$s[$next]]))
				{
					//We make a new loop until we find an uppercase char
					for($k2 = $k; $k2 < strlen($s); $k2++)
					{
						//Go to upper case because betacode
						$v2 = strtoupper($s[$k2]);
						if(isset($diacritics[$v2]))//Si it's diacritic
						{
							$end .= utf8($diacritics[$v2]); //We add $end the diacritics char
						}
						elseif(isset($letters[$v2]))//If it's a letter
						{
							$string .= utf8($letters["*".$v2]).$end;//We print the maj  with $end var which contain every diacritics for this letter
							$k = $k2;//We jump in the Parent loop
							$end = "";//We reset end
							break;//We break the loop
						}
					}
				}
				else//If we don't know the char, lets print it for debug
				{
					$string .= $v.$s[$k+1];
				}
			}
			elseif(($k != 0) && ($s[$k-1] != "*"))//If it's not a maj => Putting $k!=0 to be sure that $s will return something
			{
				//If we have a latter
				if(isset($letters[$v]))
				{
					$string .= utf8($letters[$v]);//We add to the string
				}
				//Diacritics
				elseif(isset($diacritics[$v]))
				{
					$string .= utf8($diacritics[$v]);
				}
				//Punctuation
				elseif(isset($puncts[$v]))
				{
					$string .= utf8($puncts[$v]);
				}
				//If we don't know the char, lets print it for debug
				else
				{
					$string .=$v;
				}
			}
		}
		//End of Loop
		
		//We return the value
		return $string;
	}





$dir = '/Users/Michael/Dropbox/Filologi/Workspace/Projects/kardinaldyderne/ordstudier/tools/DB/wordlist/diogenes/split/';
$new_dir = $dir . "out/";
$split_dir = $dir . "*";
$new_file = $new_dir . "result.txt";

foreach(glob($split_dir) as $file) {    
    $content = file_get_contents($file);

    $content = "\n" . $content; 		// Add newline at beginning of string.
	$content = preg_replace("/\([^()]*\)/","",$content); // Remove parentheses
    $content = preg_replace("/\([^()]*\)/","",$content); // Remove parentheses
    $content = preg_replace('/\d+/',' ',$content);

    $content = preg_replace('/\n/', ";", $content ); 	// Convert [return][space] to ;
    $content = preg_replace( '/\s+/', " ", $content ); 	// Remove excessive whitespace

    $content = str_replace(";", "\n", $content); // Convert ; to linebreak

    $content = preg_replace("/[,]+/", ",", $content);
    
    // $content = convertFromBetaCode($content);
    
    file_put_contents($new_file, $content, FILE_APPEND);
    
}





//$content = str_replace("(", "[", $content);
//$content = str_replace(")", "]", $content);
//$content = str_replace(": ", ",", $content);


// $content = preg_replace("/\([^()]*\)/",",",$content); // Remove parentheses
// $content = preg_replace("/\([^()]*\)/",",",$content); // Remove parentheses
// $content = preg_replace('/\d+/','->',$content);
//  
// $content = preg_replace('/\n/', ";", $content ); 	// Convert [return][space] to ;
// $content = preg_replace( '/\s+/', "", $content ); 	// Remove excessive whitespace
//  
// $content = str_replace(";", "\r", $content); // Convert ; to linebreak
//  
// $content = preg_replace("/[,]+/", ",", $content);


//file_put_contents($dir, $content);






?> 