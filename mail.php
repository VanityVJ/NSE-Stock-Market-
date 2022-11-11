<?php
//get data from form  
$name = $_POST['name'];
$email= $_POST['email'];
$mobnumber = $_POST['mobile'];
$names = $_POST['names'];
$message= $_POST['message'];
$to = "hublichristianassembly@gmail.com";
$subject = "Mail From HCA website";
$txt ="Name = ". $name . "\r\n  Email = " . $email . "\r\n Subject = " . $names . "\r\n Message =" . $message ."\r\n Mobile Num =" . $mobnumber ;
$headers = "From: hcawebsite@yoursite.com" . "\r\n" .
"CC: vanitygaming4@gmail.com";
if($email!=NULL){
    mail($to,$subject,$txt,$headers);
}
//redirect
header("Location:thankyou.html");
?>