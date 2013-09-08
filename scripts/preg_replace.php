<?php 


$filename = "theognis/theognis-001.txt";






$dir = '/Users/Michael/Dropbox/Filologi/Projects/Books/Kardinaldyderne/Ordstudier/Corpora/'.$filename;
$content = file_get_contents($dir);




preg_replace("/\r\n?|\n/", " ", $content);			// Removes line breaks


file_put_contents($dir, $content);




print "<pre>";
print $content;
print "</pre>";

?> 