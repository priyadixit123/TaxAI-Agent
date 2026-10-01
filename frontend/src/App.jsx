import { useState } from "react";

import "./App.css";

function App() {

  const [showLogin, setShowLogin] = useState(false);

  const [showSignup, setShowSignup] = useState(false);

  const [files, setFiles] = useState({
  pan: null,
  aadhaar: [],
  salary: [],
  bank: [],
  form16: [],
});

  const handleFileChange = (type, event) => {

  const selectedFiles = Array.from(event.target.files);

  if (selectedFiles.length === 0) {
    return;
  }

  // PAN = only one file
  if (type === "pan") {

    setFiles((previous) => ({
      ...previous,
      pan: selectedFiles[0],
    }));

    return;
  }

  // Other documents = multiple files
  setFiles((previous) => ({
    ...previous,
    [type]: [
      ...previous[type],
      ...selectedFiles,
    ],
  }));

  event.target.value = "";
};

  const scrollToUpload = () => {
    document
      .getElementById("upload")
      .scrollIntoView({ behavior: "smooth" });
  };

  
const processDocuments = async () => {

  console.log("PROCESS BUTTON CLICKED");
  console.log("Current files:", files);

  const formData = new FormData();

  // PAN - single file
  if (files.pan) {
    formData.append("pan", files.pan);
  }

  // Aadhaar - multiple files
  if (Array.isArray(files.aadhaar)) {
    files.aadhaar.forEach((file) => {
      formData.append("aadhaar", file);
    });
  }

  // Salary - multiple files
  if (Array.isArray(files.salary)) {
    files.salary.forEach((file) => {
      formData.append("salary", file);
    });
  }

  // Bank - multiple files
  if (Array.isArray(files.bank)) {
    files.bank.forEach((file) => {
      formData.append("bank", file);
    });
  }

  // Form 16 - multiple files
  if (Array.isArray(files.form16)) {
    files.form16.forEach((file) => {
      formData.append("form16", file);
    });
  }

  try {

    const response = await fetch(
      "http://127.0.0.1:8000/upload",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await response.json();

    console.log(
      "Backend response:",
      JSON.stringify(data, null, 2)
    );

    if (!response.ok) {
      throw new Error(
        data.detail || "Upload failed"
      );
    }

    alert("Documents uploaded successfully!");

  } catch (error) {

    console.error("Upload error:", error);

    alert("Could not connect to backend.");
  }
};


  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="logo">
          <span className="logo-icon">✦</span>
          TAX<span>AI</span>
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#how-it-works">How it works</a>
          <a href="#upload">Upload</a>
        </div>

        <div className="auth-buttons">

  <button
    className="login-button"
    onClick={() => setShowLogin(true)}
  >
    Login
  </button>

  <button
    className="signup-button"
    onClick={() => setShowSignup(true)}
  >
    Sign Up
  </button>

</div>
      </nav>


      {/* HERO SECTION */}
      <section className="hero" id="home">

        <div className="hero-content">

          <div className="badge">
            <span className="pulse-dot"></span>
            AI-Powered Tax Automation
          </div>

          <h1>
            Your Smart
            <br />
            <span>AI Tax Assistant</span>
          </h1>

          <p>
            Upload your tax documents and let AI extract,
            validate and organize your information automatically.
          </p>

          <div className="hero-buttons">
            <button className="primary-button" onClick={scrollToUpload}>
              Start Tax Analysis
              <span>→</span>
            </button>

            <a href="#how-it-works" className="secondary-button">
              How it works
            </a>
          </div>

          <div className="hero-features">
            <span>✓ Document AI</span>
            <span>✓ Smart Validation</span>
            <span>✓ CA Review</span>
          </div>

        </div>


        {/* AI VISUAL */}
        <div className="hero-visual">

          <div className="glow glow-one"></div>
          <div className="glow glow-two"></div>

          <div className="ai-orb">

            <div className="orb-ring ring-one"></div>
            <div className="orb-ring ring-two"></div>

            <div className="orb-core">
              <span>✦</span>
            </div>

          </div>

          <div className="floating-card card-one">
            <span>📄</span>
            <div>
              <strong>Document</strong>
              <small>Detected</small>
            </div>
          </div>

          <div className="floating-card card-two">
            <span>✓</span>
            <div>
              <strong>Validation</strong>
              <small>Ready</small>
            </div>
          </div>

          <div className="floating-card card-three">
            <span>🤖</span>
            <div>
              <strong>AI Agent</strong>
              <small>Processing</small>
            </div>
          </div>

        </div>

      </section>


      {/* HOW IT WORKS */}
      <section className="workflow-section" id="how-it-works">

        <div className="section-heading">

          <div className="section-label">
            SIMPLE PROCESS
          </div>

          <h2>
            From documents to
            <span> tax-ready data</span>
          </h2>

          <p>
            Our AI agent handles the repetitive work while keeping
            important decisions available for human review.
          </p>

        </div>


        <div className="workflow">

          <div className="workflow-card">
            <div className="step-number">01</div>
            <div className="workflow-icon">📄</div>
            <h3>Upload</h3>
            <p>
              Upload your PAN, Aadhaar and salary documents.
            </p>
          </div>

          <div className="workflow-line"></div>

          <div className="workflow-card">
            <div className="step-number">02</div>
            <div className="workflow-icon">🤖</div>
            <h3>AI Reads</h3>
            <p>
              AI reads your documents and extracts useful information.
            </p>
          </div>

          <div className="workflow-line"></div>

          <div className="workflow-card">
            <div className="step-number">03</div>
            <div className="workflow-icon">✓</div>
            <h3>Validate</h3>
            <p>
              The agent checks missing fields and data inconsistencies.
            </p>
          </div>

          <div className="workflow-line"></div>

          <div className="workflow-card">
            <div className="step-number">04</div>
            <div className="workflow-icon">👨‍💼</div>
            <h3>Review</h3>
            <p>
              Final cases can be reviewed and approved by a CA.
            </p>
          </div>

        </div>

      </section>


      {/* UPLOAD SECTION */}
      <section className="upload-section" id="upload">

        <div className="upload-container">

          <div className="section-heading">

            <div className="section-label">
              DOCUMENT CENTER
            </div>

            <h2>
              Upload your <span>documents</span>
            </h2>

            <p>
              Add the documents required for your tax analysis.
            </p>

          </div>


          <div className="upload-grid">

  {/* PAN */}
  <div className={`upload-card ${files.pan ? "uploaded" : ""}`}>

    <div className="document-icon pan-icon">
      🪪
    </div>

    <h3>PAN Card</h3>

    <p>
      Upload your PAN document
    </p>

    <label className="upload-button">
      {files.pan ? "Change File" : "Choose File"}

      <input
        type="file"
        accept=".jpg,.jpeg,.png,.pdf"
        onChange={(event) =>
          handleFileChange("pan", event)
        }
      />
    </label>

    {files.pan && (
      <div className="file-name">
        ✓ {files.pan.name}
      </div>
    )}

    <small>JPG, PNG or PDF</small>

  </div>


  {/* AADHAAR */}
  <div className={`upload-card ${files.aadhaar?.length ? "uploaded" : ""}`}>

    <div className="document-icon aadhaar-icon">
      🆔
    </div>

    <h3>Aadhaar Card</h3>

    <p>
      Upload front and back side
    </p>

    <label className="upload-button">
      {files.aadhaar?.length
        ? "Add More Files"
        : "Choose Files"}

      <input
        type="file"
        multiple
        accept=".jpg,.jpeg,.png,.pdf"
        onChange={(event) =>
          handleFileChange("aadhaar", event)
        }
      />
    </label>

    {files.aadhaar?.length > 0 && (
      <div className="file-list">

        {files.aadhaar.map((file, index) => (
          <div className="file-name" key={index}>
            ✓ {file.name}
          </div>
        ))}

      </div>
    )}

    <small>
      JPG, PNG or PDF · Multiple files
    </small>

  </div>


  {/* SALARY */}
  <div className={`upload-card ${files.salary?.length ? "uploaded" : ""}`}>

    <div className="document-icon salary-icon">
      💰
    </div>

    <h3>Salary Slips</h3>

    <p>
      Upload one or multiple monthly slips
    </p>

    <label className="upload-button">
      {files.salary?.length
        ? "Add More Files"
        : "Choose Files"}

      <input
        type="file"
        multiple
        accept=".jpg,.jpeg,.png,.pdf"
        onChange={(event) =>
          handleFileChange("salary", event)
        }
      />
    </label>

    {files.salary?.length > 0 && (
      <div className="file-list">

        {files.salary.map((file, index) => (
          <div className="file-name" key={index}>
            ✓ {file.name}
          </div>
        ))}

      </div>
    )}

    <small>
      JPG, PNG or PDF · Multiple files
    </small>

  </div>


  {/* BANK STATEMENT */}
  <div className={`upload-card ${files.bank?.length ? "uploaded" : ""}`}>

    <div className="document-icon bank-icon">
      🏦
    </div>

    <h3>Bank Statement</h3>

    <p>
      Upload your bank statements
    </p>

    <label className="upload-button">
      {files.bank?.length
        ? "Add More Files"
        : "Choose Files"}

      <input
        type="file"
        multiple
        accept=".jpg,.jpeg,.png,.pdf"
        onChange={(event) =>
          handleFileChange("bank", event)
        }
      />
    </label>

    {files.bank?.length > 0 && (
      <div className="file-list">

        {files.bank.map((file, index) => (
          <div className="file-name" key={index}>
            ✓ {file.name}
          </div>
        ))}

      </div>
    )}

    <small>
      JPG, PNG or PDF · Multiple files
    </small>

  </div>


  {/* FORM 16 */}
  <div className={`upload-card ${files.form16?.length ? "uploaded" : ""}`}>

    <div className="document-icon form16-icon">
      📑
    </div>

    <h3>Form 16</h3>

    <p>
      Upload your Form 16 document
    </p>

    <label className="upload-button">
      {files.form16?.length
        ? "Add More Files"
        : "Choose Files"}

      <input
        type="file"
        multiple
        accept=".jpg,.jpeg,.png,.pdf"
        onChange={(event) =>
          handleFileChange("form16", event)
        }
      />
    </label>

    {files.form16?.length > 0 && (
      <div className="file-list">

        {files.form16.map((file, index) => (
          <div className="file-name" key={index}>
            ✓ {file.name}
          </div>
        ))}

      </div>
    )}

    <small>
      JPG, PNG or PDF · Multiple files
    </small>

  </div>

</div>



          <div className="privacy-note">
            <span>🔒</span>
            For development, use sample documents and masked Aadhaar data.
          </div>


          <button
            className="process-button"
            disabled={
             !files.pan &&
             files.aadhaar.length === 0 &&
             files.salary.length === 0 &&
             files.bank.length === 0 &&
             files.form16.length === 0
            }
            onClick={processDocuments}
          >
            Process Documents
            <span>→</span>
          </button>

        </div>

      </section>


      {/* FOOTER */}
      <footer>

        <div className="footer-logo">
          ✦ TAX<span>AI</span>
        </div>

        <p>
          Intelligent document processing for tax workflows.
        </p>

        <div className="footer-line"></div>

        <small>
          © 2026 TAXAI · Demo Project
        </small>

      </footer>

    </div>
  );

  {/* LOGIN MODAL */}

{showLogin && (
  <div
    className="modal-overlay"
    onClick={() => setShowLogin(false)}
  >
    <div
      className="auth-modal"
      onClick={(event) => event.stopPropagation()}
    >

      <button
        className="close-button"
        onClick={() => setShowLogin(false)}
      >
        ×
      </button>

      <div className="auth-icon">✦</div>

      <h2>Welcome back</h2>

      <p>Login to continue to your AI Tax Assistant.</p>

      <input
        type="email"
        placeholder="Email address"
      />

      <input
        type="password"
        placeholder="Password"
      />

      <button className="auth-submit">
        Login
      </button>

      <div className="auth-switch">
        Don't have an account?
        <button
          onClick={() => {
            setShowLogin(false);
            setShowSignup(true);
          }}
        >
          Sign Up
        </button>
      </div>

    </div>
  </div>
)}


{/* SIGNUP MODAL */}

{showSignup && (
  <div
    className="modal-overlay"
    onClick={() => setShowSignup(false)}
  >
    <div
      className="auth-modal"
      onClick={(event) => event.stopPropagation()}
    >

      <button
        className="close-button"
        onClick={() => setShowSignup(false)}
      >
        ×
      </button>

      <div className="auth-icon">✦</div>

      <h2>Create your account</h2>

      <p>Start managing your tax documents with AI.</p>

      <input
        type="text"
        placeholder="Full name"
      />

      <input
        type="email"
        placeholder="Email address"
      />

      <input
        type="password"
        placeholder="Create password"
      />

      <button className="auth-submit">
        Create Account
      </button>

      <div className="auth-switch">
        Already have an account?
        <button
          onClick={() => {
            setShowSignup(false);
            setShowLogin(true);
          }}
        >
          Login
        </button>
      </div>

    </div>
  </div>
)}
}

export default App;