﻿<?php
mb_internal_encoding("UTF-8");
ini_set('memory_limit', '128M');



$author = "plato";
$corpus_dir = "../../private-korpus/Corpora";
$corpus_subdir = "plato/minor";


$terms = array(" ευσεβ");
$exceptions = array();
$bar_bot = "3";



$freq_factor = 10000;
$width_factor = 10;
$diagram_bars = 7;
$granularity = 4;



/* SCRIPT START
 * No adjustments below this point. */

// Set dir
if ($corpus_subdir) {
    $filename = $corpus_dir .DIRECTORY_SEPARATOR. $corpus_subdir .DIRECTORY_SEPARATOR. $author ."-corpus-stripped.txt";
} else {
    $filename = $corpus_dir .DIRECTORY_SEPARATOR. $author .DIRECTORY_SEPARATOR. $author ."-corpus-stripped.txt";
}

if (file_exists($filename)) {
     $string = file_get_contents($filename);
} else { print "$filename does not exist"; die(1);
}
$strlen = mb_strlen($string);
$bar_top = $bar_bot + 0.5;
$dia_bot = "0";
$dia_top = "3.5";
$Author = ucfirst($author);
$results = array();




/*
**	FUNCTIONS
*/
function strpos_recursive($haystack, $needle, $offset = 0, &$results = array()) {                
    $offset = strpos($haystack, $needle, $offset);
    if($offset === false) {
        return $results;            
    } else {
        $results[] = $offset;
        return strpos_recursive($haystack, $needle, ($offset + 1), $results);
    }
}
function strpos_words($haystack,$needles,$pos_as_key=true) 
{ 
   $idx=0; // Used if pos_as_key is false 
   
   // Iterate the $needles array 
   foreach ( $needles as $needle ) 
   { 
       // Get all occurences of this keyword ($needle)
       $i=0; $pos_cur=0; $pos_found=0; 
       while (  $pos_found !== false && $needles !== '') 
       { 
           // Get the strpos of this keyword (if thereis one) 
           $pos_found = mb_strpos(mb_substr($haystack,$pos_cur),$needle); 
           if ( $pos_found !== false ) 
           { 
               // Set up key for main array 
               $index = $pos_as_key ? $pos_found+$pos_cur : $idx++; 
               
               // Populate main array with this keywords positional data 
               $positions[$index]['start'] = $pos_found+$pos_cur; 
               $pos_cur += ($pos_found+mb_strlen($needle)); 
               $positions[$index]['end']  = $pos_cur; 
               $positions[$index]['word'] = $needle; 
               $i++; 
           } 
       } 
   }
    

   // If we found anything then sort the array and return it 
   if ( isset($positions) ) 
   { 
       ksort($positions); 
       return $positions; 
   } 

   // If nothign was found then return false 
   return false; 
}



/*
**	Positioning of $terms, removal of exceptions
**	Making positions relative to strlen in array $results
**	Reading arrays for subsequent functions
*/
$positions = strpos_words($string,$terms,$pos_as_key=true);
$excep_array = strpos_words($string,$exceptions,$pos_as_key=true);

if($excep_array) {
	foreach($excep_array as $exception) {
		$key = $exception['start'];
		if(array_key_exists($key,$positions)) {
			unset($positions[$key]);
		}
	}
}

$abspos = array();
$passages = array();
$i=0;
foreach($positions as $position) {
	// Reading $results for relative positions.
	$relpos = $position['start'] / $strlen * $width_factor;
	$results[] = number_format($relpos, $granularity);
	
	// Reading the positions for $passages in table
	preg_match('/[\p{L}]+/u',mb_substr($string,$position['start']),$matches[$i]);
	$passages[$i][0] = mb_substr($string,$position['start']-50,50);
	$passages[$i][1] = $matches[$i][0];
	$passages[$i][2] = mb_substr($string,$position['start']+mb_strlen($passages[$i][1])+2,50);
	$i++;
	
	// Reading absolute positions in seperate array for std_dev.
	$abspos[] = $position['start'];
		
}





/*
** Relative position of book marks
**
*/
$titles = array();
if(preg_match_all("/(\[[0-9]{1,2}]\s\{.*?\})+/u",$string,$matches,PREG_OFFSET_CAPTURE)){
    foreach($matches[0] as $match){
    	$match[1] = mb_strpos($string,$match[0]);    
        $titles[] = $match;
    }
}
foreach($titles as $obj) {
	$pos = $obj[1];
	$relpos = $pos / $strlen * $width_factor;
	$titlepos[$obj[0]] = number_format($relpos, 1);
}

