import { createSlice, createSelector } from "@reduxjs/toolkit";
import { storage } from "../utils/storageUtils";

const initialState = {
  // Favorites state
  favorites: [],
  selectedAvatar: null,

  // Pin Mode Settings (for floating pinned avatar)
  pinPosition: { x: 0, y: -3.3, z: 0 }, // Better default position for fallback.glb
  pinRotation: { x: 0, y: 180, z: 0 }, // Face forward by default
  pinScale: 2.5, // Increased default scale for better visibility in floating mode

  // Pin Avatar feature state
  isPinModeEnabled: true, // Default to pin mode enabled
  pinnedAvatarPosition: { x: 100, y: 100 },
  isDragging: false,
  dragOffset: { x: 0, y: 0 },

  // Avatar Settings Tab state (only pin mode now)
  activeSettingsTab: "pin",

  // Main page tab state (for avatar-selection page)
  activeMainTab: "favorites", // 'custom-models' or 'favorites'

  // Custom Models state
  customModels: [], // Array of uploaded .glb models with metadata
  customModelsLoading: false,
  customModelsError: null,

  // Avatar Chat feature state
  isChatOpen: false,
  chatHistory: [],
  chatContext: null,
  isTyping: false,

  // Loading state
  isLoading: false,
  error: null,
};

