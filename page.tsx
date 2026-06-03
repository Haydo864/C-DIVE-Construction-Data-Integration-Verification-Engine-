

'use client';
import { useState } from 'react';

export default function Dashboard() {
  const [invoiceData, setInvoiceData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const testData = "Invoice from BuildPro HVAC. Date: 2024-05-12. Total: $4500. Line 1: Ductwork install (Cost Code 23-100) $4000. Line 2: Filters (Cost Code 23-200) $500.";

  const processInvoice = async () => {
    setLoading(true);
    // In reality, this fetches from your locally running FastAPI backend (http://localhost:8000/api/process-invoice)
    const response = await fetch('http://127.0.0.1:8000/api/process-invoice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_text: testData }),
    });
    const data = await response.json();
    setInvoiceData(data);
    setLoading(false);
  };
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    
    // Create a form data object to send the file securely
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch('http://localhost:8000/api/upload-invoice', {
        method: 'POST',
        // Note: Do NOT set 'Content-Type' manually when sending FormData, the browser does it automatically!
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to process file");
      
      const result = await response.json();
      setInvoiceData(result);    
    } catch (error) {
      console.error(error);
      alert("Error processing the invoice file.");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="min-h-screen bg-gray-50 p-8 text-gray-900">
      <h1 className="text-3xl font-bold mb-6 text-slate-800">C-DIVE Operator Dashboard</h1>
      
      <div className="mt-4 flex gap-4">
  <button
    onClick={processInvoice}
    disabled={loading}
    className="bg-blue-600 text-white px-4 py-2 rounded font-medium hover:bg-blue-700 disabled:opacity-50"
  >
    {loading ? 'Processing...' : 'Process Text'}
  </button>

  {/* NEW UPLOAD BUTTON */}
  <label className="bg-gray-800 text-white px-4 py-2 rounded font-medium hover:bg-gray-700 cursor-pointer disabled:opacity-50">
    {loading ? 'Uploading...' : 'Upload PDF Invoice'}
    <input 
      type="file" 
      accept=".pdf" 
      className="hidden" 
      onChange={handleFileUpload} 
    />
  </label>
</div>

        {/* Right Side: AI Output & Verification Status */}
        <div className="bg-white p-6 shadow rounded-lg border border-gray-200">
          <h2 className="text-xl font-semibold mb-4 border-b pb-2">Verified Output</h2>
          
          {invoiceData ? (
            <div>
              <div className={`p-4 rounded mb-6 font-bold ${invoiceData.status === 'Green' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                Status: {invoiceData.status}
                {invoiceData.flags.map((flag: string, i: number) => (
                  <p key={i} className="text-sm font-normal mt-1">{flag}</p>
                ))}
              </div>

              <div className="space-y-2 text-sm">
                <p><strong>Vendor:</strong> {invoiceData.data.vendor_name}</p>
                <p><strong>Date:</strong> {invoiceData.data.invoice_date}</p>
                <p><strong>Total Billed:</strong> ${invoiceData.data.total_amount}</p>
                
                <h3 className="font-semibold mt-4 mb-2">Line Items:</h3>
                <ul className="space-y-2">
                  {invoiceData.data.line_items.map((item: any, i: number) => (
                    <li key={i} className="bg-gray-100 p-2 rounded flex justify-between border border-gray-200">
                      <span>[{item.cost_code}] {item.description}</span>
                      <span className="font-mono">${item.amount}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <div className="text-gray-400 italic">Awaiting document processing...</div>
          )}
        </div>
      </div>
    
        );
}