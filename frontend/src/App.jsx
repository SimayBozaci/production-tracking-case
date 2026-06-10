import { useEffect, useState } from "react";

import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box,
  TextField,
} from "@mui/material";

function App() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const [uploads, setUploads] = useState([]);
  const [uploadResult, setUploadResult] = useState(null);
  const [syncResult, setSyncResult] = useState(null);
  const [validationErrors, setValidationErrors] = useState([]);
  const [records, setRecords] = useState([]);
  const [shiftFilter, setShiftFilter] = useState("");
  const [stationFilter, setStationFilter] = useState("");
  const [stockFilter, setStockFilter] = useState("");

  const API_URL = "http://127.0.0.1:8000";

  const loadReport = async () => {
    try {
      const response = await fetch(`${API_URL}/report`);
      const data = await response.json();
      setReport(data);
    } catch (error) {
      console.error(error);
    }
  };

  const loadUploads = async () => {
    try {
      const response = await fetch(`${API_URL}/uploads`);
      const data = await response.json();
      setUploads(data);
    } catch (error) {
      console.error(error);
    }
  };
  const loadValidationErrors = async () => {
  try {

    const response = await fetch(
      `${API_URL}/validation-errors`
    );

    const data = await response.json();

    console.log(
      "VALIDATION ERRORS:",
      data
    );

    setValidationErrors(data);

  } catch (error) {
    console.error(error);
  }
};
const loadRecords = async () => {
  try {
    let url = `${API_URL}/records?`;

    if (shiftFilter) {
      url += `vardiya=${shiftFilter}&`;
    }

    if (stationFilter) {
      url += `is_istasyonu=${stationFilter}&`;
    }

    if (stockFilter) {
      url += `stok_adi=${stockFilter}&`;
    }

    const response = await fetch(url);
    const data = await response.json();

    setRecords(data);

  } catch (error) {
    console.error(error);
  }
};
  useEffect(() => {
    loadReport();
    loadUploads();
    loadValidationErrors();
    loadRecords();
  }, []);

  useEffect(() => {
    loadRecords();
  }, [
    shiftFilter,
    stationFilter,
    stockFilter
  ]);




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
      loadValidationErrors();
      loadRecords();
      
    } catch (error) {
      console.error(error);
      alert("Dosya yüklenemedi");
    }
  };

  const handleSync = async () => {
    try {
      const response = await fetch(`${API_URL}/sync-data`, {
        method: "POST",
      });

      const data = await response.json();

      setSyncResult(data);
    } catch (error) {
      console.error(error);
      alert("Sync işlemi başarısız");
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Production Tracking Dashboard
      </Typography>

      {report && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary">
                  Total Uploads
                </Typography>
                <Typography variant="h4">
                  {report.total_uploads}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary">
                  Total Rows
                </Typography>
                <Typography variant="h4">
                  {report.total_rows}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="success.main">
                  Valid Rows
                </Typography>
                <Typography variant="h4">
                  {report.total_valid_rows}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="error.main">
                  Invalid Rows
                </Typography>
                <Typography variant="h4">
                  {report.total_invalid_rows}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            CSV Upload & Sync
          </Typography>

          <Box
            display="flex"
            gap={2}
            alignItems="center"
            flexWrap="wrap"
          >
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <Button
              variant="contained"
              color="primary"
              onClick={handleUpload}
            >
              Upload CSV
            </Button>

            <Button
              variant="contained"
              color="success"
              onClick={handleSync}
            >
              Sync Valid Records
            </Button>
          </Box>
        </CardContent>
      </Card>

      {uploadResult && (
        <Alert
          severity={
            uploadResult.validation_status === "PASSED"
              ? "success"
              : "error"
          }
          sx={{ mb: 3 }}
        >
          Upload ID: {uploadResult.upload_id}
          {" | "}
          Valid Rows: {uploadResult.valid_rows}
          {" | "}
          Invalid Rows: {uploadResult.invalid_rows}
          {" | "}
          Status: {uploadResult.validation_status}
        </Alert>
      )}

      {syncResult && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Synced Records: {syncResult.sent_records}
          {" | "}
          Files: {syncResult.uploaded_files}
          {" | "}
          Status: {syncResult.status}
        </Alert>
      )}

      {report && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Validation Summary
            </Typography>

            <Typography>
              Validation Passed: {report.validation_passed}
            </Typography>

            <Typography>
              Validation Failed: {report.validation_failed}
            </Typography>
          </CardContent>
        </Card>
      )}

<Card sx={{ mb: 4 }}>
  <CardContent>
    <Typography variant="h6" gutterBottom>
      Production Filters
    </Typography>

    <Box display="flex" gap={2} flexWrap="wrap">
      <TextField
        label="Vardiya"
        value={shiftFilter}
        onChange={(e) => setShiftFilter(e.target.value)}
      />

      <TextField
        label="İş İstasyonu"
        value={stationFilter}
        onChange={(e) => setStationFilter(e.target.value)}
      />

      <TextField
        label="Stok Adı"
        value={stockFilter}
        onChange={(e) => setStockFilter(e.target.value)}
      />
    </Box>
  </CardContent>
</Card>      
<Card sx={{ mb: 4 }}>
  
  <CardContent>
    <Typography variant="h6" gutterBottom>
      Upload History
    </Typography>

    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>File Name</TableCell>
            <TableCell>Rows</TableCell>
            <TableCell>Columns</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Valid Rows</TableCell>
            <TableCell>Invalid Rows</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {uploads.map((upload) => (
            <TableRow key={upload.upload_id}>
              <TableCell>{upload.upload_id}</TableCell>
              <TableCell>{upload.file_name}</TableCell>
              <TableCell>{upload.row_count}</TableCell>
              <TableCell>{upload.column_count}</TableCell>

              <TableCell>
                <Chip
                  label={upload.validation_status}
                  color={
                    upload.validation_status === "PASSED"
                      ? "success"
                      : "error"
                  }
                />
              </TableCell>

              <TableCell>{upload.valid_rows}</TableCell>
              <TableCell>{upload.invalid_rows}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </CardContent>
</Card>
<Card sx={{ mb: 4 }}>
  <CardContent>
    <Typography variant="h6" gutterBottom>
      Production Records
    </Typography>

    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Record ID</TableCell>
            <TableCell>Tarih</TableCell>
            <TableCell>Vardiya</TableCell>
            <TableCell>İş İstasyonu</TableCell>
            <TableCell>Stok Adı</TableCell>
            <TableCell>OEE</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {records.map((record, index) => (
            <TableRow key={index}>
              <TableCell>{record.record_id}</TableCell>
              <TableCell>{record.tarih}</TableCell>
              <TableCell>{record.vardiya}</TableCell>
              <TableCell>{record.is_istasyonu}</TableCell>
              <TableCell>{record.stok_adi}</TableCell>
              <TableCell>{record.oee}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </CardContent>
</Card>
<Card sx={{ mt: 4 }}>
  <CardContent>
    <Typography variant="h6" gutterBottom>
      Validation Errors
    </Typography>

    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Upload ID</TableCell>
            <TableCell>Row Number</TableCell>
            <TableCell>Error Message</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {validationErrors.map((error) => (
            <TableRow key={error.id}>
              <TableCell>{error.id}</TableCell>

              <TableCell>
                {error.upload_id}
              </TableCell>

              <TableCell>
                {error.row_number}
              </TableCell>

              <TableCell>
                <Chip
                  label={error.error_message}
                  color="error"
                  size="small"
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </CardContent>
</Card>
 </Container>
  );
}




export default App;