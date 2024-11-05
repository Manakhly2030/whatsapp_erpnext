import { getFirestore } from "firebase/firestore";


  // Initialize Firebase
  const db = getFirestore(app);

  export { db }