export const avatarSlice = createSlice({
  name: "avatar",
  initialState,
  reducers: {
    // Favorites management
    setFavorites: (state, action) => {
      state.favorites = action.payload;
    },
    addFavorite: (state, action) => {
      // Ensure favorites is an array
      if (!Array.isArray(state.favorites)) {
        state.favorites = [];
      }
      state.favorites.push(action.payload);
    },
    removeFavorite: (state, action) => {
      // Ensure favorites is an array
      if (!Array.isArray(state.favorites)) {
        state.favorites = [];
        return;
      }
      state.favorites = state.favorites.filter(
        (fav) => fav.id !== action.payload
      );
    },
    updateFavorite: (state, action) => {
      // Ensure favorites is an array
      if (!Array.isArray(state.favorites)) {
        state.favorites = [];
        return;
      }
      const { id, updates } = action.payload;
      const index = state.favorites.findIndex((fav) => fav.id === id);
      if (index !== -1) {
        state.favorites[index] = { ...state.favorites[index], ...updates };
      }
    },

    // Selected avatar
    setSelectedAvatar: (state, action) => {
      state.selectedAvatar = action.payload;
    },

    // Grid settings removed - only pin mode now

    // Pin settings
    setPinPosition: (state, action) => {
      state.pinPosition = action.payload;
    },
    setPinRotation: (state, action) => {
      state.pinRotation = action.payload;
    },
    setPinScale: (state, action) => {
      state.pinScale = action.payload;
    },

    // Pin mode state
    setIsPinModeEnabled: (state, action) => {
      const newPinModeState = action.payload;
      console.log("🎭 Redux: Setting pin mode enabled:", { from: state.isPinModeEnabled, to: newPinModeState });
      state.isPinModeEnabled = newPinModeState;

      // If enabling pin mode and no avatar is selected, create a fallback
      if (newPinModeState && !state.selectedAvatar) {
        console.log("🎭 Redux: Creating fallback avatar for pin mode");
        const fallbackAvatar = {
          id: "fallback-avatar-" + Date.now(),
          name: "Guru1",
          isDefault: true,
          previewUrl: "/avatar/fallback.glb",
          timestamp: new Date().toISOString(),
          gridPosition: { x: 0, y: 0, z: 0 },
          gridRotation: { x: 0, y: 180, z: 0 },
          gridScale: 1,
          pinPosition: { x: 0, y: -3.3, z: 0 },
          pinRotation: { x: 0, y: 180, z: 0 },
          pinScale: 2.5,
          isPinModeEnabled: true,
          pinnedAvatarPosition: state.pinnedAvatarPosition || { x: 100, y: 100 }
        };
        state.selectedAvatar = fallbackAvatar;

        // Add to favorites if not already there
        if (!state.favorites.some(fav => fav.isDefault)) {
          state.favorites.unshift(fallbackAvatar);
        }
      }
    },
    setPinnedAvatarPosition: (state, action) => {
      state.pinnedAvatarPosition = action.payload;
    },
    setIsDragging: (state, action) => {
      state.isDragging = action.payload;
    },
    setDragOffset: (state, action) => {
      state.dragOffset = action.payload;
    },

    // Settings tab
    setActiveSettingsTab: (state, action) => {
      state.activeSettingsTab = action.payload;
    },

    // Main tab
    setActiveMainTab: (state, action) => {
      state.activeMainTab = action.payload;
    },

    // Custom Models actions
    setCustomModelsLoading: (state, action) => {
      state.customModelsLoading = action.payload;
    },
    setCustomModelsError: (state, action) => {
      state.customModelsError = action.payload;
    },
    addCustomModel: (state, action) => {
      state.customModels.push(action.payload);
      // Note: IndexedDB storage is handled in the component, not here
      // This keeps the Redux store synchronous and avoids async actions
    },
    removeCustomModel: (state, action) => {
      state.customModels = state.customModels.filter(
        (model) => model.id !== action.payload
      );
      // Note: IndexedDB storage is handled in the component, not here
      // This keeps the Redux store synchronous and avoids async actions
    },
    loadCustomModels: (state, action) => {
      state.customModels = action.payload;
    },

    // Reset functions
    resetPinSettings: (state) => {
      state.isPinModeEnabled = true; // Default to enabled
      state.pinnedAvatarPosition = { x: 100, y: 100 };
      state.pinPosition = { x: 0, y: -4.0, z: 0 }; // Better default position
      state.pinRotation = { x: 0, y: 180, z: 0 }; // Face forward by default
      state.pinScale = 2.5; // Better default for pin mode
    },

    // Load avatar settings
    loadAvatarSettings: (state, action) => {
      const avatar = action.payload;
      if (!avatar) return;

      // Load pin settings (with fallback to legacy settings)
      // Avatar-specific position defaults
      let defaultPosition = { x: 0, y: -3.3, z: 0 }; // Default for fallback.glb
      if (avatar.previewUrl && avatar.previewUrl.includes('jupiter.glb')) {
        defaultPosition = { x: 0, y: 0.5, z: -4.0 }; // Perfect hardcoded position for jupiter.glb
      }

      state.pinPosition = avatar.pinPosition || avatar.avatarPosition || defaultPosition;
      state.pinRotation = avatar.pinRotation ||
        avatar.avatarRotation || { x: 0, y: 180, z: 0 }; // Face forward by default

      // Avatar-specific scale defaults
      let defaultScale = 2.5; // Default for fallback.glb
      if (avatar.previewUrl && avatar.previewUrl.includes('jupiter.glb')) {
        defaultScale = 0.6; // Decreased by 0.3 (was 0.9, now 0.6)
      }

      state.pinScale = avatar.pinScale || avatar.avatarScale || defaultScale;

      state.isPinModeEnabled = avatar.isPinModeEnabled !== undefined ? avatar.isPinModeEnabled : true; // Default to enabled
      state.pinnedAvatarPosition = avatar.pinnedAvatarPosition || {
        x: 100,
        y: 100,
      };
    },

    // Auto-save current settings to selected avatar with storage optimization
    autoSaveAvatarSettings: (state) => {
      if (!state.selectedAvatar) return;

      try {
        const updatedAvatar = {
          ...state.selectedAvatar,
          // Save pin settings
          pinPosition: state.pinPosition,
          pinRotation: state.pinRotation,
          pinScale: state.pinScale,
          // Legacy support - use pin settings as default
          avatarPosition: state.pinPosition,
          avatarRotation: state.pinRotation,
          avatarScale: state.pinScale,
          isPinModeEnabled: state.isPinModeEnabled,
          pinnedAvatarPosition: state.pinnedAvatarPosition,
          lastUpdated: new Date().toISOString(),
        };

        // Remove large data that shouldn't be in Redux persist
        delete updatedAvatar.fileData;
        if (
          updatedAvatar.previewUrl &&
          updatedAvatar.previewUrl.startsWith("blob:")
        ) {
          delete updatedAvatar.previewUrl; // Remove blob URLs to save space
        }

        // Ensure favorites is an array before updating
        if (!Array.isArray(state.favorites)) {
          console.warn(
            "🚨 Favorites is not an array in autoSaveAvatarSettings, resetting to empty array"
          );
          state.favorites = [];
        }

        // Update the favorites array
        const index = state.favorites.findIndex(
          (fav) => fav.id === state.selectedAvatar.id
        );
        if (index !== -1) {
          state.favorites[index] = updatedAvatar;
        }

        state.selectedAvatar = updatedAvatar;

        // Limit favorites to prevent storage overflow
        if (state.favorites.length > 10) {
          console.warn("🚨 Too many favorites, removing oldest ones");
          state.favorites = state.favorites
            .sort(
              (a, b) =>
                new Date(b.lastUpdated || b.timestamp || 0) -
                new Date(a.lastUpdated || a.timestamp || 0)
            )
            .slice(0, 10);
        }
      } catch (error) {
        console.error("Error in autoSaveAvatarSettings:", error);
        // Don't throw to prevent app crash
      }
    },

    // Loading and error states
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },

    // Global state persistence
    loadGlobalState: (state, action) => {
      const globalState = action.payload;
      if (!globalState) return;

      // Load global avatar state
      state.isPinModeEnabled = globalState.isPinModeEnabled !== undefined ? globalState.isPinModeEnabled : true; // Default to true
      state.pinnedAvatarPosition = globalState.pinnedAvatarPosition || {
        x: 100,
        y: 100,
      };
      state.activeSettingsTab = globalState.activeSettingsTab || "pin"; // Default to pin
      state.activeMainTab = globalState.activeMainTab || "custom-models";
      state.pinPosition = globalState.pinPosition || { x: 0, y: -4.0, z: 0 }; // Better default for fallback.glb
      state.pinRotation = globalState.pinRotation || { x: 0, y: 180, z: 0 }; // Face forward by default
      state.pinScale = globalState.pinScale || 2.5; // Better default for pin mode

      // Load chat state
      state.isChatOpen = globalState.isChatOpen || false;
      state.chatHistory = globalState.chatHistory || [];
    },

    saveGlobalState: (state) => {
      // Save current global state to localStorage
      storage.saveAvatarGlobalState(state);
    },

    // Avatar Chat actions
    setIsChatOpen: (state, action) => {
      state.isChatOpen = action.payload;
    },

    addChatMessage: (state, action) => {
      state.chatHistory.push(action.payload);
    },

    setChatHistory: (state, action) => {
      state.chatHistory = action.payload;
    },

    setChatContext: (state, action) => {
      state.chatContext = action.payload;
    },

    setIsTyping: (state, action) => {
      state.isTyping = action.payload;
    },

    clearChatHistory: (state) => {
      state.chatHistory = [];
    },
  },
});

