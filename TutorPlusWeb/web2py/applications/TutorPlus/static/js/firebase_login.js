firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    window.alert("You successfully login!")
  } else {
    window.alert("You haven't login!")
  }
});
function login(){

    var userEmail = document.getElementById("username_field").value;
    var userPass = document.getElementById("password_field").value;
    window.alert(userEmail + " " + userPass);

    firebase.auth().signInWithEmailAndPassword(userEmail, userPass).catch(function(error) {
      // Handle Errors here.
      var errorCode = error.code;
      var errorMessage = error.message;
      windows.alert("Error : " + errorMessage);
    });
}

function signout(){
    firebase.auth().signOut().then(function() {
  // Sign-out successful.
    }).catch(function(error) {
      windows.alert("Error : " + error);
    });
}