function validate() {

    var username = document.getElementById("username").value;
    var secretpassword = document.getElementById("password").value;

    if (username == "admin" && secretpassword == "admin") {


        window.open('Nindex.html', '_self');


    }
    else {

        alert("login failed pls retry")
    }

}