/*
** Creating $bookarray, splitting text into array of books
** Complete word count (memory efficient): $word_count
*/
for($i=0; $i < count($titles); $i++) {
	if($i < count($titles) - 1) {
		$length = $titles[$i+1][1] - $titles[$i][1];
	} else {
		$length = $strlen - $titles[$i][1];
	}
	$bookarray[$i] = mb_substr($string, $titles[$i][1], $length);
	$book_word_count[$i] = count(explode(" ", $bookarray[$i]));
}
$word_count = array_sum($book_word_count);



/*
** 	Calculations:
** 	$word_count (int): Word-count.
** 	$expected_distance (int): Mean = expected observation if evenly distributed. $strlen / $count
** 	$obs_dist (array): All observed distances in characters.
** 	$obs_mean (int): Mean of all observed distances. sum($obs_dist) / $count
**  $variance: Variance from mean. (∑(X-μ)^2) / N: 
** 	$std_dev (int): Standard deviation from mean. sqrt($variance)
** 	$var_coef (int): Variation coefficient. $std_dev / $obs_mean
** 	$avg_dev (int): Average absolute deviation normalized over mean of observations. ∑|X-μ| / N div. m. μ
**
*/


/* Create array with all observed distances.
 * A distance = characters between occurrence n and n+1 and distance
 * from last occuren to end of string. 
 * Total count = count of distances.
*/
foreach($abspos as $pos_key => $position) {
    if($pos_key == 0) {
        $obs_dist[$pos_key] = $abspos[$pos_key];
    }
    $obs_dist[$pos_key] = $abspos[$pos_key] - $abspos[$pos_key-1];
}
/* Go to end of array and add distance to end */
end($positions);
end($abspos);
$obs_dist[] = ($strlen) - $positions[current($abspos)]['end'];         // Subtract strlen from last array-key to get
                                                           // distance from last observation to string end
/* Sum count of all distances */
$count = count($obs_dist);


$obs_mean = array_sum($obs_dist) / $count;         // Mean of distance
$expected_distance = $strlen / $count;             // Expected value

foreach ($obs_dist as $observation) {
	$obs_minus_mean[] = pow($observation - $expected_distance, 2); // Needed for variance
	$abs_mean_deviations[] = abs($observation - $expected_distance); // Needed for average dev.
}

$variance = (array_sum($obs_minus_mean)/ $count);
$std_dev = sqrt($variance);
$var_coef = $std_dev / $obs_mean;

foreach ($abs_mean_deviations as $value) {
    $norm_mean_deviation[] = $value / $std_dev;
}
$avg_dev = ((array_sum($abs_mean_deviations) / $count) / $obs_mean);


/*
** WRITE PAGE
** 
*/
print "<pre>";
foreach($terms as $search) {
$found = strpos_recursive($string, $search);

	if($found) {
		print "Found " .substr_count($string, $search). " occurences of ".$search." in the file ".$filename."\n";
	} else {
	    print "String '".$search."' not found in " .$filename. "\n\n";
	}
}

print "Total count (excl. exceptions): ".count($results)."\n";
print "Exceptions removed: ".count($excep_array)."\n";


print "Positions: \n";
foreach($results as $v) {
	print "\draw[very thin](". $v .",".$bar_bot.") -- (". $v .",".$bar_top.");\n";
}


print "\n\n";
print '<table cellpadding="2" border="1">';
print "<tr><td>Word count: </td><td>$word_count</td></tr>";
print "<tr><td>Dist Mean: </td><td>$obs_mean</td></tr>";
print "<tr><td>Std.dev: </td><td>".round($std_dev,2)."</td></tr>";
print "<tr><td>Variance: </td><td>".round($variance,2)."</td></tr>";
print "<tr><td>Var. coef.: </td><td>".round($var_coef,2)."</td></tr>";
print "<tr><td>Average deviation: </td><td>".round($avg_dev,2)."</td></tr>";

print '</table>';


print "\n\n";
print "Passages:\n";
print '<table cellpadding="2" border="1">';
for($i=0; $i<count($passages); $i++) {
	echo '<tr>';
	echo '<td style="text-align:right;">'.$passages[$i][0].'</td>';
	echo '<td style="text-align:center;font-weight:bold;">'.$passages[$i][1].'</td>';
	echo '<td>'.$passages[$i][2].'</td>';
	echo '</tr>';
}
print '</table>';



print "\n\nDraw diagram\n";
// Draw table start
echo "\begin{table}[htbp]\n"; 
echo "\centering\n";
echo "\begin{adjustbox}{width=\linewidth}\n\n";
echo "\begin{tikzpicture}\n\n";


// Draw diagram
$outer_limit_left = -1.5;
$outer_limit_right = $width_factor + 1.5;
$outer_limit_top = ($diagram_bars * 0.5) + 0.75;
$outer_limit_bottom = -0.65;
$inner_limit_left = 0;
$inner_limit_right = $width_factor;
$inner_limit_top = $diagram_bars * 0.5;
$inner_limit_bottom = 0;
$header_baseline = ($diagram_bars * 0.5) + 0.35;
$header_baseline_descender = ($diagram_bars * 0.5) + 0.3;

