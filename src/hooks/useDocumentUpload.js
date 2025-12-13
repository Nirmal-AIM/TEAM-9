import { useState } from 'react';
import { uploadDocument, getDocumentStatus } from '../services/api';

/**
 * Custom hook for managing document upload and processing
 * Handles file upload to backend ML model for document analysis
 */
export const useDocumentUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadedDocuments, setUploadedDocuments] = useState([]);
  const [processingStatus, setProcessingStatus] = useState(null);

  const upload = async (file, documentType) => {
    setUploading(true);
    setError(null);
    setProcessingStatus('uploading');

    try {
      // TODO: Uncomment when backend ML model is ready
      // const result = await uploadDocument(file, documentType);
      // setUploadedDocuments(prev => [...prev, result]);
      // setProcessingStatus('processing');
      
      // Placeholder for now
      console.log('Uploading document:', file.name, 'Type:', documentType);
      
      // Simulate upload and processing
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const mockResult = {
        id: Date.now().toString(),
        filename: file.name,
        type: documentType,
        status: 'processed',
        extractedData: {
          // This will be populated by ML model
          fields: [],
        },
      };
      
      setUploadedDocuments(prev => [...prev, mockResult]);
      setProcessingStatus('completed');
      
      return mockResult;
    } catch (err) {
      setError(err.message);
      setProcessingStatus('error');
      throw err;
    } finally {
      setUploading(false);
    }
  };

  const checkStatus = async (documentId) => {
    try {
      // TODO: Uncomment when backend is ready
      // const status = await getDocumentStatus(documentId);
      // setProcessingStatus(status);
      // return status;
      
      // Placeholder
      return { status: 'completed' };
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  return {
    uploading,
    error,
    uploadedDocuments,
    processingStatus,
    upload,
    checkStatus,
  };
};

