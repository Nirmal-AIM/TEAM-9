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
  useEffect(() => {
    const fetchScore = async () => {
      setLoading(true);
      setError(null);
      try {
        // TODO: Uncomment when backend is ready
        // const data = await getCreditScore();
        // setScore(data.score);
        
        // Placeholder for now
        setScore(750);
      } catch (err) {
        setError(err.message);
        // Fallback to placeholder
        setScore(750);
      } finally {
        setLoading(false);
      }
    };

    fetchScore();
  }, []);

  const analyze = async (userData) => {
    setLoading(true);
    setError(null);
    try {
      // TODO: Uncomment when backend ML model is ready
      // const result = await analyzeCreditScore(userData);
      // setScore(result.score);
      // setAnalysis(result.analysis);
      
      // Placeholder for now
      console.log('Analyzing credit score with data:', userData);
      await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate API call
      setAnalysis({
        factors: ['Payment History', 'Credit Utilization', 'Credit History Length'],
        recommendations: ['Pay bills on time', 'Reduce credit card balances'],
      });
    } catch (err) {
      setError(err.message);
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
  };
};

