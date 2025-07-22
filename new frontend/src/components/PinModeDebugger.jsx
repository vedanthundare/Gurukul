import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useLocation } from 'react-router-dom';
import {
  selectSelectedAvatar,
  selectFavorites,
  selectIsPinModeEnabled,
  selectPinnedAvatarPosition,
  selectPinPosition,
  selectPinRotation,
  selectPinScale,
  selectActiveSettingsTab,
  selectActiveMainTab,
} from '../store/avatarSlice';
import { selectIsAuthenticated } from '../store/authSlice';
import {
  checkFallbackAvatarFile,
  test3DModelLoading
} from '../utils/pinModeTestUtils';

/**
 * Debug component to help troubleshoot pin mode issues
 * Only shows in development mode
 */
export default function PinModeDebugger() {
  const location = useLocation();

  // Redux state
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const selectedAvatar = useSelector(selectSelectedAvatar);
  const favorites = useSelector(selectFavorites);
  const isPinModeEnabled = useSelector(selectIsPinModeEnabled);
  const pinnedAvatarPosition = useSelector(selectPinnedAvatarPosition);
  const pinPosition = useSelector(selectPinPosition);
  const pinRotation = useSelector(selectPinRotation);
  const pinScale = useSelector(selectPinScale);
  const activeSettingsTab = useSelector(selectActiveSettingsTab);
  const activeMainTab = useSelector(selectActiveMainTab);

  // Test results state
  const [testResults, setTestResults] = useState({
    fileAccessible: null,
    modelLoading: null,
    testing: false
  });

  // Auto-run tests when pin mode is enabled
  useEffect(() => {
    if (isPinModeEnabled && !testResults.testing) {
      runDiagnosticTests();
    }
  }, [isPinModeEnabled]);

  const runDiagnosticTests = async () => {
    console.log("🧪 Running automatic diagnostic tests...");
    setTestResults(prev => ({ ...prev, testing: true }));

    try {
      // Test 1: File accessibility
      const fileResult = await checkFallbackAvatarFile();
      setTestResults(prev => ({ ...prev, fileAccessible: fileResult }));

      // Test 2: 3D model loading
      const modelResult = await test3DModelLoading();
      setTestResults(prev => ({ ...prev, modelLoading: modelResult }));

      console.log("🧪 Diagnostic tests completed:", { fileResult, modelResult });
    } catch (error) {
      console.error("🧪 Diagnostic tests failed:", error);
      setTestResults(prev => ({
        ...prev,
        fileAccessible: false,
        modelLoading: false
      }));
    } finally {
      setTestResults(prev => ({ ...prev, testing: false }));
    }
  };

  // Only show in development
  if (!import.meta.env.DEV) {
    return null;
  }

  // Calculate visibility conditions
  const isOnAvatarSelectionPage = location.pathname === "/avatar-selection";
  const isOnAvatarSelectionPinTab = isOnAvatarSelectionPage && activeMainTab === "favorites" && activeSettingsTab === "pin";
  
  const shouldShowPinnedAvatar = isAuthenticated && isPinModeEnabled && !isOnAvatarSelectionPinTab;
  const shouldShowContainedAvatar = isAuthenticated && isPinModeEnabled && isOnAvatarSelectionPinTab;

  return (
    <div className="fixed bottom-4 left-4 bg-black/80 text-white p-4 rounded-lg text-xs max-w-sm z-[10000] border border-orange-500/50">
      <h3 className="text-orange-400 font-bold mb-2">🎭 Pin Mode Debug</h3>
      
      <div className="space-y-1">
        <div className="text-green-400">
          ✓ Auth: {isAuthenticated ? "YES" : "NO"}
        </div>
        <div className={isPinModeEnabled ? "text-green-400" : "text-red-400"}>
          {isPinModeEnabled ? "✓" : "✗"} Pin Mode: {isPinModeEnabled ? "ENABLED" : "DISABLED"}
        </div>
        <div className={selectedAvatar ? "text-green-400" : "text-yellow-400"}>
          {selectedAvatar ? "✓" : "⚠"} Avatar: {selectedAvatar?.name || "NONE"}
        </div>
        <div className="text-blue-400">
          📍 Favorites: {favorites.length}
        </div>
        
        <div className="border-t border-white/20 pt-2 mt-2">
          <div className="text-purple-400">Location: {location.pathname}</div>
          <div className="text-purple-400">Main Tab: {activeMainTab}</div>
          <div className="text-purple-400">Settings Tab: {activeSettingsTab}</div>
        </div>
        
        <div className="border-t border-white/20 pt-2 mt-2">
          <div className={shouldShowPinnedAvatar ? "text-green-400" : "text-red-400"}>
            {shouldShowPinnedAvatar ? "✓" : "✗"} Should Show Floating
          </div>
          <div className={shouldShowContainedAvatar ? "text-green-400" : "text-red-400"}>
            {shouldShowContainedAvatar ? "✓" : "✗"} Should Show Contained
          </div>
        </div>
        
        {isPinModeEnabled && (
          <div className="border-t border-white/20 pt-2 mt-2">
            <div className="text-cyan-400">Screen: ({pinnedAvatarPosition.x}, {pinnedAvatarPosition.y})</div>
            <div className="text-cyan-400">3D Pos: ({pinPosition.x.toFixed(1)}, {pinPosition.y.toFixed(1)}, {pinPosition.z.toFixed(1)})</div>
            <div className="text-cyan-400">3D Rot: ({pinRotation.x}°, {pinRotation.y}°, {pinRotation.z}°)</div>
            <div className="text-cyan-400">Scale: {pinScale.toFixed(1)}</div>
          </div>
        )}

        {/* Diagnostic Tests Section */}
        <div className="border-t border-white/20 pt-2 mt-2">
          <div className="text-pink-400 font-bold mb-1">🧪 Diagnostics</div>

          {testResults.testing && (
            <div className="text-yellow-400">⏳ Running tests...</div>
          )}

          {!testResults.testing && (
            <>
              <div className={testResults.fileAccessible === true ? "text-green-400" : testResults.fileAccessible === false ? "text-red-400" : "text-gray-400"}>
                {testResults.fileAccessible === true ? "✅" : testResults.fileAccessible === false ? "❌" : "⏳"} File Access
              </div>
              <div className={testResults.modelLoading === true ? "text-green-400" : testResults.modelLoading === false ? "text-red-400" : "text-gray-400"}>
                {testResults.modelLoading === true ? "✅" : testResults.modelLoading === false ? "❌" : "⏳"} 3D Loading
              </div>

              {(testResults.fileAccessible === false || testResults.modelLoading === false) && (
                <button
                  onClick={runDiagnosticTests}
                  className="mt-1 px-2 py-1 bg-orange-500 text-white text-xs rounded hover:bg-orange-600"
                >
                  Retry Tests
                </button>
              )}
            </>
          )}
        </div>

        {/* Quick Actions Section */}
        <div className="border-t border-white/20 pt-2 mt-2">
          <div className="text-green-400 font-bold mb-1">⚡ Quick Actions</div>

          {!isPinModeEnabled && (
            <button
              onClick={() => {
                if (window.pinModeTestUtils) {
                  window.pinModeTestUtils.forceEnablePinMode(window.__REDUX_STORE__.dispatch);
                }
              }}
              className="w-full mb-1 px-2 py-1 bg-green-600 text-white text-xs rounded hover:bg-green-700"
            >
              🚀 Enable Pin Mode
            </button>
          )}

          <button
            onClick={runDiagnosticTests}
            className="w-full px-2 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
          >
            🧪 Run Tests
          </button>
        </div>
      </div>
    </div>
  );
}
