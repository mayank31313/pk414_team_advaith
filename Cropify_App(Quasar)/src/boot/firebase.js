// Firebase App (the core Firebase SDK) is always required and
// must be listed before other Firebase SDKs
import * as firebase from "firebase/app";

// Add the Firebase services that you want to use
import "firebase/database";

// Your web app's Firebase configuration
var firebaseConfig = {
  apiKey: "AIzaSyA7tb5-K_KqVbEfybO78GKiqp3GDB3Adgs",
  authDomain: "cropify-51d79.firebaseapp.com",
  databaseURL: "https://cropify-51d79.firebaseio.com",
  projectId: "cropify-51d79",
  storageBucket: "cropify-51d79.appspot.com",
  messagingSenderId: "576927689097",
  appId: "1:576927689097:web:a03f38b21f8b54ff1b5958"
};
// Initialize Firebase
let firebaseApp = firebase.initializeApp(firebaseConfig);
let firebaseDb = firebaseApp.database()
//let messaging = firebase.messaging()

export { firebaseDb }