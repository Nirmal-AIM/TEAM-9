import { useState, useEffect } from 'react';
import { getCreditScore, analyzeCreditScore } from '../services/api';

/**
 * Custom hook for managing credit score data
 * Handles fetching and analyzing credit scores from backend ML model
 */
export const useCreditScore = () => {
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  // Fetch current credit score on mount
  // Function to fetch score for a specific user
  const fetchUserScore = async (userId) => {
    if (!userId) return;

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/api/user/${userId}`);
      if (!response.ok) throw new Error('User not found or backend unavailable');
      const data = await response.json();

      if (data.explanation) {
        setScore(data.explanation.score);
        setAnalysis(data.explanation.analysis);
      } else {
        setScore(null);
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
      setScore(null);
    } finally {
      setLoading(false);
    }
  };

  // Initial load with default if needed, or just leave empty
  useEffect(() => {
    // Optional: fetch a default user or waiting for input
    // fetchUserScore('C03PVPPHOY');
  }, []);

  const analyze = async (userData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/credit-score/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ features: userData })
      });

      if (!response.ok) throw new Error('Analysis failed');

      const result = await response.json();
      setScore(result.score);
      setAnalysis(result.analysis);

      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    score,
    loading,
    error,
    analysis,
    analyze,
    fetchUserScore
  };
};

