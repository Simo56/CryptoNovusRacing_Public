<?php
header("HTTP/1.1 200 OK");
header('Content-type: application/json');
header("Access-Control-Allow-Origin: *");
include "/home/bitnami/BackendFolder/db_config.php";

//read last available token ID
if (!file_exists("AvailableID.txt")) { 
    die(/*__DIR__.*/' & File does not exist');
}
clearstatcache();
$myfileReading = fopen("AvailableID.txt", "r") or die("Unable to open file FOR READING 1!");
$lastAvailableID = intval(fread($myfileReading,filesize("AvailableID.txt")));
fclose($myfileReading);
$myfileWriting = fopen("AvailableID.txt", "w") or die("Unable to open file FOR WRITING 1!");
fwrite($myfileWriting, $lastAvailableID+1);
fclose($myfileWriting);

$TokenName = $_POST['_tokenNameData'];


$_baseURI = "https://ipfs.infura.io/ipfs/";
$_websiteLink = "www.cryptonovusracing.com";
$_description = "A unique car generated from the Crypto Novus Racing Project!";

$myObjForJSON->name = $TokenName;
$myObjForJSON->description = $_description;
$myObjForJSON->external_url = $_websiteLink;


// prepare and bind
$stmt = $con->prepare("SELECT ipfsURI FROM renderedcars WHERE id = ?");
$stmt->bind_param("i", intval($lastAvailableID));
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($ipfsURI);
$stmt->fetch();
$myObjForJSON->image = $ipfsURI;

### SKIN ###
// prepare and bind
$stmt = $con->prepare("SELECT skinName FROM renderedcars WHERE id = ?;");
$stmt->bind_param("i", $lastAvailableID);
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($skinName);
$stmt->fetch();
$propertiesArray= ["skinName" => $skinName];
### SKIN ###

### SPOILER ###
// prepare and bind
$stmt = $con->prepare("SELECT spoilerName FROM renderedcars WHERE id = ?;");
$stmt->bind_param("i", $lastAvailableID);
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($spoilerName);
$stmt->fetch();
$propertiesArray= ["spoilerName" => $spoilerName];

$stmt = $con->prepare("SELECT spoilerPower FROM renderedcars WHERE id = ?;");
$stmt->bind_param("i", $lastAvailableID);
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($spoilerPower);
$stmt->fetch();
$propertiesArray= ["spoilerPower" => $spoilerPower];
### SPOILER ###

### WHEEL ###
// prepare and bind
$stmt = $con->prepare("SELECT wheelName FROM renderedcars WHERE id = ?;");
$stmt->bind_param("i", $lastAvailableID);
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($wheelName);
$stmt->fetch();
$propertiesArray= ["wheelName" => $wheelName];

$stmt = $con->prepare("SELECT wheelPower FROM renderedcars WHERE id = ?;");
$stmt->bind_param("i", $lastAvailableID);
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($wheelPower);
$stmt->fetch();
$propertiesArray= ["wheelPower" => $wheelPower];
### WHEEL ###

### BUMPER ###
// prepare and bind
$stmt = $con->prepare("SELECT bumperName FROM renderedcars WHERE id = ?;");
$stmt->bind_param("i", $lastAvailableID);
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($bumperName);
$stmt->fetch();
$propertiesArray= ["bumperName" => $bumperName];

$stmt = $con->prepare("SELECT bumperPower FROM renderedcars WHERE id = ?;");
$stmt->bind_param("i", $lastAvailableID);
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($bumperPower);
$stmt->fetch();
$propertiesArray= ["bumperPower" => $bumperPower];
### BUMPER ###

### CARBODY ###
// prepare and bind
$stmt = $con->prepare("SELECT carBodyName FROM renderedcars WHERE id = ?;");
$stmt->bind_param("i", $lastAvailableID);
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($carBodyName);
$stmt->fetch();
$propertiesArray= ["carBodyName" => $carBodyName];

$stmt = $con->prepare("SELECT carBodyPower FROM renderedcars WHERE id = ?;");
$stmt->bind_param("i", $lastAvailableID);
$stmt->execute();
// bind and fetch the result
$stmt->bind_result($carBodyPower);
$stmt->fetch();
$propertiesArray= ["carBodyPower" => $carBodyPower];
### CARBODY ###


$myObjForJSON->properties = $propertiesArray;

//close the connections with the database
$stmt->close();
$con->close();

$myJSON = json_encode($myObjForJSON);
//write json to file
file_put_contents("fileJSONDaCaricareIPFS.json", $myJSON);

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, 'https://ipfs.infura.io:5001/api/v0/add?pin=true');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POST, 1);
$postfields = array('file' => '@' . '/fileJSONDaCaricareIPFS.json');
curl_setopt($ch, CURLOPT_POSTFIELDS, $postfields);

$headers = array();
$headers[] = 'Content-Type: multipart/form-data';
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

$result = curl_exec($ch);
if (curl_errno($ch)) {
    echo 'Error:' . curl_error($ch);
}
curl_close($ch);
$header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
$header = substr($result, 0, $header_size);
$body = substr($result, $header_size);

echo $_baseURI.$body['Hash'];
exit();
?>