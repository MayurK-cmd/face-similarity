// import React, { useState } from "react";
// import axios from "axios";
// import "./App.css"; // Ensure the CSS file is imported

// function App() {
//   const [selectedFile, setSelectedFile] = useState(null);
//   const [message, setMessage] = useState("");
//   const [similarity, setSimilarity] = useState("");

//   const handleFileChange = (e) => {
//     setSelectedFile(e.target.files[0]);
//     setMessage("");
//     setSimilarity("");
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     if (!selectedFile) {
//       setMessage("Please select an image to upload.");
//       return;
//     }

//     const formData = new FormData();
//     formData.append("file", selectedFile);

//     try {
//       const response = await axios.post("http://localhost:8000/predict/", formData, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });

//       setMessage(response.data.message);
//       if (response.data.similarity) {
//         setSimilarity(response.data.similarity);
//       }
//     } catch (error) {
//       console.error("Error:", error.message);
//       setMessage("An error occurred while processing the image.");
//     }
//   };

//   return (
//     <div className="app-container">
//       <h1>Image Similarity Detector</h1>
//       <form onSubmit={handleSubmit}>
//         <input type="file" onChange={handleFileChange} accept="image/*" />
//         <button type="submit">Upload & Compare</button>
//       </form>
//       {message && <h3>{message}</h3>}
//       {similarity && <h3 style={{ color: "green" }}>Similarity: {similarity}</h3>}
//     </div>
//   );
// }

// export default App;



import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Ensure the CSS file is imported

function App() {
  const [selectedFile1, setSelectedFile1] = useState(null);
  const [selectedFile2, setSelectedFile2] = useState(null);
  const [preview1, setPreview1] = useState(null);
  const [preview2, setPreview2] = useState(null);
  const [message, setMessage] = useState("");
  const [similarity, setSimilarity] = useState("");

  const handleFileChange1 = (e) => {
    const file = e.target.files[0];
    setSelectedFile1(file);
    setPreview1(URL.createObjectURL(file));
    setMessage("");
    setSimilarity("");
  };

  const handleFileChange2 = (e) => {
    const file = e.target.files[0];
    setSelectedFile2(file);
    setPreview2(URL.createObjectURL(file));
    setMessage("");
    setSimilarity("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile1 || !selectedFile2) {
      setMessage("Please select both images.");
      return;
    }

    const formData = new FormData();
    formData.append("file1", selectedFile1);
    formData.append("file2", selectedFile2);

    try {
      const response = await axios.post("http://localhost:8000/predict/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage(response.data.message);
      setSimilarity(response.data.similarity);
    } catch (error) {
      console.error("Error:", error.response?.data || error.message);
      setMessage("An error occurred while processing the images.");
    }
  };

  return (
    <div className="app-container">
      <h1>Image Similarity Detector</h1>
      <form onSubmit={handleSubmit}>
        <div className="upload-container">
          <div className="image-upload">
            <label>Upload Image 1:</label>
            <input type="file" onChange={handleFileChange1} accept="image/*" />
            {preview1 && <img src={preview1} alt="Preview 1" className="image-preview" />}
          </div>
          <div className="image-upload">
            <label>Upload Image 2:</label>
            <input type="file" onChange={handleFileChange2} accept="image/*" />
            {preview2 && <img src={preview2} alt="Preview 2" className="image-preview" />}
          </div>
        </div>
        <button type="submit">Compare Images</button>
      </form>
      {message && <h3>{message}</h3>}
      {similarity && <h3 style={{ color: "green" }}>Similarity: {similarity}</h3>}
    </div>
  );
}

export default App;
