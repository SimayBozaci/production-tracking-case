import { useEffect, useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const [uploads, setUploads] = useState([]);
  const [uploadResult, setUploadResult] = useState(null);

  const API_URL = "http://127.0.0.1:8000";

  const loadReport = async () => {
    try {
      const response = await fetch(`${API_URL}/report`);
      const data = await response.json();

      console.log("REPORT:", data);

      setReport(data);
    } catch (error) {
      console.error(error);
    }
  };

  const loadUploads = async () => {
    try {
      const response = await fetch(`${API_URL}/uploads`);
      const data = await response.json();

      console.log("UPLOADS:", data);

      setUploads(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadReport();
    loadUploads();
  }, []);

  const handleUpload = async () => {
    if (!file) {
      alert("Lütfen bir CSV dosyası seçin");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/upload-csv`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setUploadResult(data);

      loadReport();
      loadUploads();
    } catch (error) {
      console.error(error);
      alert("Dosya yüklenemedi");
    }
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>Production Tracking Dashboard</h1>

      <hr />

      <h2>CSV Upload</h2>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        style={{
          marginLeft: "10px",
          padding: "8px 16px",
        }}
      >
        Upload
      </button>

      {uploadResult && (
        <div style={{ marginTop: "20px" }}>
          <h3>Upload Result</h3>

          <p>Upload ID: {uploadResult.upload_id}</p>
          <p>Total Rows: {uploadResult.total_rows}</p>
          <p>Valid Rows: {uploadResult.valid_rows}</p>
          <p>Invalid Rows: {uploadResult.invalid_rows}</p>
          <p>Status: {uploadResult.validation_status}</p>
        </div>
      )}

      <hr />
      <h2>Debug</h2>

      <pre>
        {JSON.stringify(report, null, 2)}
      </pre>

      <pre>
        {JSON.stringify(uploads, null, 2)}
      </pre>

      <h2>Report Summary</h2>

      {report && (
        <div>
          <p>Total Uploads: {report.total_uploads}</p>
          <p>Total Rows: {report.total_rows}</p>
          <p>Total Valid Rows: {report.total_valid_rows}</p>
          <p>Total Invalid Rows: {report.total_invalid_rows}</p>
          <p>Validation Passed: {report.validation_passed}</p>
          <p>Validation Failed: {report.validation_failed}</p>
        </div>
      )}

      <hr />

      <h2>Upload History</h2>

      <table
        border="1"
        cellPadding="10"
        style={{
          borderCollapse: "collapse",
          width: "100%",
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>File Name</th>
            <th>Rows</th>
            <th>Columns</th>
            <th>Status</th>
            <th>Valid Rows</th>
            <th>Invalid Rows</th>
          </tr>
        </thead>

        <tbody>
          {uploads.map((upload) => (
            <tr key={upload.upload_id}>
              <td>{upload.upload_id}</td>
              <td>{upload.file_name}</td>
              <td>{upload.row_count}</td>
              <td>{upload.column_count}</td>
              <td>{upload.validation_status}</td>
              <td>{upload.valid_rows}</td>
              <td>{upload.invalid_rows}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;