// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCOni_tbO1u590ztnIrMX0YETJXNNd37-o",
  authDomain: "medicosaus.firebaseapp.com",
  projectId: "medicosaus",
  storageBucket: "medicosaus.firebasestorage.app",
  messagingSenderId: "877693374023",
  appId: "1:877693374023:web:03ed64f7635ce44a372b62",
  measurementId: "G-VTEVTV6Z9P"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);