// Rule widths (= booktabs package)
$heavyrulewidth = "line width=0.08em";
$lightrulewidth = "line width=0.05em";

echo "% Grid\n";
echo "\draw[$heavyrulewidth]($outer_limit_left,$outer_limit_top) -- ($outer_limit_right,$outer_limit_top);						% Top border\n";
echo "\draw[$heavyrulewidth]($outer_limit_left,$outer_limit_bottom) -- ($outer_limit_right,$outer_limit_bottom);			% Bottom border\n";
echo "\draw[very thin,color=gray]($inner_limit_left,$inner_limit_bottom) -- ($inner_limit_left,$inner_limit_top);				% Left vertical border\n";
echo "\draw[$lightrulewidth]($outer_limit_left,$inner_limit_top) -- ($outer_limit_right,$inner_limit_top);								% Mid-top border\n";
echo "\draw[very thin,color=gray]($inner_limit_right,$inner_limit_bottom) -- ($inner_limit_right,$inner_limit_top);			% Right vertical borderr\n";
echo "\draw[very thin,color=gray]($outer_limit_left,$inner_limit_bottom) -- ($outer_limit_right,$inner_limit_bottom);		% Mid-bottom border\n";

for($i=1; $i < $diagram_bars; $i++) {
	$height = $i/2;
	echo "\draw[very thin,color=gray]($outer_limit_left,$height) -- ($outer_limit_right,$height);		% $i. horizontal line\n";
}

// Headers
echo "\n% Headers\n";
echo "\draw ($inner_limit_left,$header_baseline) node[left,color=black] {Lemma};\n";
echo "\draw ($inner_limit_left,$header_baseline_descender) node[right,color=black] {Fordeling};\n";
echo "\draw ($outer_limit_right,$header_baseline) node[left,color=black] {\$\sigma_{norm}$};\n";

// Fyld selv ud
echo "\n\n% Work divisions\n";
$i = 1;
foreach($titlepos as $key => $val) {
		print "\draw[very thin,color=gray](". $val .",".$dia_bot.")node[below,color=black]{" .$i."} -- (". $val .",".$inner_limit_top."); % " . $key . "\n";
		$i++;		
}

echo "\n\n% Word bars (standard)\n";
echo "\draw[very thin,color=gray] (0,0) -- (0,0.25) node[left,color=black] {{\gr ανδρε-}}; 		% 1. bar\n";
echo "\draw[very thin,color=gray] (0,0.25) -- (0,0.75) node[left,color=black] {{\gr δικαι-}}; 		% 2. bar\n";
echo "\draw[very thin,color=gray] (0,0.75) -- (0,1.25) node[left,color=black] {{\gr σοφ-}};		% 3. bar\n";
echo "\draw[very thin,color=gray] (0,1.25) -- (0,1.75) node[left,color=black] {{\gr σωφρ-}};	% 4. bar\n";
echo "\draw[very thin,color=gray] (0,1.75) -- (0,2.25) node[left,color=black] {{\gr φρον-}};		% 5. bar\n";
echo "\draw[very thin,color=gray] (0,2.25) -- (0,2.75) node[left,color=black] {{\gr ὁσι-}};		% 6. bar\n";
echo "\draw[very thin,color=gray] (0,2.75) -- (0,3.25) node[left,color=black] {{\gr εὐσεβ-}};		% 7. bar\n\n";


echo "% Standard deviation, normalized\n";                                        
echo "\draw (11.5,0) (11.5,0.25) node[left,color=black]    {\$xx\$};\n";
echo "\draw (11.5,0.25) (11.5,0.75) node[left,color=black] {\$xx\$};\n";
echo "\draw (11.5,0.75) (11.5,1.25) node[left,color=black] {\$xx\$};\n";
echo "\draw (11.5,1.25) (11.5,1.75) node[left,color=black] {\$xx\$};\n";
echo "\draw (11.5,1.75) (11.5,2.25) node[left,color=black] {\$xx\$};\n";
echo "\draw (11.5,2.25) (11.5,2.75) node[left,color=black] {\$xx\$};\n";
echo "\draw (11.5,2.75) (11.5,3.25) node[left,color=black] {\$xx\$};\n\n";

echo "% ανδρει-\n\n";
echo "% δικαι-\n\n";
echo "% σοφ-\n\n";
echo "% σωφρ-\n\n";
echo "% φρον-\n\n";
echo "% οσι-\n\n";
echo "% εὐσεβ-\n\n";


echo "% closing\n";
echo "\\end{tikzpicture}\n";
echo "\\end{adjustbox}\n";
echo "\caption{Diagram over søgetermernes fordeling hos $Author.}\n";
echo "\label{fig:fordeling:$author}\n";
echo "\\end{table}\n";



print "</pre>";




?>