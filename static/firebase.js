import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
import { getStorage, ref, uploadBytes } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-storage.js";

const firebaseConfig = {
    apiKey: "AIzaSyBEKC0POE6oa2HDEutoYvIBogheWb3082U",
    authDomain: "garjna2k25.firebaseapp.com",
    projectId: "garjna2k25",
    storageBucket: "garjna2k25.appspot.com",
    messagingSenderId: "76079966769",
    appId: "1:76079966769:web:93bed255f7167454b1c310",
    measurementId: "G-79T462X0WK"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth();
const storage = getStorage(app);

export async function uploadFile(file) {
    const storageRef = ref(storage, 'uploads/' + file.name);
    await uploadBytes(storageRef, file);
    alert('File uploaded!');
}

// Example Firebase upload complete handler
uploadTask.then((snapshot) => {
  snapshot.ref.getDownloadURL().then((downloadURL) => {
    fetch('/firebase_upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        filename: file.name,
        firebase_url: downloadURL
      })
    });
  });
});
