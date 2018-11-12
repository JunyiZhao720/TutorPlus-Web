// check login states
firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {

        console.log(idToken)
        // Send token to your backend via HTTPS
        $.post(check_userId_url, {
            userId: idToken
        });

    }).catch(function(error) {
      // Handle error
        const errorMessage = error.message;
        windows.alert("Error : " + errorMessage);
    });

  } else{
      // not logging in
  }
});

// login function
function login(){

    var userEmail = document.getElementById("username_field").value;
    var userPass = document.getElementById("password_field").value;

    firebase.auth().signInWithEmailAndPassword(userEmail, userPass).catch(function(error) {
        // Handle Errors here.
        var errorCode = error.code;
        const errorMessage = error.message;
        windows.alert("Error : " + errorMessage);
    })
}

// signout function
function signout(){
    firebase.auth().signOut().then(function() {
  // Sign-out successful.
    }).catch(function(error) {
      windows.alert("Error : " + error);
    });
}