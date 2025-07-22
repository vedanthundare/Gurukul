import React, { useState, useRef, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import {
  Send,
  LayoutDashboard,
  BookOpen,
  MessageSquare,
  Settings,
  FileText as FileTextIcon,
  Video,
  Cpu,
  FileDigit,
  UserCircle,
  X,
  ArrowRight,
  Play,
  Upload,
  PenTool,
  Sparkles,
  Home,
  Target,
  BarChart3,
  Search,
  ExternalLink,
  Save,
  Palette,
  Volume2,
  Moon,
  Sun,
  Globe,
  Type,
  Bell,
  Trash2,
  RefreshCw,
  Download,
  History,
  Zap,
} from "lucide-react";
import { toast } from "react-hot-toast";
import {
  selectIsChatOpen,
  selectChatHistory,
  selectIsTyping,
  selectSelectedAvatar,
  selectFavorites,
  setIsChatOpen,
  addChatMessage,
  setChatHistory,
  setIsTyping,
} from "../store/avatarSlice";
import { selectUser } from "../store/authSlice";
import { usePageContext, formatContextForAI } from "../hooks/usePageContext";
import { TerminalMessage } from "./TerminalTypewriter";
import { CHAT_API_BASE_URL } from "../config";
import { supabase } from "../supabaseClient";

/**
 * LoadingDots - Animated loading indicator for chat responses
 */
const LoadingDots = () => (
  <div className="flex items-center gap-1 py-2">
    <span className="text-orange-500 text-xs">{">"}</span>
    <div className="flex gap-1 ml-1">
      <div
        className="w-1 h-1 bg-orange-400 rounded-full animate-pulse"
        style={{ animationDelay: '0ms', animationDuration: '1000ms' }}
      />
      <div
        className="w-1 h-1 bg-orange-400 rounded-full animate-pulse"
        style={{ animationDelay: '200ms', animationDuration: '1000ms' }}
      />
      <div
        className="w-1 h-1 bg-orange-400 rounded-full animate-pulse"
        style={{ animationDelay: '400ms', animationDuration: '1000ms' }}
      />
    </div>
  </div>
);

/**
 * InteractiveButton - Minimal clickable action buttons below the chat interface
 */
const InteractiveButton = ({ icon: Icon, label, onClick, variant = "primary", disabled = false }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    className={`
      flex items-center gap-1 px-2 py-1 rounded text-xs transition-all duration-200
      ${variant === "primary"
        ? "text-orange-400/80 hover:text-orange-300 hover:bg-orange-500/10"
        : "text-white/50 hover:text-white/70 hover:bg-white/5"
      }
      ${disabled ? "opacity-50 cursor-not-allowed" : ""}
    `}
  >
    <Icon className="w-3 h-3" />
    <span>{label}</span>
  </button>
);

/**
 * QuickActionButtons - Contextual action buttons based on current page functionality
 */
const QuickActionButtons = ({ onAction, isFirstTime = false }) => {
  const navigate = useNavigate();

  const handleAction = (action, path = null) => {
    if (path) {
      setTimeout(() => navigate(path), 300);
    }
    if (onAction) {
      onAction(action);
    }
  };

  // Helper function to trigger actual page elements
  const triggerPageAction = (selector, fallbackAction = null) => {
    // Provide immediate feedback
    if (onAction) {
      onAction("action-triggered");
    }

    setTimeout(() => {
      const element = document.querySelector(selector);
      if (element) {
        element.click();
        // Show success feedback
        if (onAction) {
          onAction("action-success");
        }
      } else if (fallbackAction) {
        handleAction(fallbackAction);
      }
    }, 500);
  };

  if (isFirstTime) {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={LayoutDashboard}
          label="Dashboard"
          onClick={() => handleAction("navigate", "/dashboard")}
        />
        <InteractiveButton
          icon={BookOpen}
          label="Subjects"
          onClick={() => handleAction("navigate", "/subjects")}
        />
        <InteractiveButton
          icon={Upload}
          label="Summarizer"
          onClick={() => handleAction("navigate", "/learn")}
        />
        <InteractiveButton
          icon={MessageSquare}
          label="Full Chat"
          onClick={() => handleAction("navigate", "/chatbot")}
        />
      </div>
    );
  }

  const pathname = window.location.pathname;

  // Dashboard - Goal setting, progress tracking
  if (pathname === "/dashboard") {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={Target}
          label="Set Goal"
          onClick={() => triggerPageAction('button:contains("Set Daily Goal")', "set-goal")}
        />
        <InteractiveButton
          icon={BarChart3}
          label="View Stats"
          onClick={() => handleAction("view-stats")}
          variant="secondary"
        />
        <InteractiveButton
          icon={RefreshCw}
          label="Refresh"
          onClick={() => window.location.reload()}
          variant="secondary"
        />
      </div>
    );
  }

  // Subjects - Topic exploration, lesson generation
  if (pathname === "/subjects") {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={Search}
          label="Focus Subject"
          onClick={() => {
            const subjectInput = document.querySelector('input[placeholder*="subject"]');
            if (subjectInput) subjectInput.focus();
          }}
        />
        <InteractiveButton
          icon={BookOpen}
          label="Generate Lesson"
          onClick={() => triggerPageAction('button:contains("Explore Topic")', "generate-lesson")}
        />
        <InteractiveButton
          icon={BarChart3}
          label="View Progress"
          onClick={() => triggerPageAction('button:contains("View Progress")', "view-progress")}
          variant="secondary"
        />
      </div>
    );
  }

  // Summarizer/Learn - File upload, document analysis
  if (pathname === "/learn") {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={Upload}
          label="Upload File"
          onClick={() => {
            const fileInput = document.querySelector('input[type="file"]');
            if (fileInput) fileInput.click();
            else handleAction("upload");
          }}
        />
        <InteractiveButton
          icon={FileTextIcon}
          label="Change Model"
          onClick={() => {
            const modelSelect = document.querySelector('select');
            if (modelSelect) modelSelect.focus();
            else handleAction("change-model");
          }}
          variant="secondary"
        />
        <InteractiveButton
          icon={Sparkles}
          label="Tips"
          onClick={() => handleAction("learn-tips")}
          variant="secondary"
        />
      </div>
    );
  }

  // Chatbot - Model selection, history management
  if (pathname === "/chatbot") {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={RefreshCw}
          label="New Session"
          onClick={() => triggerPageAction('button:contains("New Session")', "new-session")}
        />
        <InteractiveButton
          icon={History}
          label="History"
          onClick={() => triggerPageAction('button:contains("History")', "view-history")}
          variant="secondary"
        />
        <InteractiveButton
          icon={Download}
          label="Export"
          onClick={() => triggerPageAction('button:contains("Export")', "export-chat")}
          variant="secondary"
        />
      </div>
    );
  }

  // Test - Browse and take tests
  if (pathname === "/test") {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={ExternalLink}
          label="Take Test"
          onClick={() => {
            const testCard = document.querySelector('.flip-card');
            if (testCard) testCard.click();
            else handleAction("browse-tests");
          }}
        />
        <InteractiveButton
          icon={Search}
          label="Browse Tests"
          onClick={() => handleAction("browse-tests")}
          variant="secondary"
        />
      </div>
    );
  }

  // Lectures - Watch videos
  if (pathname === "/lectures") {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={Play}
          label="Watch Video"
          onClick={() => {
            const lectureCard = document.querySelector('.flip-card');
            if (lectureCard) lectureCard.click();
            else handleAction("browse-lectures");
          }}
        />
        <InteractiveButton
          icon={Search}
          label="Browse Videos"
          onClick={() => handleAction("browse-lectures")}
          variant="secondary"
        />
      </div>
    );
  }

  // Settings - Configuration options
  if (pathname === "/settings") {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={Save}
          label="Save Settings"
          onClick={() => triggerPageAction('button:contains("Save")', "save-settings")}
        />
        <InteractiveButton
          icon={Moon}
          label="Toggle Theme"
          onClick={() => handleAction("toggle-theme")}
          variant="secondary"
        />
        <InteractiveButton
          icon={Volume2}
          label="Audio Settings"
          onClick={() => handleAction("audio-settings")}
          variant="secondary"
        />
      </div>
    );
  }

  // Avatar Selection - Customization features
  if (pathname === "/avatar-selection") {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={Save}
          label="Save Avatar"
          onClick={() => triggerPageAction('button:contains("Save")', "save-avatar")}
        />
        <InteractiveButton
          icon={Upload}
          label="Upload Model"
          onClick={() => triggerPageAction('input[type="file"]', "upload-model")}
          variant="secondary"
        />
        <InteractiveButton
          icon={Palette}
          label="Customize"
          onClick={() => handleAction("customize-avatar")}
          variant="secondary"
        />
      </div>
    );
  }

  // Agent Simulator
  if (pathname === "/agent-simulator") {
    return (
      <div className="flex flex-wrap gap-1">
        <InteractiveButton
          icon={Play}
          label="Start Sim"
          onClick={() => triggerPageAction('button:contains("Start")', "start-simulation")}
        />
        <InteractiveButton
          icon={RefreshCw}
          label="Reset"
          onClick={() => triggerPageAction('button:contains("Reset")', "reset-simulation")}
          variant="secondary"
        />
      </div>
    );
  }

  // Default for unknown pages
  return (
    <div className="flex flex-wrap gap-1">
      <InteractiveButton
        icon={Sparkles}
        label="Help"
        onClick={() => handleAction("help")}
        variant="secondary"
      />
    </div>
  );
};

