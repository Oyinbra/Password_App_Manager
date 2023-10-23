// JavaScript function to show/hide password 

function myFunction(pid) {
  var x = document.getElementById(pid);
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}