// Export actions
export const {
  setFavorites,
  addFavorite,
  removeFavorite,
  updateFavorite,
  setSelectedAvatar,
  // Grid actions removed
  setPinPosition,
  setPinRotation,
  setPinScale,
  setIsPinModeEnabled,
  setPinnedAvatarPosition,
  setIsDragging,
  setDragOffset,
  setActiveSettingsTab,
  setActiveMainTab,
  setCustomModelsLoading,
  setCustomModelsError,
  addCustomModel,
  removeCustomModel,
  loadCustomModels,
  resetPinSettings,
  loadAvatarSettings,
  autoSaveAvatarSettings,
  setLoading,
  setError,
  clearError,
  loadGlobalState,
  saveGlobalState,
  setIsChatOpen,
  addChatMessage,
  setChatHistory,
  setChatContext,
  setIsTyping,
  clearChatHistory,
} = avatarSlice.actions;

// Export selectors with safety checks and proper memoization
const selectAvatarState = (state) => state.avatar;

export const selectFavorites = createSelector(
  [selectAvatarState],
  (avatarState) => {
    const favorites = avatarState.favorites;
    // Ensure favorites is always an array to prevent filter errors
    return Array.isArray(favorites) ? favorites : [];
  }
);
export const selectSelectedAvatar = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.selectedAvatar
);

// Grid selectors removed - only pin mode now

export const selectPinPosition = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.pinPosition
);

export const selectPinRotation = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.pinRotation
);

export const selectPinScale = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.pinScale
);

export const selectIsPinModeEnabled = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.isPinModeEnabled
);

export const selectPinnedAvatarPosition = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.pinnedAvatarPosition
);

export const selectIsDragging = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.isDragging
);

export const selectDragOffset = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.dragOffset
);

export const selectActiveSettingsTab = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.activeSettingsTab
);

export const selectActiveMainTab = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.activeMainTab
);

export const selectCustomModels = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.customModels
);

export const selectCustomModelsLoading = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.customModelsLoading
);

export const selectCustomModelsError = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.customModelsError
);

export const selectAvatarLoading = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.isLoading
);

export const selectAvatarError = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.error
);

// Complex selectors
export const selectHasUnsavedChanges = createSelector(
  [selectAvatarState],
  (avatar) => {
    if (!avatar.selectedAvatar) return false;

    const savedPinPos = avatar.selectedAvatar.pinPosition ||
      avatar.selectedAvatar.avatarPosition || { x: 0, y: -4.0, z: 0 }; // Better default for fallback.glb
    const savedPinRot = avatar.selectedAvatar.pinRotation ||
      avatar.selectedAvatar.avatarRotation || { x: 0, y: 180, z: 0 }; // Face forward by default
    const savedPinScale =
      avatar.selectedAvatar.pinScale ||
      avatar.selectedAvatar.avatarScale ||
      2.5; // Better default for pin mode

    const savedPinMode = avatar.selectedAvatar.isPinModeEnabled !== undefined ?
      avatar.selectedAvatar.isPinModeEnabled : true; // Default to enabled
    const savedPinScreenPos = avatar.selectedAvatar.pinnedAvatarPosition || {
      x: 100,
      y: 100,
    };

    return (
      avatar.pinPosition.x !== savedPinPos.x ||
      avatar.pinPosition.y !== savedPinPos.y ||
      avatar.pinPosition.z !== savedPinPos.z ||
      avatar.pinRotation.x !== savedPinRot.x ||
      avatar.pinRotation.y !== savedPinRot.y ||
      avatar.pinRotation.z !== savedPinRot.z ||
      avatar.pinScale !== savedPinScale ||
      avatar.isPinModeEnabled !== savedPinMode ||
      avatar.pinnedAvatarPosition.x !== savedPinScreenPos.x ||
      avatar.pinnedAvatarPosition.y !== savedPinScreenPos.y
    );
  }
);

// Chat selectors
export const selectIsChatOpen = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.isChatOpen
);

export const selectChatHistory = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.chatHistory
);

export const selectChatContext = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.chatContext
);

export const selectIsTyping = createSelector(
  [selectAvatarState],
  (avatarState) => avatarState.isTyping
);

export default avatarSlice.reducer;
