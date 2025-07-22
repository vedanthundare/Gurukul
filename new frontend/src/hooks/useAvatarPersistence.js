import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import StorageQuotaManager from "../utils/storageQuotaManager";
import {
  setFavorites,
  setSelectedAvatar,
  loadAvatarSettings,
  autoSaveAvatarSettings,
  loadGlobalState,
  saveGlobalState,
  selectFavorites,
  selectSelectedAvatar,
  selectHasUnsavedChanges,
  selectIsPinModeEnabled,
  selectPinnedAvatarPosition,
  selectActiveSettingsTab,
  selectActiveMainTab,
  selectCustomModels,
  loadCustomModels,
  selectPinPosition,
  selectPinRotation,
  selectPinScale,
  selectIsChatOpen,
  selectChatHistory,
} from "../store/avatarSlice";
import { selectIsAuthenticated } from "../store/authSlice";
import { storage } from "../utils/storageUtils";

/**
 * Custom hook to manage avatar persistence with localStorage
 * Handles loading and saving avatar data across sessions
 */
export const useAvatarPersistence = () => {
  const dispatch = useDispatch();
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const favorites = useSelector(selectFavorites);
  const selectedAvatar = useSelector(selectSelectedAvatar);
  const hasUnsavedChanges = useSelector(selectHasUnsavedChanges);

  // Global state selectors for persistence
  const isPinModeEnabled = useSelector(selectIsPinModeEnabled);
  const pinnedAvatarPosition = useSelector(selectPinnedAvatarPosition);
  const activeSettingsTab = useSelector(selectActiveSettingsTab);
  const activeMainTab = useSelector(selectActiveMainTab);
  const customModels = useSelector(selectCustomModels);
  const pinPosition = useSelector(selectPinPosition);
  const pinRotation = useSelector(selectPinRotation);
  const pinScale = useSelector(selectPinScale);
  const isChatOpen = useSelector(selectIsChatOpen);
  const chatHistory = useSelector(selectChatHistory);

  // Initialize storage with aggressive cleanup to prevent quota issues
  useEffect(() => {
    const initializeStorage = async () => {
      try {
        // Aggressive storage cleanup on app start
        console.log('🧹 Performing aggressive storage cleanup...');

        // Clear all blob URLs and temporary data
        const keysToRemove = [];
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          if (key && (
            key.includes('blob:') ||
            key.includes('temp_') ||
            key.includes('cache_') ||
            key.includes('debug_') ||
            key.includes('_backup')
          )) {
            keysToRemove.push(key);
          }
        }

        keysToRemove.forEach(key => {
          try {
            localStorage.removeItem(key);
          } catch (error) {
            console.warn('Failed to remove key:', key, error);
          }
        });

        if (keysToRemove.length > 0) {
          console.log(`🧹 Cleaned up ${keysToRemove.length} temporary storage items`);
        }

        // Monitor and cleanup storage if needed
        const cleanupPerformed = await StorageQuotaManager.monitorAndCleanup();

        if (cleanupPerformed) {
          console.log('🔄 Storage cleanup performed, page will reload...');
          setTimeout(() => window.location.reload(), 1000);
          return;
        }

        // Log current storage usage
        await StorageQuotaManager.checkStorageUsage();
      } catch (error) {
        console.error('Error initializing storage:', error);
      }
    };

    initializeStorage();
  }, []);

  // Initialize default avatar if no favorites exist (Redux persist will handle the rest)
  useEffect(() => {
    // Check if we need to migrate to use fallback.glb as default avatar
    const currentVersion = '2.3'; // Increment this when we need to force migration
    const storedVersion = localStorage.getItem('gurukul_avatar_version');

    if (storedVersion !== currentVersion) {
      console.log('🔄 Avatar system version mismatch, migrating...');
      // Clear all favorites and Redux persist data to ensure clean state
      dispatch(setFavorites([]));

      // Also clear any Redux persist data that might be causing duplicates
      try {
        localStorage.removeItem('persist:root');
        localStorage.removeItem('persist:avatar');
        localStorage.removeItem('gurukul_favorite_avatars');
        console.log('🔄 Cleared Redux persist data');
      } catch (error) {
        console.error('Error clearing persist data:', error);
      }

      localStorage.setItem('gurukul_avatar_version', currentVersion);
      console.log('🔄 Migration completed - all data cleared for fresh start');
    }

    // Only run if we have no favorites (first time setup)
    console.log('🔄 useAvatarPersistence: Checking favorites initialization');
    console.log('🔄 Current favorites type:', typeof favorites);
    console.log('🔄 Current favorites:', favorites);
    console.log('🔄 Selected avatar:', selectedAvatar);

    // Ensure favorites is an array - fix for corrupted Redux state
    if (!Array.isArray(favorites)) {
      console.warn('🚨 Favorites is not an array, resetting to empty array:', typeof favorites, favorites);
      dispatch(setFavorites([]));
      return; // Exit and let the effect run again with clean data
    }

    console.log('🔄 Current favorites length:', favorites.length);

    // Clean up any duplicates first
    const uniqueFavorites = favorites.filter((fav, index, arr) => {
      const firstIndex = arr.findIndex(f => f.id === fav.id);
      return firstIndex === index;
    });

    // If we found duplicates, clean them up
    if (uniqueFavorites.length !== favorites.length) {
      console.log('🔄 Found duplicate favorites, cleaning up...');
      console.log('🔄 Before cleanup:', favorites.length, 'After cleanup:', uniqueFavorites.length);
      dispatch(setFavorites(uniqueFavorites));
      return; // Exit and let the effect run again with clean data
    }

    // Check if we need to initialize or add default avatar
    const hasDefaultAvatar = Array.isArray(favorites) ? favorites.some(fav => fav.id === 'default') : false;
    const hasJupiterAvatar = Array.isArray(favorites) ? favorites.some(fav => fav.id === 'jupiter-default') : false;

    if (favorites.length === 0 || !hasDefaultAvatar || !hasJupiterAvatar) {
      console.log('🔄 Initializing default avatars (no favorites or missing defaults)');

      // If we have favorites but missing defaults, add them to the beginning
      if (favorites.length > 0 && (!hasDefaultAvatar || !hasJupiterAvatar)) {
        console.log('🔄 Adding missing default avatars to existing favorites');
        const newDefaults = [];

        if (!hasDefaultAvatar) {
          const defaultFavorite = {
            id: 'default',
            name: 'Guru1',
            previewUrl: '/avatar/fallback.glb',
            activeTab: 'avatar',
            isDefault: true,
            timestamp: new Date().toISOString(),
          };
          newDefaults.push(defaultFavorite);
        }

        if (!hasJupiterAvatar) {
          const jupiterFavorite = {
            id: 'jupiter-default',
            name: 'Guru2',
            previewUrl: '/avatar/jupiter.glb',
            activeTab: 'avatar',
            isDefault: true,
            timestamp: new Date().toISOString(),
          };
          newDefaults.push(jupiterFavorite);
        }

        dispatch(setFavorites([...newDefaults, ...favorites]));
        return; // Exit early after adding defaults
      }

      // If no favorites at all, initialize with default
      if (favorites.length === 0) {
        const initializeDefaultAvatar = async () => {
          try {
          // Check storage quota before initializing
          if ('storage' in navigator && 'estimate' in navigator.storage) {
            const estimate = await navigator.storage.estimate();
            const usedMB = (estimate.usage / 1024 / 1024).toFixed(2);
            const quotaMB = (estimate.quota / 1024 / 1024).toFixed(2);
            console.log(`Storage usage: ${usedMB}MB / ${quotaMB}MB`);

            // If storage is more than 80% full, clear some space
            if (estimate.usage / estimate.quota > 0.8) {
              console.warn('Storage quota nearly exceeded, clearing old data');
              try {
                // Clear old localStorage items that might be taking up space
                const keysToRemove = [];
                for (let i = 0; i < localStorage.length; i++) {
                  const key = localStorage.key(i);
                  if (key && (key.includes('blob:') || key.includes('temp_') || key.includes('cache_'))) {
                    keysToRemove.push(key);
                  }
                }
                keysToRemove.forEach(key => localStorage.removeItem(key));
                console.log(`Cleared ${keysToRemove.length} old storage items`);
              } catch (cleanupError) {
                console.error('Error cleaning up storage:', cleanupError);
              }
            }
          }

          // Add both default avatars as favorites - using your actual GLB files
          const defaultFavorite = {
            id: 'default',
            name: 'Guru1',
            previewUrl: '/avatar/fallback.glb', // Use your actual fallback.glb file
            activeTab: 'avatar',
            isDefault: true,
            timestamp: new Date().toISOString(),
          };

          const jupiterFavorite = {
            id: 'jupiter-default',
            name: 'Guru2',
            previewUrl: '/avatar/jupiter.glb', // Use your actual jupiter.glb file
            activeTab: 'avatar',
            isDefault: true,
            timestamp: new Date().toISOString(),
          };

          console.log('🔄 Creating default favorites:', { defaultFavorite, jupiterFavorite });
          dispatch(setFavorites([defaultFavorite, jupiterFavorite]));
          dispatch(setSelectedAvatar(defaultFavorite));
          dispatch(loadAvatarSettings(defaultFavorite));
          console.log('🔄 Default avatars initialization completed');
          console.log('🔄 Default avatars should now be visible in favorites tab');
        } catch (error) {
          console.error('Error initializing default avatar:', error);

          // If it's a quota error, try to clear some space and retry
          if (error.name === 'QuotaExceededError') {
            try {
              localStorage.clear();
              // Retry initialization after clearing - include both defaults
              const defaultFavorite = {
                id: 'default',
                name: 'Guru1',
                previewUrl: '/avatar/fallback.glb', // Use your actual fallback.glb file
                activeTab: 'avatar',
                isDefault: true,
                timestamp: new Date().toISOString(),
              };

              const jupiterFavorite = {
                id: 'jupiter-default',
                name: 'Guru2',
                previewUrl: '/avatar/jupiter.glb', // Use your actual jupiter.glb file
                activeTab: 'avatar',
                isDefault: true,
                timestamp: new Date().toISOString(),
              };

              dispatch(setFavorites([defaultFavorite, jupiterFavorite]));
              dispatch(setSelectedAvatar(defaultFavorite));
              dispatch(loadAvatarSettings(defaultFavorite));
            } catch (retryError) {
              console.error('Failed to initialize even after clearing storage:', retryError);
            }
          }
        }
        };

        initializeDefaultAvatar();
      }
    }
  }, [favorites, dispatch]);

  // Restore last selected avatar after favorites are loaded
  useEffect(() => {
    // Only run if we have favorites but no selected avatar
    if (Array.isArray(favorites) && favorites.length > 0 && !selectedAvatar) {
      try {
        const lastSelectedId = storage.getItem('gurukul_last_selected_avatar');
        if (lastSelectedId) {
          const lastSelectedAvatar = Array.isArray(favorites) ? favorites.find(fav => fav.id === lastSelectedId) : null;
          if (lastSelectedAvatar) {
            console.log('🔄 Restoring last selected avatar:', lastSelectedAvatar.name);
            dispatch(setSelectedAvatar(lastSelectedAvatar));
            dispatch(loadAvatarSettings(lastSelectedAvatar));
          } else {
            // If last selected avatar not found, select the first one (usually default)
            console.log('🔄 Last selected avatar not found, selecting first favorite');
            dispatch(setSelectedAvatar(favorites[0]));
            dispatch(loadAvatarSettings(favorites[0]));
          }
        } else {
          // No last selected avatar, select the first one
          console.log('🔄 No last selected avatar, selecting first favorite');
          dispatch(setSelectedAvatar(favorites[0]));
          dispatch(loadAvatarSettings(favorites[0]));
        }
      } catch (error) {
        console.error('Error restoring last selected avatar:', error);
        // Fallback to first favorite
        if (Array.isArray(favorites) && favorites.length > 0) {
          dispatch(setSelectedAvatar(favorites[0]));
          dispatch(loadAvatarSettings(favorites[0]));
        }
      }
    }
  }, [favorites, selectedAvatar, dispatch]);

  // Load custom models from IndexedDB (not handled by Redux persist)
  useEffect(() => {
    const loadCustomModelsFromStorage = async () => {
      try {
        const indexedDBStorage = (await import('../utils/indexedDBStorage')).default;
        const savedCustomModels = await indexedDBStorage.getAllModels();
        if (savedCustomModels && savedCustomModels.length > 0) {
          dispatch(loadCustomModels(savedCustomModels));
          console.log(`Loaded ${savedCustomModels.length} custom models from IndexedDB`);
        }
      } catch (error) {
        console.error('Error loading custom models from IndexedDB:', error);
        // Fallback to localStorage for backward compatibility
        const savedCustomModels = storage.loadCustomModels();
        if (savedCustomModels && savedCustomModels.length > 0) {
          dispatch(loadCustomModels(savedCustomModels));
          console.log(`Loaded ${savedCustomModels.length} custom models from localStorage (fallback)`);
        }
      }
    };

    loadCustomModelsFromStorage();
  }, [dispatch]);

  // Throttled save for pin mode settings changes to prevent storage quota issues
  useEffect(() => {
    if (!selectedAvatar || !hasUnsavedChanges) return;

    // Use longer delay to prevent storage quota exceeded errors
    const throttledTimer = setTimeout(() => {
      try {
        dispatch(autoSaveAvatarSettings());
        console.log(`Saved pin settings for "${selectedAvatar?.name}"`);
      } catch (error) {
        console.warn('Failed to save pin settings:', error);
      }
    }, 2000); // Increased to 2 seconds to reduce storage pressure

    return () => clearTimeout(throttledTimer);
  }, [pinPosition, pinRotation, pinScale, isPinModeEnabled, pinnedAvatarPosition, selectedAvatar, hasUnsavedChanges, dispatch]);

  // Debounced auto-save for grid settings changes
  useEffect(() => {
    if (!hasUnsavedChanges || !selectedAvatar) return;

    const autoSaveTimer = setTimeout(() => {
      try {
        dispatch(autoSaveAvatarSettings());
        console.log(`Auto-saved grid settings for "${selectedAvatar?.name}"`);
      } catch (error) {
        console.warn('Failed to save grid settings:', error);
      }
    }, 3000); // Increased to 3 seconds to reduce storage pressure

    return () => clearTimeout(autoSaveTimer);
  }, [hasUnsavedChanges, selectedAvatar, dispatch]);

  // Storage monitoring to prevent quota issues
  useEffect(() => {
    const monitorStorage = async () => {
      try {
        if ('storage' in navigator && 'estimate' in navigator.storage) {
          const estimate = await navigator.storage.estimate();
          const usagePercent = (estimate.usage / estimate.quota) * 100;

          if (usagePercent > 80) {
            console.warn(`🚨 Storage usage high: ${usagePercent.toFixed(1)}%`);

            // Trigger aggressive cleanup
            const cleanupResult = await StorageQuotaManager.handleQuotaExceeded();
            if (cleanupResult === 'reload_required') {
              console.log('🔄 Reloading page after storage cleanup...');
              setTimeout(() => window.location.reload(), 1000);
            }
          }
        }
      } catch (error) {
        console.warn('Storage monitoring failed:', error);
      }
    };

    // Monitor storage every 30 seconds
    const interval = setInterval(monitorStorage, 30000);
    return () => clearInterval(interval);
  }, []);

  // Manual save function with error handling
  const saveAvatarSettings = () => {
    if (!selectedAvatar) return false;

    try {
      dispatch(autoSaveAvatarSettings());
      return true;
    } catch (error) {
      console.error('Error saving avatar settings:', error);
      if (error.name === 'QuotaExceededError') {
        console.warn('🚨 Storage quota exceeded during manual save');
        StorageQuotaManager.handleQuotaExceeded();
      }
      return false;
    }
  };

  // Load specific avatar
  const loadAvatar = (avatar) => {
    if (!avatar) return;

    dispatch(setSelectedAvatar(avatar));
    dispatch(loadAvatarSettings(avatar));
  };

  return {
    saveAvatarSettings,
    loadAvatar,
    hasUnsavedChanges,
  };
};
