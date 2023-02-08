const container = document.querySelector(".container"),
      pwShowHide = document.querySelectorAll(".showHidePw"),
      pwFields = document.querySelectorAll(".password"),
      signUp = document.querySelector(".signup-link"),
      login = document.querySelector(".login-link");

      login_button = document.getElementById("login_button")
      register_button = document.getElementById("register_button")

let current_register_username, current_register_email = null
let username_has_changed, email_has_changed = false

let username_occupied = false
let email_occupied = false

    //   js code to show/hide password and change icon
    pwShowHide.forEach(eyeIcon =>{
        eyeIcon.addEventListener("click", ()=>{
            pwFields.forEach(pwField =>{
                if(pwField.type ==="password"){
                    pwField.type = "text";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye-slash", "uil-eye");
                    })
                }else{
                    pwField.type = "password";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye", "uil-eye-slash");
                    })
                }
            }) 
        })
    })

    var register_interval = null;
    var login_interval = null;

    // js code to appear signup and login form
    signUp.addEventListener("click", ( )=>{
        container.classList.add("active");

        if (login_interval != null) {
            clearInterval(login_interval)
        }
        register_interval = setInterval(register_validation, 100);
    });
    login.addEventListener("click", ( )=>{
        container.classList.remove("active");

        if (register_interval != null) {
            clearInterval(register_interval)
        }
        login_interval = setInterval(login_validation, 100);
    });

    login_button.addEventListener("click", ()=>{
        login_ajax();
    })
    register_button.addEventListener("click", ()=>{
        register_ajax();
    })

    //======================================================================
    // GET COOKIES
    //======================================================================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    //======================================================================
    // CHECKING IF ALL INPUTS ARE CORRECT WHILE LOGIN
    //======================================================================
    function login_validation() {
        var username_or_email = document.getElementById("login_email_or_username").value
        var password = document.getElementById("login_password").value

        if (username_or_email == "" || password == "") {
            login_button.disabled = true
        } else {
            login_button.disabled = false
        }
    }

    //======================================================================
    // CHECKING IF ALL INPUTS ARE CORRECT WHILE REGISTRATION
    //======================================================================
    function register_validation() {
        var username = document.getElementById("register_username").value
        var email = document.getElementById("register_email")
        var password = document.getElementById("register_password").value
        var password2 = document.getElementById("register_password2").value

        var terms_accept = document.getElementById("termCon").checked

        if (username == "" || email.value == "" || email.validity.typeMismatch 
                                || password == "" || password2 == "" || password != password2 || !terms_accept
                                || username_occupied == true || email_occupied == true) {
            register_button.disabled = true
        } else {
            register_button.disabled = false
        }
    }

    function validateEmail(email) {
        var re = /\S+@\S+\.\S+/;
        return re.test(email);
    }

    //======================================================================
    // LOGIN UNTO ACCOUNT (AJAX)
    //======================================================================
    function login_ajax() {
        //var login_form = document.getElementById("login_form")
        var login_url = `http://127.0.0.1:8000/api/account/login`

        var username_or_email = document.getElementById("login_email_or_username").value
        var password = document.getElementById("login_password").value
        // var checkBoxValue2 = document.querySelector(".checkbox-" + current_edit_elem.id).checked

        var json = (validateEmail(username_or_email) != true) ? {'username':username_or_email, 'password':password}
         : {'email':username_or_email, 'password':password}

        console.log(json)
    
        fetch(login_url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(json)
        })
        .then(response=>response.json())
        .then(data=>{ console.log(data); })
        // .then(function(response){
        //     window.location.replace("http://127.0.0.1:8000");
        // })
    }

    //======================================================================
    // REGISTER ACCOUNT (AJAX)
    //======================================================================
    function register_ajax() {
        var register_form = document.getElementById("register_form")
        var register_url = `http://127.0.0.1:8000/api/account/register`

        var username = document.getElementById("register_username").value
        var email = document.getElementById("register_email").value
        var password = document.getElementById("register_password").value
        var password2 = document.getElementById("register_password2").value
    
        fetch(register_url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken, 
            },
            body: JSON.stringify({'username':username, 'email':email, 'password':password, 'password2':password2})
        }).then(response=>response.json())
        // .then(data=>{ console.log(data); })
        .then(function(response){
            window.location.replace("http://127.0.0.1:8000");
        })
    }

    //======================================================================
    // CHEKING USERNAME AVAILABLE (AJAX)
    //======================================================================
    function check_username_available(username) {
        var username_avalible_url = `http://127.0.0.1:8000/api/account/username-available`
        var username_inputfield = document.getElementById("register_inputfield_username");

        fetch(username_avalible_url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken, 
            },
            body: JSON.stringify({'username':username})
        })
        .then(response=>response.json())
        .then(data=>{
            username_has_changed = false;

            if (data['available'] != "Username can be used") {
                //console.log("Имя занято")
                mark_inputfield(username_inputfield, true)
                username_occupied = true
            } else {
                //console.log("Имя свободно")
                mark_inputfield(username_inputfield, false)
                username_occupied = false
            }
        })
    }
       
    //======================================================================
    // CHEKING EMAIL AVAILABLE (AJAX)
    //======================================================================
    function check_email_available(email) {
        var email_avalible_url = `http://127.0.0.1:8000/api/account/email-available`
        var email_inputfield = document.getElementById("register_inputfield_email")

        fetch(email_avalible_url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken, 
            },
            body: JSON.stringify({'email':email})
        }).then(response=>response.json())
        .then(data=>{ 
            email_has_changed = false;

            if (data['available'] != "Email can be used") {
                //console.log("Имя занято")
                mark_inputfield(email_inputfield, true)
                email_occupied == true
            } else {
                //console.log("Имя свободно")
                mark_inputfield(email_inputfield, false)
                email_occupied == false
            }
        })
        
    }

    //======================================================================
    // MARK INPUTFIELD AVAILABLE (AJAX)
    //======================================================================
    function mark_inputfield(inputfield, is_wrong) {
        if(is_wrong) {
            inputfield.classList.add("error")
        } else {
            inputfield.classList.remove("error")
        }
    }
    
    //======================================================================
    // SEND REQUEST TO CHECK IF USERNAME & EMAIL IS AVAILABLE (AJAX)
    //======================================================================
    document.addEventListener("click", function(event) {
        var username = document.getElementById("register_username").value

        if (event.target.closest(".register_username") || event.target.closest(".signup")
                                || event.target.closest(".input-field")) return
            if (username != "") {
                if (current_register_username == null) {
                    current_register_username = username
                    username_has_changed = true
                } else {
                    if (current_register_username != username) {
                        current_register_username = username
                        username_has_changed = true
                    }
                }

                if (username_has_changed) {
                    check_username_available(username)
                }
            }

        var email = document.getElementById("register_email").value
        
        if (event.target.closest(".email_username") || event.target.closest(".signup")) return
            if (email != "") {
                if (current_register_email == null) {
                    current_register_email = email
                    email_has_changed = true
                } else {
                    if (current_register_email != email) {
                        current_register_email = email
                        email_has_changed = true
                    }
                }

                if (email_has_changed) {
                    check_email_available(email)
                }
            }
    })