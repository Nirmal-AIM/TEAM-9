import React from 'react';

const Navbar = () => {
  return (
    <nav className="sticky top-0 z-50 w-full bg-white/95 backdrop-blur-sm shadow-lg border-b border-gray-100">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Left: Logo/Title */}
          <div className="flex-shrink-0 flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center shadow-md">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
                WebFlow AI
              </h1>
              <p className="text-xs text-gray-500 hidden sm:block">Financial Intelligence</p>
            </div>
          </div>

          {/* Center: Title Banner */}
          <div className="hidden lg:flex flex-1 justify-center">
            <div className="px-4 py-2 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-full border border-blue-100">
              <h2 className="text-sm font-semibold text-gray-700">
                Smart Credit Score Analysis & Verification
              </h2>
            </div>
          </div>

          {/* Right: Menu Items */}
          <div className="flex items-center space-x-1">
            <a href="#profile" className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200">
              Profile
            </a>
            <a href="#analysis" className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200">
              Analysis
            </a>
            <a href="#contact" className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200">
              Contact Us
            </a>
          </div>
        </div>

        {/* Mobile: Center Title Banner */}
        <div className="lg:hidden mt-3 text-center">
          <div className="inline-block px-4 py-2 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-full border border-blue-100">
            <h2 className="text-xs font-semibold text-gray-700">
              Smart Credit Score Analysis & Verification
            </h2>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

