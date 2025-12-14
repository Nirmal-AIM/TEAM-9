import React, { useState } from 'react';
import { useCreditScore } from '../hooks/useCreditScore';

const CreditScoreCard = () => {
  const { score, loading, error, analysis, fetchUserScore } = useCreditScore();
  const [userId, setUserId] = useState('');

  const handleCheckScore = () => {
    if (userId) {
      fetchUserScore(userId);
    }
  };

  const getScoreColor = (score) => {
    if (!score) return 'from-gray-400 via-gray-500 to-gray-600';
    if (score >= 750) return 'from-green-500 via-green-600 to-green-700';
    if (score >= 650) return 'from-yellow-500 via-yellow-600 to-yellow-700';
    return 'from-red-500 via-red-600 to-red-700';
  };

  return (
    <div className="group relative bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 border border-gray-100 overflow-hidden">
      {/* Decorative gradient overlay */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full -mr-16 -mt-16 opacity-50 group-hover:opacity-70 transition-opacity"></div>
      <div className="relative text-center">
        {/* Header with icon */}
        <div className="flex items-center justify-center mb-6">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg mr-3">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-800">Credit Score</h2>
        </div>

        {/* Input Section */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Enter User ID (e.g. C03PVPPHOY)"
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none mb-2 text-center uppercase"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
        </div>

        {/* Score Display with gradient */}
        <div className="mb-8 min-h-[160px]">
          {loading ? (
            <div className="animate-pulse flex flex-col items-center">
              <div className="h-20 w-32 bg-gray-200 rounded mb-4"></div>
              <div className="h-4 w-24 bg-gray-200 rounded"></div>
            </div>
          ) : error ? (
            <div className="text-red-500 bg-red-50 p-3 rounded-lg text-sm">
              {error}
            </div>
          ) : score ? (
            <>
              <div className="relative inline-block">
                <div className={`text-7xl font-bold bg-gradient-to-r ${getScoreColor(score)} bg-clip-text text-transparent mb-2`}>
                  {score}
                </div>
              </div>
              <div className="text-sm font-medium text-gray-500 mt-2">Current Score</div>

              {/* Analysis Section */}
              {analysis && (
                <div className="mt-6 text-left bg-gray-50 p-4 rounded-xl">
                  <h4 className="font-semibold text-gray-700 text-sm mb-2">Why this score?</h4>
                  <p className="text-xs text-gray-600 mb-3">{analysis.explanation}</p>

                  <h4 className="font-semibold text-gray-700 text-sm mb-2">How to improve:</h4>
                  <ul className="text-xs text-green-600 space-y-1">
                    {analysis.recommendations.map((rec, idx) => (
                      <li key={idx} className="flex items-start">
                        <svg className="w-3 h-3 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          ) : (
            <div className="text-gray-400 text-sm py-8">
              Enter a User ID and click below to analyze
            </div>
          )}
        </div>

        {/* Action Button */}
        <button
          onClick={handleCheckScore}
          disabled={loading || !userId}
          className={`w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold py-3.5 px-6 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
        >
          <span className="flex items-center justify-center">
            {loading ? (
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            )}
            {loading ? 'Analyzing...' : 'Analyze Score'}
          </span>
        </button>
      </div>
    </div>
  );
};

export default CreditScoreCard;