/**
 * AvatarChatInterface - Minimal terminal-style chat interface for the floating avatar
 * Positioned near the avatar with context-aware AI responses and typewriter effects
 */
export default function AvatarChatInterface({ avatarPosition }) {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector(selectUser);
  const isChatOpen = useSelector(selectIsChatOpen);
  const chatHistory = useSelector(selectChatHistory);
  const isTyping = useSelector(selectIsTyping);
  const selectedAvatar = useSelector(selectSelectedAvatar);
  const favorites = useSelector(selectFavorites);
  const pageContext = usePageContext();

  const [input, setInput] = useState("");
  const [currentlyTypingMessageId, setCurrentlyTypingMessageId] =
    useState(null);
  const [selectedModel, setSelectedModel] = useState("grok"); // Default to grok model
  const [isNavigating, setIsNavigating] = useState(false);
  const [isLoadingResponse, setIsLoadingResponse] = useState(false); // New loading state
  const inputRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Load the selected model from localStorage if available
  useEffect(() => {
    const savedModel = localStorage.getItem("selectedAIModel");
    if (savedModel) {
      setSelectedModel(savedModel);
    }
  }, []);

  // Helper function to format messages for avatar chat
  const formatAvatarMessage = (message, role = "user", model = "grok") => ({
    id: Date.now() + Math.random(),
    role,
    content: message,
    model,
    timestamp: new Date().toISOString(),
    type: "avatar_chat",
  });

  // Function to get the appropriate icon and header text based on current page
  const getPageHeaderInfo = () => {
    if (!pageContext?.routeContext) {
      return { icon: MessageSquare, header: "AI Guru Chat", description: "browsing the platform" };
    }

    const pathname = window.location.pathname;

    const pageMap = {
      '/dashboard': { icon: LayoutDashboard, header: "Dashboard Overview", description: "viewing the main dashboard" },
      '/subjects': { icon: BookOpen, header: "Subject Explorer", description: "browsing available subjects" },
      '/learn': { icon: FileDigit, header: "Smart Document Analysis", description: "in the learning/summarizer section" },
      '/chatbot': { icon: MessageSquare, header: "AI Guru Chat", description: "in the main chatbot interface" },
      '/test': { icon: FileTextIcon, header: "Assessment Center", description: "taking or viewing tests" },
      '/lectures': { icon: Video, header: "Lecture Hub", description: "browsing lectures" },
      '/agent-simulator': { icon: Cpu, header: "Agent Simulator", description: "in the agent simulator" },
      '/avatar-selection': { icon: UserCircle, header: "Avatar Customization", description: "selecting or customizing your avatar" },
      '/settings': { icon: Settings, header: "Settings Panel", description: "in the settings page" },
    };

    return pageMap[pathname] || { icon: MessageSquare, header: "AI Guru Chat", description: "browsing the platform" };
  };

  // Function to generate intelligent context-aware messages
  const getContextualMessage = (pageInfo, avatarName, isFirstTime = false) => {
    const pathname = window.location.pathname;

    // First time greeting (only when chat is first opened)
    if (isFirstTime) {
      // Check if this is a first-time user on the home page
      const isFirstTimeUser = localStorage.getItem("gurukul_visited") !== "true";

      if (isFirstTimeUser && (pathname === "/home" || pathname === "/")) {
        return `🎓 Hey there! I'm ${avatarName}, your personal AI Guru and learning companion!

Welcome to Gurukul - your gateway to academic excellence! Let me show you around this amazing learning platform:

📊 **Dashboard** - Your learning command center! Track progress, view achievements, and get personalized insights
📚 **Subjects** - Dive into various academic topics and structured courses tailored to your level
📄 **Summarizer** - Upload any document (PDF, text, etc.) and get instant AI-powered summaries and explanations
💬 **Chatbot** - Have in-depth conversations with me about any topic - I'm here 24/7 to help you learn
📝 **Tests** - Take assessments to evaluate your knowledge and identify areas for improvement
🎥 **Lectures** - Access curated educational video content and interactive learning materials

✨ **Interactive Features:**
• **Click the action buttons** below to jump straight to any section
• **Ask me questions** - I understand natural language perfectly
• **I'll follow you** around the site providing contextual help
• **Smart suggestions** - I adapt to each page you visit
• **Instant help** - No waiting, I respond immediately

🚀 **Quick Start Options:**
Use the interactive buttons below to dive right in, or just tell me what you want to do! I can take you anywhere and help with anything.

Ready to start your learning adventure?`;
      }

      // First-time user on other pages - give them a brief intro and guide them
      if (isFirstTimeUser) {
        return `🎓 Hello! I'm ${avatarName}, your AI Guru!

I see you're ${pageInfo.description}. Since this is your first time here, let me quickly introduce Gurukul:

This is your personalized learning platform with AI-powered tools for studying, document analysis, interactive chat, tests, and more!

I'm here to help you navigate and make the most of every feature. Try asking me about what you see on this page, or say "show me around" for a full tour!

What would you like to know?`;
      }

      return `Hello! I'm ${avatarName}, your AI learning companion. I can see you're ${pageInfo.description}. How can I help you?`;
    }

    // Context-aware transition messages for page changes
    const transitionMessages = {
      '/dashboard': [
        "I notice you're checking the dashboard. Need help with any metrics or navigation?",
        "Looking at your dashboard overview? I can help explain any data you see here.",
        "Dashboard view activated. What would you like to explore?"
      ],
      '/subjects': [
        "Ah, exploring subjects! I can help you find the perfect topic to dive into.",
        "Subject exploration mode. What field of knowledge interests you today?",
        "I see you're browsing subjects. Need recommendations based on your learning goals?"
      ],
      '/learn': [
        "Document analysis time! Upload anything you'd like me to summarize or explain.",
        "Ready to analyze some documents? I can break down complex content for you.",
        "Smart analysis mode activated. What documents shall we explore together?"
      ],
      '/chatbot': [
        "Back to our main conversation space. What's on your mind?",
        "Full chat mode engaged. I'm here for any questions or discussions.",
        "Ready for a deeper conversation. How can I assist you today?"
      ],
      '/test': [
        "Assessment center detected. I can help you prepare or review test materials.",
        "Time for some testing? I can assist with study strategies or explanations.",
        "Test mode active. Need help with preparation or understanding concepts?"
      ],
      '/lectures': [
        "Lecture hub opened. Looking for specific educational content?",
        "Ready to dive into some learning materials? I can supplement any lectures.",
        "Educational content mode. What topics would you like to explore?"
      ],
      '/agent-simulator': [
        "Agent simulation environment detected. Interesting choice for experimentation!",
        "Simulation mode active. I can help you understand AI agent behaviors.",
        "Ready to explore AI simulations? This is fascinating territory!"
      ],
      '/avatar-selection': [
        "Avatar customization time! I can help you find the perfect digital companion.",
        "Personalizing your experience? Great choice - appearance matters for connection.",
        "Avatar selection mode. Want help choosing the right companion for your learning journey?"
      ],
      '/settings': [
        "Configuration panel accessed. Need help optimizing your experience?",
        "Settings mode. I can guide you through any customization options.",
        "Time to fine-tune things? I'm here to help with any preferences."
      ]
    };

    // Get random message for current page, fallback to generic
    const messages = transitionMessages[pathname] || [
      "I notice you've moved to a new section. How can I assist you here?",
      "New area detected. What would you like to explore?",
      "I'm adapting to this new context. How can I help?"
    ];

    return messages[Math.floor(Math.random() * messages.length)];
  };

  // Function to get the avatar's display name
  const getAvatarName = () => {
    if (!selectedAvatar) return "your AI assistant";

    try {
      // Try to get custom name from localStorage
      const customNames = JSON.parse(localStorage.getItem('avatar-custom-names') || '{}');
      if (customNames[selectedAvatar.id]) {
        return customNames[selectedAvatar.id];
      }

      // If no custom name, use the avatar's name property or generate default
      if (selectedAvatar.name) {
        return selectedAvatar.name;
      }

      // Find the index in favorites to generate default name
      const avatarIndex = favorites.findIndex(fav => fav.id === selectedAvatar.id);
      return avatarIndex >= 0 ? `Guru${avatarIndex + 1}` : "Guru1";
    } catch (error) {
      console.error('Error getting avatar name:', error);
      return selectedAvatar.name || "your AI assistant";
    }
  };

  // Function to get smart contextual placeholder text
  const getSmartPlaceholder = () => {
    const pathname = window.location.pathname;
    const isFirstTimeUser = localStorage.getItem("gurukul_visited") !== "true";

    if (isFirstTimeUser) {
      return "try: 'show me around' or 'take me to dashboard'...";
    }

    const placeholders = {
      '/home': "try: 'take me to dashboard' or 'what can I do?'...",
      '/dashboard': "ask: 'explain my progress' or 'show subjects'...",
      '/subjects': "try: 'recommend a subject' or 'go to chatbot'...",
      '/learn': "try: 'upload tips' or 'how does this work?'...",
      '/chatbot': "ask me anything or say 'go to summarizer'...",
      '/test': "try: 'start a test' or 'view my results'...",
      '/lectures': "try: 'recommend videos' or 'browse topics'...",
      '/avatar-selection': "try: 'help me choose' or 'customization tips'...",
      '/settings': "try: 'explain settings' or 'optimization tips'..."
    };

    return placeholders[pathname] || "ask uniguru anything...";
  };

  // Direct API functions (same as main chatbot)
  const sendChatMessage = async (userQuery, userId, llmModel = "grok") => {
    console.log(`DEBUG - Avatar Chat: Sending chat message to ${CHAT_API_BASE_URL}/chatpost`);
    console.log(`DEBUG - Avatar Chat: User ID: ${userId}, Model: ${llmModel}`);
    console.log(`DEBUG - Avatar Chat: Message: ${userQuery}`);

    try {
      const response = await fetch(`${CHAT_API_BASE_URL}/chatpost?user_id=${userId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userQuery,
          llm: llmModel,
          type: "chat_message",
        }),
      });

      if (!response.ok) {
        console.error(`HTTP error! status: ${response.status}`);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("DEBUG - Avatar Chat: Chat message sent successfully:", data);
      return data;
    } catch (error) {
      console.error("DEBUG - Avatar Chat: Error sending chat message:", error);
      throw error;
    }
  };

  const fetchChatbotResponse = async (userId) => {
    console.log(`DEBUG - Avatar Chat: Fetching chatbot response from ${CHAT_API_BASE_URL}/chatbot`);
    console.log(`DEBUG - Avatar Chat: User ID: ${userId}`);

    try {
      // Add timestamp to prevent caching
      const timestamp = new Date().getTime();
      const response = await fetch(`${CHAT_API_BASE_URL}/chatbot?user_id=${userId}&timestamp=${timestamp}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Cache-Control": "no-cache, no-store, must-revalidate",
          "Pragma": "no-cache",
          "Expires": "0"
        },
      });

      if (!response.ok) {
        console.error(`HTTP error! status: ${response.status}`);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("DEBUG - Avatar Chat: Chatbot response received:", data);
      return data;
    } catch (error) {
      console.error("DEBUG - Avatar Chat: Error fetching chatbot response:", error);
      throw error;
    }
  };

  // Auto-scroll to bottom when new messages arrive or loading state changes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory, isTyping, isLoadingResponse]);

  // Detect navigation and prevent chat from closing
  useEffect(() => {
    if (pageContext) {
      setIsNavigating(true);
      const timer = setTimeout(() => {
        setIsNavigating(false);
      }, 500); // Give 500ms buffer after navigation

      return () => clearTimeout(timer);
    }
  }, [pageContext]);

  // Close chat when clicking outside (but not during navigation)
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        isChatOpen &&
        !isNavigating && // Don't close during navigation
        !event.target.closest("[data-chat-interface]") &&
        !event.target.closest("[data-avatar-container]") &&
        !event.target.closest("nav") && // Don't close when clicking navigation
        !event.target.closest(".sidebar") && // Don't close when clicking sidebar
        !event.target.closest("a") && // Don't close when clicking links
        !event.target.closest("button") && // Don't close when clicking buttons (except send)
        !event.target.closest(".header") // Don't close when clicking header
      ) {
        dispatch(setIsChatOpen(false));
      }
    };

    // Add a small delay to prevent immediate closing during navigation
    let timeoutId;
    const delayedHandleClickOutside = (event) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => handleClickOutside(event), 100);
    };

    document.addEventListener("mousedown", delayedHandleClickOutside);
    return () => {
      document.removeEventListener("mousedown", delayedHandleClickOutside);
      clearTimeout(timeoutId);
    };
  }, [isChatOpen, isNavigating, dispatch]);

  // Focus input when chat opens and add welcome message if first time
  useEffect(() => {
    if (isChatOpen) {
      // Focus input
      if (inputRef.current) {
        setTimeout(() => inputRef.current?.focus(), 100);
      }

      // Add welcome message if chat history is empty
      if (chatHistory.length === 0) {
        // Get page-specific header info
        const pageInfo = getPageHeaderInfo();
        const avatarName = getAvatarName();

        // Use intelligent contextual message for first time
        const welcomeMessage = formatAvatarMessage(
          getContextualMessage(pageInfo, avatarName, true),
          "assistant",
          "system"
        );
        dispatch(addChatMessage(welcomeMessage));
        setCurrentlyTypingMessageId(welcomeMessage.id);
      }
    }
  }, [isChatOpen, chatHistory.length, pageContext, dispatch, selectedAvatar, favorites]);

  // Track the last page path to detect actual page changes
  const [lastPagePath, setLastPagePath] = useState(window.location.pathname);

  // Update context message when page actually changes (intelligent transitions)
  useEffect(() => {
    const currentPath = window.location.pathname;

    // Only update if the page actually changed and chat is open with messages
    if (isChatOpen && chatHistory.length > 0 && currentPath !== lastPagePath) {
      // Find all system messages (there might be duplicates)
      const systemMessages = chatHistory.filter(msg => msg.model === "system" && msg.role === "assistant");

      if (systemMessages.length > 0) {
        // Get current page info and avatar name
        const pageInfo = getPageHeaderInfo();
        const avatarName = getAvatarName();

        // Generate intelligent contextual message (not first time)
        const contextualContent = getContextualMessage(pageInfo, avatarName, false);

        // Remove all existing system messages and add one updated message
        const nonSystemMessages = chatHistory.filter(msg => !(msg.model === "system" && msg.role === "assistant"));

        // Create new contextual message
        const updatedContextMessage = formatAvatarMessage(
          contextualContent,
          "assistant",
          "system"
        );

        // Update chat history with the new contextual message at the beginning
        const updatedChatHistory = [updatedContextMessage, ...nonSystemMessages];
        dispatch(setChatHistory(updatedChatHistory));
        setCurrentlyTypingMessageId(updatedContextMessage.id);

        // Update the last page path to prevent repeated updates
        setLastPagePath(currentPath);
      }
    }
  }, [pageContext, isChatOpen, chatHistory, lastPagePath, dispatch]);

  const handleSendMessage = async () => {
    if (!input.trim() || isLoadingResponse) return;

    const userMessage = input.trim();
    setInput("");

    // Check for special tour/introduction requests
    const tourKeywords = ['tour', 'show me around', 'introduce', 'what can you do', 'help me navigate', 'guide me', 'features', 'how does this work', 'what is this', 'explain'];
    const isTourRequest = tourKeywords.some(keyword =>
      userMessage.toLowerCase().includes(keyword.toLowerCase())
    );

    // Check for navigation requests
    const navKeywords = {
      dashboard: ['dashboard', 'go to dashboard', 'show dashboard', 'take me to dashboard'],
      subjects: ['subjects', 'go to subjects', 'show subjects', 'browse subjects'],
      learn: ['summarizer', 'go to learn', 'upload document', 'analyze document', 'summarize'],
      chatbot: ['chatbot', 'full chat', 'main chat', 'go to chatbot'],
      test: ['test', 'quiz', 'assessment', 'go to test', 'take test'],
      lectures: ['lectures', 'videos', 'go to lectures', 'watch lectures'],
      home: ['home', 'go home', 'back to home', 'main page']
    };

    let navigationRequest = null;
    for (const [page, keywords] of Object.entries(navKeywords)) {
      if (keywords.some(keyword => userMessage.toLowerCase().includes(keyword.toLowerCase()))) {
        navigationRequest = page;
        break;
      }
    }

    // Check for reset requests (for testing)
    const resetKeywords = ['reset first time', 'reset visited', 'make me new user', 'reset intro'];
    const isResetRequest = resetKeywords.some(keyword =>
      userMessage.toLowerCase().includes(keyword.toLowerCase())
    );

    // Add user message to history
    const userMessageObj = formatAvatarMessage(userMessage, "user");
    dispatch(addChatMessage(userMessageObj));

    // Handle navigation requests
    if (navigationRequest) {
      const pageMap = {
        dashboard: '/dashboard',
        subjects: '/subjects',
        learn: '/learn',
        chatbot: '/chatbot',
        test: '/test',
        lectures: '/lectures',
        home: '/home'
      };

      const targetPath = pageMap[navigationRequest];
      const avatarName = getAvatarName();

      const navMessage = `🚀 Perfect! Taking you to ${navigationRequest.charAt(0).toUpperCase() + navigationRequest.slice(1)} now. I'll be right there with you to help!`;
      const navMessageObj = formatAvatarMessage(navMessage, "assistant", "system");
      dispatch(addChatMessage(navMessageObj));
      setCurrentlyTypingMessageId(navMessageObj.id);

      // Navigate after a short delay
      setTimeout(() => {
        navigate(targetPath);
      }, 1500);
      return;
    }

    // Handle reset requests for testing
    if (isResetRequest) {
      localStorage.removeItem("gurukul_visited");
      const resetMessage = `🔄 Done! I've reset your first-time user status. Refresh the page to see the full introduction again!`;
      const resetMessageObj = formatAvatarMessage(resetMessage, "assistant", "system");
      dispatch(addChatMessage(resetMessageObj));
      setCurrentlyTypingMessageId(resetMessageObj.id);
      return;
    }

    // Handle tour requests locally without API call
    if (isTourRequest) {
      const avatarName = getAvatarName();
      const tourMessage = `🎓 Absolutely! Let me give you the grand tour of Gurukul:

🏠 **Home** - Your starting point with quick access to all features
📊 **Dashboard** - Your personal learning analytics and progress tracking
📚 **Subjects** - Organized academic content across multiple disciplines
📄 **Summarizer** - AI-powered document analysis and summarization
💬 **Chatbot** - Deep conversations and learning assistance (that's me!)
📝 **Tests** - Assessments and quizzes to test your knowledge
🎥 **Lectures** - Video content and interactive learning materials
⚙️ **Settings** - Customize your experience and preferences
👤 **Avatar Selection** - Choose and customize your AI companion

✨ **Special Features:**
• I follow you around the site providing contextual help
• Upload documents for instant summaries and explanations
• Take tests and get detailed feedback
• Chat with multiple AI models for different perspectives
• Personalized learning recommendations

Navigate using the buttons above, the sidebar menu, or just ask me to take you somewhere! What would you like to explore first?`;

      const tourMessageObj = formatAvatarMessage(tourMessage, "assistant", "system");
      dispatch(addChatMessage(tourMessageObj));
      setCurrentlyTypingMessageId(tourMessageObj.id);
      return;
    }

    try {
      setIsLoadingResponse(true);
      dispatch(setIsTyping(true));

      // Get user ID
      const userId = user?.id || "guest-user";



      // Get user ID (same logic as main chatbot)
      let effectiveUserId = userId;
      if (!effectiveUserId) {
        try {
          // Get the current session
          const { data: sessionData } = await supabase.auth.getSession();
          if (sessionData?.session?.user?.id) {
            effectiveUserId = sessionData.session.user.id;
          } else {
            // Fallback to getUser if session doesn't have what we need
            const { data: userData } = await supabase.auth.getUser();
            if (userData?.user?.id) {
              effectiveUserId = userData.user.id;
            } else {
              effectiveUserId = "guest-user";
            }
          }
        } catch (error) {
          console.error("DEBUG - Avatar Chat: Error getting user ID:", error);
          effectiveUserId = "guest-user";
        }
      }

      // Send message with context (same as main chatbot)
      console.log("DEBUG - Avatar Chat: Sending message to chatpost");
      console.log("DEBUG - Avatar Chat: Using model:", selectedModel);
      console.log("DEBUG - Avatar Chat: Using effective user ID:", effectiveUserId);

      // Enhance the message with page context for better AI responses
      const contextualMessage = pageContext
        ? `${formatContextForAI(pageContext)}\n\nUser Message: ${userMessage}`
        : userMessage;

      try {
        // Send the user's query to the chatpost endpoint with the selected model
        const chatpostResult = await sendChatMessage(contextualMessage, effectiveUserId, selectedModel);
        console.log("DEBUG - Avatar Chat: Initial chatpost result:", chatpostResult);
      } catch (error) {
        console.error("DEBUG - Avatar Chat: Error sending chat message:", error);
        // Continue anyway - the message might still be processed
      }

      // Wait a moment for backend processing
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Fetch AI response with retry logic (similar to main chatbot)
      console.log("DEBUG - Avatar Chat: Fetching response from chatbot endpoint");

      let response = null;
      let aiMessage = "";
      let maxRetries = 5;
      let retryCount = 0;
      let retryDelay = 2000; // Start with 2 seconds

      // Keep trying until we get a response or reach max retries
      while (retryCount < maxRetries) {
        try {
          response = await fetchChatbotResponse(effectiveUserId);
          console.log("DEBUG - Avatar Chat: Got response:", response);

          // If we got a valid response with no "No queries yet" error, break out of the loop
          if (response && (!response.error || response.error !== "No queries yet")) {
            break;
          }

          // If we got a "No queries yet" error, wait and retry
          console.log(`DEBUG - Avatar Chat: Got 'No queries yet' error, retrying (${retryCount + 1}/${maxRetries})...`);
          retryCount++;

          // Exponential backoff - increase delay with each retry
          await new Promise((resolve) => setTimeout(resolve, retryDelay));
          retryDelay = Math.min(retryDelay * 1.5, 10000); // Cap at 10 seconds
        } catch (error) {
          console.error("DEBUG - Avatar Chat: Error fetching response:", error);
          retryCount++;
          await new Promise((resolve) => setTimeout(resolve, retryDelay));
          retryDelay = Math.min(retryDelay * 1.5, 10000);
        }
      }

      // If we've exhausted all retries and still have no valid response
      if (!response || (response.error && response.error === "No queries yet")) {
        aiMessage = "I'm processing your message. Please wait a moment and try again.";
        console.log("DEBUG - Avatar Chat: No valid response after all retries, using fallback");
      }

      // If we don't have an aiMessage yet, process the response
      if (!aiMessage) {
        if (response?.response?.message) {
          aiMessage = response.response.message;
          console.log("DEBUG - Avatar Chat: Found message in response.response.message:", aiMessage);
        } else if (response?.message) {
          aiMessage = response.message;
          console.log("DEBUG - Avatar Chat: Found message directly:", aiMessage);
        } else if (response?.isFirstQuery) {
          aiMessage = "Hi! I'm your AI avatar assistant. I can help you with anything on this page. What would you like to know?";
          console.log("DEBUG - Avatar Chat: Using first query message");
        } else {
          // Fallback message if no response
          aiMessage = "I'm here to help! Feel free to ask me anything about what you're currently viewing.";
          console.log("DEBUG - Avatar Chat: Using fallback message");
        }
      }

      if (aiMessage && aiMessage.trim() !== "") {
        // Get the model used for this response
        const modelUsed = response?.response?.llm || selectedModel;

        const aiMessageObj = formatAvatarMessage(
          aiMessage,
          "assistant",
          modelUsed
        );
        dispatch(addChatMessage(aiMessageObj));
        setCurrentlyTypingMessageId(aiMessageObj.id);
      }
    } catch (error) {
      console.error("Avatar chat error:", error);
      toast.error("Failed to send message. Please try again.");

      // Add error message to chat
      const errorMessage = formatAvatarMessage(
        "Sorry, I'm having trouble responding right now. Please try again in a moment.",
        "assistant",
        "error"
      );
      dispatch(addChatMessage(errorMessage));
    } finally {
      setIsLoadingResponse(false);
      dispatch(setIsTyping(false));
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClose = () => {
    dispatch(setIsChatOpen(false));
  };

  const handleClearMessages = () => {
    dispatch(setChatHistory([]));
    setCurrentlyTypingMessageId(null);
    toast.success("Chat cleared");
  };

  const handleTypingComplete = (messageId) => {
    if (currentlyTypingMessageId === messageId) {
      setCurrentlyTypingMessageId(null);
    }
  };

  // Handle quick action button clicks
  const handleQuickAction = (action) => {
    const avatarName = getAvatarName();
    let responseMessage = "";

    switch (action) {
      // Dashboard actions
      case "set-goal":
        responseMessage = `� **Set Your Daily Learning Goal!**

I can help you establish a realistic daily learning target. A good goal might be:
• **Beginner**: 30-60 minutes daily
• **Intermediate**: 1-2 hours daily
• **Advanced**: 2+ hours daily

Click the "Set Daily Goal" button above to configure your target. I'll help you track your progress and stay motivated!`;
        break;

      case "view-stats":
        responseMessage = `📊 **Your Learning Analytics:**

Here's what I can see on your dashboard:
• **Today's Progress**: Current session time and goal completion
• **Learning Streak**: Consecutive days of learning activity
• **Weekly/Monthly Stats**: Time spent learning over periods
• **Achievements**: Unlocked milestones and badges

Your progress data helps me provide better recommendations. Keep up the great work!`;
        break;

      // Subjects actions
      case "generate-lesson":
        responseMessage = `📚 **Generate Custom Lessons!**

I see you're ready to explore a topic! Here's how to get the best results:

1. **Enter a specific subject** (e.g., "Calculus", "World War II", "Python Programming")
2. **Add a focused topic** (e.g., "derivatives", "causes", "loops")
3. **Click "Explore Topic"** to generate comprehensive content

The system will create structured lessons with explanations, examples, and key concepts. What subject interests you?`;
        break;

      case "view-progress":
        responseMessage = `📈 **Track Your Learning Journey!**

Your progress dashboard shows:
• **Overall Performance**: Quiz scores and completion rates
• **Lessons Completed**: Total learning activities
• **Trend Analysis**: Performance improvements over time
• **Personalized Recommendations**: AI-suggested next steps

This data helps optimize your learning path. Click "View Progress" to see detailed analytics!`;
        break;

      case "tour":
        responseMessage = `🎓 **Complete Platform Tour:**

🏠 **Home** - Your starting point with quick access to all features
📊 **Dashboard** - Personal learning analytics and progress tracking
📚 **Subjects** - Generate custom lessons on any topic
📄 **Summarizer** - AI-powered document analysis and summarization
💬 **Chatbot** - Deep conversations and learning assistance (that's me!)
📝 **Tests** - External assessments and quizzes
🎥 **Lectures** - Video content and educational materials
⚙️ **Settings** - Customize your experience and preferences
👤 **Avatar Selection** - Choose and customize your AI companion

Each section has specialized tools to enhance your learning experience!`;
        break;

      case "upload":
        responseMessage = `📄 Ready to analyze a document! Here's how:

1. **Click the upload area** on this page
2. **Select your file** (PDF, DOCX, TXT, etc.)
3. **Choose analysis type** (summary, key points, Q&A, etc.)
4. **Get instant AI insights** in seconds!

I can help explain any part of your document or answer questions about it. Try uploading something now!`;

        // Try to trigger file upload if we're on the learn page
        setTimeout(() => {
          const uploadArea = document.querySelector('[data-upload-area], .upload-area, input[type="file"]');
          if (uploadArea) {
            uploadArea.click();
          }
        }, 1000);
        break;

      case "examples":
        responseMessage = `📚 Here are some great ways to use the Summarizer:

**Academic Papers** - Get key findings and methodology summaries
**Textbook Chapters** - Extract main concepts and important points
**Research Articles** - Understand conclusions and implications
**Study Notes** - Organize and condense your materials
**Legal Documents** - Break down complex language
**Technical Manuals** - Simplify instructions and procedures

What type of document would you like to analyze?`;
        break;

      case "start-test":
        responseMessage = `📝 Let's get you started with assessments!

**Available Test Types:**
• **Subject Quizzes** - Test knowledge in specific topics
• **Practice Exams** - Full-length assessment simulations
• **Quick Reviews** - Short knowledge checks
• **Custom Tests** - Create your own questions

I can help you choose the right test based on your learning goals. What subject are you focusing on?`;
        break;

      case "view-results":
        responseMessage = `📊 Let's review your performance!

I can help you:
• **Analyze your scores** and identify strengths
• **Understand mistakes** with detailed explanations
• **Plan improvement** strategies for weak areas
• **Track progress** over time
• **Suggest study materials** for better performance

Which test results would you like to review?`;
        break;

      case "start-lecture":
        responseMessage = `🎥 Time to dive into some great content!

**Learning Options:**
• **Video Lectures** - Expert-led educational content
• **Interactive Tutorials** - Hands-on learning experiences
• **Study Guides** - Structured learning paths
• **Practice Sessions** - Apply what you learn

I can recommend content based on your interests and level. What topic would you like to explore?`;
        break;

      case "browse-topics":
        responseMessage = `📚 Let's find the perfect learning content for you!

**Popular Categories:**
• **Mathematics** - From basics to advanced calculus
• **Science** - Physics, Chemistry, Biology
• **Literature** - Classic and modern works
• **History** - World events and civilizations
• **Technology** - Programming, AI, and more
• **Languages** - Communication and linguistics

What subject interests you most right now?`;
        break;

      // Summarizer/Learn actions
      case "change-model":
        responseMessage = `🤖 **AI Model Selection:**

Choose the best AI model for your task:
• **Grok**: Fast, general-purpose analysis
• **GPT-4**: Detailed, comprehensive summaries
• **Claude**: Excellent for academic content
• **Gemini**: Great for technical documents

Each model has different strengths. Try different ones to see which works best for your content type!`;
        break;

      case "learn-tips":
        responseMessage = `💡 **Pro Tips for Document Analysis:**

**Best Practices:**
• **Upload clear, text-based files** for best results
• **Use specific questions** like "What are the key points?"
• **Try different analysis types** - summary, Q&A, key concepts
• **Break large documents** into smaller sections for detailed analysis

**Supported Formats:**
📄 PDF, DOCX, TXT, RTF, and more!

**Smart Questions to Ask:**
• "Summarize this in 3 bullet points"
• "What are the main arguments?"
• "Create study notes from this"
• "Generate quiz questions"

Want to try uploading a document now?`;
        break;

      // Chatbot actions
      case "new-session":
        responseMessage = `🆕 **Start Fresh Conversation:**

Starting a new chat session gives you:
• **Clean slate** for new topics
• **Fresh context** without previous conversation history
• **Better focus** on current questions
• **Organized conversations** by topic

Your previous conversations are saved in history. Ready for a new discussion?`;
        break;

      case "view-history":
        responseMessage = `📚 **Chat History Management:**

Your conversation history includes:
• **All previous sessions** with timestamps
• **Searchable conversations** by topic or date
• **Export options** for important discussions
• **Session switching** to continue old conversations

Use the History button to browse and manage your past conversations!`;
        break;

      case "export-chat":
        responseMessage = `💾 **Export Your Conversations:**

Save your valuable discussions:
• **PDF format** for easy sharing and printing
• **Text format** for notes and documentation
• **Include timestamps** and model information
• **Select specific sessions** or export all

Great for creating study materials from our conversations!`;
        break;

      // Test actions
      case "browse-tests":
        responseMessage = `📝 **Available Tests & Assessments:**

Browse through various test categories:
• **Subject-specific quizzes** for focused learning
• **Comprehensive exams** for thorough evaluation
• **Practice tests** to prepare for real assessments
• **Interactive assessments** with immediate feedback

Each test card shows details on hover. Click any test to open it in a new tab and start your assessment!`;
        break;

      // Lectures actions
      case "browse-lectures":
        responseMessage = `🎥 **Educational Video Content:**

Explore our lecture library:
• **Subject-organized content** across multiple disciplines
• **Interactive video players** with controls
• **High-quality educational material** from experts
• **Self-paced learning** at your convenience

Hover over any video card to see the play button, then click to watch in a new tab!`;
        break;

      // Settings actions
      case "save-settings":
        responseMessage = `💾 **Save Your Preferences:**

Your current settings will be saved including:
• **Theme preferences** (dark/light mode)
• **Font size** for better readability
• **Language selection** for interface
• **Notification preferences**
• **Audio settings** and volume

Click "Save Settings" to apply all changes permanently!`;
        break;

      case "toggle-theme":
        responseMessage = `🌙 **Theme Customization:**

Switch between visual themes:
• **Dark Mode**: Easy on the eyes, great for extended use
• **Light Mode**: Bright and clear for daytime learning
• **Auto-adjust**: Based on system preferences

Your theme choice affects the entire platform appearance!`;
        break;

      case "audio-settings":
        responseMessage = `🔊 **Audio Configuration:**

Customize your audio experience:
• **Enable/disable** notification sounds
• **Adjust volume levels** for alerts
• **Audio feedback** for interactions
• **Voice settings** for accessibility

Fine-tune audio to match your learning environment!`;
        break;

      // Avatar Selection actions
      case "save-avatar":
        responseMessage = `👤 **Save Avatar Configuration:**

Your avatar customization includes:
• **3D model selection** from favorites
• **Position and rotation** settings
• **Scale adjustments** for perfect fit
• **Pin mode settings** for floating avatar

Save your changes to apply them across the platform!`;
        break;

      case "upload-model":
        responseMessage = `📁 **Upload Custom 3D Model:**

Add your own avatar models:
• **Supported formats**: GLB, GLTF files
• **File size limit**: Check requirements
• **Custom animations** if supported
• **Personal collection** management

Upload a .glb file to add it to your custom models collection!`;
        break;

      case "customize-avatar":
        responseMessage = `🎨 **Avatar Customization Options:**

Personalize your AI companion:
• **Choose from favorites** or upload custom models
• **Adjust positioning** with precise controls
• **Scale and rotation** for perfect placement
• **Pin mode settings** for floating behavior
• **Custom naming** for personal connection

Make your avatar truly yours!`;
        break;

      // Agent Simulator actions
      case "start-simulation":
        responseMessage = `🤖 **Agent Simulation Environment:**

Start AI agent simulations:
• **Multiple agent types** with different specializations
• **Real-time interactions** and decision making
• **Performance monitoring** and analytics
• **Educational insights** into AI behavior

Click "Start" to begin the simulation experience!`;
        break;

      case "reset-simulation":
        responseMessage = `🔄 **Reset Simulation State:**

Clear current simulation:
• **Reset all agents** to initial state
• **Clear interaction history** and logs
• **Fresh start** for new experiments
• **Preserve settings** and configurations

Ready to start a new simulation from scratch!`;
        break;

      case "help":
        responseMessage = `🤝 **Contextual Help Available:**

I can assist with:
• **Current page features** and how to use them
• **Navigation guidance** to any section
• **Learning strategies** and study tips
• **Platform optimization** for your needs
• **Troubleshooting** any issues

**Smart Commands:**
• "take me to [page]" for instant navigation
• "how do I..." for step-by-step guidance
• "explain [feature]" for detailed information

What specific help do you need?`;
        break;

      default:
        responseMessage = `I'm ready to help! What would you like to do next?`;
    }

    if (responseMessage) {
      const actionMessageObj = formatAvatarMessage(responseMessage, "assistant", "system");
      dispatch(addChatMessage(actionMessageObj));
      setCurrentlyTypingMessageId(actionMessageObj.id);
    }
  };

  if (!isChatOpen) return null;

  // Calculate position relative to avatar with screen boundary checks
  // Make chat wider for first-time users to accommodate the comprehensive introduction
  const isFirstTimeUser = localStorage.getItem("gurukul_visited") !== "true";
  const isOnHomePage = window.location.pathname === "/home" || window.location.pathname === "/";
  const chatWidth = (isFirstTimeUser && isOnHomePage) ? 400 : 280; // Wider for introduction
  const screenWidth = window.innerWidth;
  const screenHeight = window.innerHeight;

  let chatLeft = avatarPosition.x + 180; // Default to right of avatar
  let chatTop = avatarPosition.y;

  // Check if chat would go off-screen to the right
  if (chatLeft + chatWidth > screenWidth) {
    chatLeft = avatarPosition.x - chatWidth - 20; // Position to the left of avatar
  }

  // Ensure chat doesn't go off-screen at the top or left
  if (chatTop < 20) {
    chatTop = 20;
  }
  if (chatLeft < 20) {
    chatLeft = 20;
  }

  const chatPosition = {
    left: `${chatLeft}px`,
    top: `${chatTop}px`,
  };

  // Check if we should show action buttons
  const shouldShowActionButtons = () => {
    if (chatHistory.length === 0) return false;
    const lastMessage = chatHistory[chatHistory.length - 1];
    return lastMessage.role === "assistant" &&
           lastMessage.model === "system" &&
           currentlyTypingMessageId !== lastMessage.id;
  };

  return (
    <div
      className="fixed z-[10000] animate-in fade-in slide-in-from-bottom-2 duration-200"
      style={{
        ...chatPosition,
        width: `${chatWidth}px`,
      }}
    >
      {/* Gurukul-style Chat Container */}
      <div
        data-chat-interface
        className="font-mono text-sm shadow-2xl transition-all duration-200"
        style={{
          background: "rgba(30, 30, 40, 0.85)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          border: "1px solid rgba(255, 255, 255, 0.2)",
          borderRadius: "12px",
          boxShadow: "0 8px 32px rgba(0, 0, 0, 0.3)",
        }}
      >
        {/* Terminal Messages */}
        <div className={`p-3 overflow-y-auto custom-scrollbar ${(isFirstTimeUser && isOnHomePage) ? 'max-h-80' : 'max-h-48'}`}>
          {chatHistory.map((message) => (
            <TerminalMessage
              key={message.id}
              message={message}
              isUser={message.role === "user"}
              isTyping={currentlyTypingMessageId === message.id}
              onTypingComplete={() => handleTypingComplete(message.id)}
            />
          ))}
          {/* Show loading indicator when waiting for response */}
          {isLoadingResponse && <LoadingDots />}
          <div ref={messagesEndRef} />
        </div>

        {/* Terminal Input */}
        <div className="border-t border-white/10 p-3">
          <div className="flex items-center gap-2">
            <span className="text-orange-500">{">"}</span>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={isLoadingResponse ? "processing..." : getSmartPlaceholder()}
              className="flex-1 bg-transparent border-none outline-none text-orange-400 placeholder-orange-400/40 font-mono text-sm"
              disabled={isTyping || isLoadingResponse}
            />
            {input.trim() && (
              <button
                onClick={handleSendMessage}
                disabled={isTyping || isLoadingResponse}
                className="text-orange-500 hover:text-orange-400 disabled:text-white/30 transition-colors"
              >
                <Send className="w-3 h-3" />
              </button>
            )}
            {/* Clear messages button */}
            {chatHistory.length > 0 && (
              <button
                onClick={handleClearMessages}
                disabled={isTyping || isLoadingResponse}
                className="text-red-400 hover:text-red-300 disabled:text-white/30 transition-colors"
                title="Clear all messages"
              >
                <X className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Interactive Action Buttons - Below Chat Interface */}
      {shouldShowActionButtons() && (
        <div className="mt-2 animate-in fade-in slide-in-from-bottom-1 duration-300">
          {/* Subtle separator */}
          <div className="flex items-center justify-center mb-1">
            <div className="w-8 h-px bg-orange-500/20"></div>
          </div>
          <QuickActionButtons
            onAction={handleQuickAction}
            isFirstTime={isFirstTimeUser && isOnHomePage}
          />
        </div>
      )}

      {/* Gurukul-style glow effect */}
      <div
        className="absolute inset-0 -z-10"
        style={{
          background: `
            radial-gradient(circle at center,
              rgba(255, 153, 51, 0.15) 0%,
              rgba(255, 153, 51, 0.08) 50%,
              transparent 70%
            )
          `,
          filter: "blur(8px)",
          transform: "scale(1.05)",
          borderRadius: "12px",
        }}
      />
    </div>
  );
}
