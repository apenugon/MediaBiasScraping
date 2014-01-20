<?php
$json_string = file_get_contents('foodnet.json');

echo "sup";

$data = json_decode($json_string, true);

$mysqli = mysqli_connect('ec2-54-201-43-92.us-west-2.compute.amazonaws.com', 'mysql', 'tech', 'TECHCOMM');

echo "Made it here";

#$query =  <<<SQL
#INSERT INTO recipe ('TOTALTIME', 'PREPTIME', 'TITLE', 'COOKTIME', 'INGREDIENTS', 'DIRECTIONS', 'SOURCE')
#VALUES (?, ?, ?, ?, ?, ?, ?)
#SQL;

function clean($string) {
  #$string = str_replace('', '-', $string); // Replaces all spaces with hyphens.
  
 
  $string = preg_replace('/[^A-Za-z0-9.,]/', ' ', $string); // Removes special chars.
 
  return $string;
}

foreach ($data as $key => $value) {
  
    $query = "INSERT INTO recipe VALUES ('" . $value['TotalTime'] . "', '" . $value['PrepTime'] . "', '" . clean($value['Title']) . "', '" . $value['CookTime'] . "', '" . clean(json_encode($value['Ingredients'])) . "', '" . clean(json_encode($value['Directions'])) . "', '" . $value['Source'] . "')";
    



    #$value['TotalTime'],
    #$value['PrepTime'],
    #$value['Title'],
    #$value['CookTime'],
    #$value['Ingredients'],
    #$value['Directions'],
    #$value['Source']
    if (!mysqli_query($mysqli, $query))
    {
      die("Error: " . mysqli_error($mysqli));
    }
}

mysqli_close($mysqli);

?>
