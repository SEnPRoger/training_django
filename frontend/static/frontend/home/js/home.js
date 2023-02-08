function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function printCookie() {
    var theCookies = document.cookie.split(';');
    var aString = '';
    for (var i = 1 ; i <= theCookies.length; i++) {
        aString += i + ' ' + theCookies[i-1] + "\n";
    }
    console.log(aString);
}

function check_cookie_name(name) 
    {
      var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
      if (match) {
        console.log(match[2]);
      }
      else{
           console.log('--something went wrong---');
      }
   }

// function login() {
//     var url = "http://127.0.0.1:8000/api/account/settings"
//     fetch(url, {
//         method: 'GET',
//         headers: {
//             'Content-type': 'application/json',
//             'X-CSRFToken': csrftoken, 
//         },
//         body: JSON.stringify({'email':'senproger@gmail.com', 'password':'12345678Qw'})
//     }).then(response=>response.json())
//     .then(data=>{ console.log(data);})
// }