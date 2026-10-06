import { useState } from "react";
import "./App.css";

const documentConfig = [
  {
    key: "pan",
    title: "PAN Card",
    subtitle: "Identity document",
    icon: "▣",
    single: true,
  },
  {
    key: "aadhaar",
    title: "Aadhaar",
    subtitle: "Front & back",
    icon: "◎",
  },
  {
    key: "salary",
    title: "Salary Slips",
    subtitle: "Monthly income",
    icon: "₹",
  },
  {
    key: "bank",
    title: "Bank Statement",
    subtitle: "Financial records",
    icon: "▤",
  },
  {
    key: "form16",
    title: "Form 16",
    subtitle: "Tax certificate",
    icon: "▥",
  },
];

function App() {
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [activeTab, setActiveTab] = useState("home");
  const [processing, setProcessing] = useState(false);

  const [files, setFiles] = useState({
    pan: null,
    aadhaar: [],
    salary: [],
    bank: [],
    form16: [],
  });

  const handleFileChange = (type, event) => {
    const selectedFiles = Array.from(event.target.files || []);

    if (selectedFiles.length === 0) return;

    if (type === "pan") {
      setFiles((previous) => ({
        ...previous,
        pan: selectedFiles[0],
      }));

      return;
    }

    setFiles((previous) => ({
      ...previous,
      [type]: [
        ...(Array.isArray(previous[type]) ? previous[type] : []),
        ...selectedFiles,
      ],
    }));

    event.target.value = "";
  };

  const getFileCount = (type) => {
    if (type === "pan") {
      return files.pan ? 1 : 0;
    }

    return files[type]?.length || 0;
  };

  const scrollTo = (id) => {
    setActiveTab(id === "upload" ? "upload" : "home");

    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  const processDocuments = async () => {
    console.log("PROCESS BUTTON CLICKED");
    console.log("Current files:", files);

    const formData = new FormData();

    if (files.pan) {
      formData.append("pan", files.pan);
    }

    files.aadhaar.forEach((file) => {
      formData.append("aadhaar", file);
    });

    files.salary.forEach((file) => {
      formData.append("salary", file);
    });

    files.bank.forEach((file) => {
      formData.append("bank", file);
    });

    files.form16.forEach((file) => {
      formData.append("form16", file);
    });

    try {
      setProcessing(true);

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

    } finally {
      setProcessing(false);
    }
  };

  const hasDocuments =
    !!files.pan ||
    files.aadhaar.length > 0 ||
    files.salary.length > 0 ||
    files.bank.length > 0 ||
    files.form16.length > 0;

  const totalFiles =
    Object.values(files).reduce(
      (total, value) =>
        total +
        (Array.isArray(value)
          ? value.length
          : value
          ? 1
          : 0),
      0
    );

  return (
    <div className="app">

      {/* TOP BAR */}

      <header className="topbar">

        <button
          className="brand"
          onClick={() => scrollTo("home")}
        >
          <span className="brand-mark">
            ✦
          </span>

          <span>
            TAX<span>AI</span>
          </span>
        </button>

        <div className="top-actions">

          <button
            className="icon-button"
            aria-label="Notifications"
            onClick={() =>
              alert("Notifications coming soon")
            }
          >
            ♧
          </button>

          <button
            className="avatar-button"
            onClick={() => setShowLogin(true)}
          >
            P
          </button>

        </div>

      </header>


      {/* DESKTOP NAV */}

      <nav className="desktop-nav">

        <button
          className={
            activeTab === "home"
              ? "active"
              : ""
          }
          onClick={() => scrollTo("home")}
        >
          Overview
        </button>

        <button
          onClick={() =>
            scrollTo("how-it-works")
          }
        >
          How it works
        </button>

        <button
          className={
            activeTab === "upload"
              ? "active"
              : ""
          }
          onClick={() => scrollTo("upload")}
        >
          Documents
        </button>

        <button
          onClick={() =>
            setShowLogin(true)
          }
        >
          Account
        </button>

      </nav>


      <main>

        {/* HERO */}

        <section
          className="hero-section"
          id="home"
        >

          <div className="hero-copy">

            <span className="eyebrow">

              <span className="status-dot" />

              AI TAX ASSISTANT

            </span>

            <h1>
              Your taxes,
              <br />
              <span>made simpler.</span>
            </h1>

            <p>
              Upload your documents. TAXAI
              extracts, validates and organizes
              the information for you.
            </p>

            <div className="hero-actions">

              <button
                className="primary-button"
                onClick={() =>
                  scrollTo("upload")
                }
              >
                Start tax analysis

                <span>→</span>

              </button>

              <button
                className="text-button"
                onClick={() =>
                  scrollTo("how-it-works")
                }
              >
                See how it works
              </button>

            </div>

          </div>


          {/* TAX WORKSPACE */}

          <div className="tax-card">

            <div className="tax-card-top">

              <div>

                <span className="mini-label">
                  TAXAI
                </span>

                <h3>
                  Tax workspace
                </h3>

              </div>

              <div className="secure-badge">
                Secure
              </div>

            </div>


            <div className="progress-ring">

              <div className="ring-inner">

                <strong>
                  {hasDocuments
                    ? "Ready"
                    : "0%"}
                </strong>

                <span>
                  {hasDocuments
                    ? "Documents added"
                    : "Start here"}
                </span>

              </div>

            </div>


            <div className="tax-card-footer">

              <span>
                Document AI
              </span>

              <span>•</span>

              <span>
                Validation
              </span>

              <span>•</span>

              <span>
                CA Review
              </span>

            </div>

          </div>

        </section>


        {/* STATS */}

        <section className="stats-row">

          <div className="stat-card">

            <span className="stat-icon">
              ⌁
            </span>

            <div>

              <strong>
                5
              </strong>

              <span>
                Document types
              </span>

            </div>

          </div>


          <div className="stat-card">

            <span className="stat-icon">
              ✓
            </span>

            <div>

              <strong>
                AI
              </strong>

              <span>
                Data validation
              </span>

            </div>

          </div>


          <div className="stat-card">

            <span className="stat-icon">
              ◌
            </span>

            <div>

              <strong>
                CA
              </strong>

              <span>
                Human review
              </span>

            </div>

          </div>

        </section>


        {/* HOW IT WORKS */}

        <section
          className="content-section"
          id="how-it-works"
        >

          <div className="section-header">

            <div>

              <span className="section-kicker">
                HOW IT WORKS
              </span>

              <h2>
                From documents to
                tax-ready data.
              </h2>

            </div>

            <span className="section-count">
              01—04
            </span>

          </div>


          <div className="workflow-list">

            <div className="workflow-item">

              <span className="workflow-number">
                01
              </span>

              <div>

                <h3>
                  Upload
                </h3>

                <p>
                  PAN, Aadhaar, salary slips,
                  bank statements and Form 16.
                </p>

              </div>

              <span className="workflow-arrow">
                →
              </span>

            </div>


            <div className="workflow-item">

              <span className="workflow-number">
                02
              </span>

              <div>

                <h3>
                  AI reads
                </h3>

                <p>
                  OCR and AI extraction turn
                  documents into structured data.
                </p>

              </div>

              <span className="workflow-arrow">
                →
              </span>

            </div>


            <div className="workflow-item">

              <span className="workflow-number">
                03
              </span>

              <div>

                <h3>
                  Validate
                </h3>

                <p>
                  The agent checks missing fields
                  and inconsistencies.
                </p>

              </div>

              <span className="workflow-arrow">
                →
              </span>

            </div>


            <div className="workflow-item">

              <span className="workflow-number">
                04
              </span>

              <div>

                <h3>
                  Review
                </h3>

                <p>
                  Cases can move to a CA for
                  final review and approval.
                </p>

              </div>

              <span className="workflow-arrow">
                ✓
              </span>

            </div>

          </div>

        </section>


        {/* DOCUMENT CENTER */}

        <section
          className="content-section document-section"
          id="upload"
        >

          <div className="section-header">

            <div>

              <span className="section-kicker">
                DOCUMENT CENTER
              </span>

              <h2>
                Prepare your tax workspace.
              </h2>

            </div>

            <div className="document-summary">

              <strong>
                {totalFiles}
              </strong>

              <span>
                files added
              </span>

            </div>

          </div>


          <div className="document-grid">

            {documentConfig.map(
              (document) => {

                const count =
                  getFileCount(
                    document.key
                  );

                const currentFiles =
                  document.key === "pan"
                    ? files.pan
                      ? [files.pan]
                      : []
                    : files[
                        document.key
                      ];

                return (

                  <article
                    className={`document-card ${
                      count
                        ? "has-files"
                        : ""
                    }`}
                    key={document.key}
                  >

                    <div className="document-card-top">

                      <div className="document-icon">
                        {document.icon}
                      </div>

                      {count > 0 && (

                        <span className="added-badge">
                          ✓ {count}
                        </span>

                      )}

                    </div>


                    <h3>
                      {document.title}
                    </h3>

                    <p>
                      {document.subtitle}
                    </p>


                    <label className="choose-button">

                      {count
                        ? document.single
                          ? "Change file"
                          : "Add more"
                        : document.single
                        ? "Choose file"
                        : "Choose files"}

                      <input
                        type="file"
                        multiple={
                          !document.single
                        }
                        accept=".jpg,.jpeg,.png,.pdf"
                        onChange={(event) =>
                          handleFileChange(
                            document.key,
                            event
                          )
                        }
                      />

                    </label>


                    {currentFiles?.length >
                      0 && (

                      <div className="selected-files">

                        {currentFiles.map(
                          (
                            file,
                            index
                          ) => (

                            <div
                              className="selected-file"
                              key={`${file.name}-${index}`}
                            >

                              <span>
                                ✓
                              </span>

                              <span
                                title={
                                  file.name
                                }
                              >
                                {file.name}
                              </span>

                            </div>

                          )
                        )}

                      </div>

                    )}


                    <small>
                      JPG, PNG or PDF
                    </small>

                  </article>

                );
              }
            )}

          </div>


          {/* PRIVACY */}

          <div className="privacy-card">

            <div className="privacy-icon">
              ⌾
            </div>

            <div>

              <strong>
                Privacy first
              </strong>

              <p>
                Use sample documents and masked
                Aadhaar data during development.
                Never upload real sensitive
                documents to this demo.
              </p>

            </div>

          </div>


          {/* PROCESS */}

          <button
            className="process-button"
            disabled={
              !hasDocuments ||
              processing
            }
            onClick={
              processDocuments
            }
          >

            <span>
              {processing
                ? "Processing documents..."
                : "Process documents"}
            </span>

            <span>
              {processing
                ? "…"
                : "→"}
            </span>

          </button>

        </section>

      </main>


      {/* FOOTER */}

      <footer className="footer">

        <div>

          <div className="footer-brand">

            <span className="brand-mark">
              ✦
            </span>

            TAX<span>AI</span>

          </div>

          <p>
            Intelligent document processing
            for tax workflows.
          </p>

        </div>

        <span>
          © 2026 TAXAI · Demo Project
        </span>

      </footer>


      {/* MOBILE NAVIGATION */}

      <nav className="mobile-tabbar">

        <button
          className={
            activeTab === "home"
              ? "active"
              : ""
          }
          onClick={() =>
            scrollTo("home")
          }
        >

          <span>⌂</span>

          Home

        </button>


        <button
          className={
            activeTab === "upload"
              ? "active"
              : ""
          }
          onClick={() =>
            scrollTo("upload")
          }
        >

          <span>＋</span>

          Documents

        </button>


        <button
          onClick={() =>
            setShowLogin(true)
          }
        >

          <span>○</span>

          Account

        </button>

      </nav>


      {/* LOGIN */}

      {showLogin && (

        <div
          className="modal-overlay"
          onClick={() =>
            setShowLogin(false)
          }
        >

          <div
            className="auth-sheet"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            <button
              className="modal-close"
              onClick={() =>
                setShowLogin(false)
              }
            >
              ×
            </button>


            <div className="auth-mark">
              ✦
            </div>

            <span className="section-kicker">
              TAXAI ACCOUNT
            </span>

            <h2>
              Welcome back.
            </h2>

            <p>
              Continue to your AI tax workspace.
            </p>


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

              New to TAXAI?

              <button
                onClick={() => {
                  setShowLogin(false);
                  setShowSignup(true);
                }}
              >
                Create account
              </button>

            </div>

          </div>

        </div>

      )}


      {/* SIGNUP */}

      {showSignup && (

        <div
          className="modal-overlay"
          onClick={() =>
            setShowSignup(false)
          }
        >

          <div
            className="auth-sheet"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            <button
              className="modal-close"
              onClick={() =>
                setShowSignup(false)
              }
            >
              ×
            </button>


            <div className="auth-mark">
              ✦
            </div>

            <span className="section-kicker">
              GET STARTED
            </span>

            <h2>
              Create your account.
            </h2>

            <p>
              Start managing your tax
              documents with AI.
            </p>


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
              Create account
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

    </div>
  );
}

export default App;