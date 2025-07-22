# 🎨 Frontend Orchestration Integration Guide

This guide explains how to use the enhanced frontend features that integrate with the orchestration system for intelligent, adaptive learning.

## 🚀 **New Frontend Features**

### **1. Enhanced Lesson Generation**
- **AI Orchestration Toggle**: Switch between basic and enhanced lesson generation
- **RAG-Enhanced Content**: Lessons now use 6,224+ educational documents for context
- **Visual Enhancement Indicators**: See when lessons are orchestration-enhanced
- **Automatic Trigger Detection**: System detects when students need help

### **2. User Progress Dashboard**
- **Performance Overview**: Visual performance metrics and trends
- **Quiz Score History**: Interactive charts showing learning progress
- **Personalized Recommendations**: AI-generated suggestions for improvement
- **Intervention Alerts**: Automatic notifications when help is needed

### **3. Smart Intervention System**
- **Automatic Triggers**: System detects struggling students (quiz scores < 60%)
- **One-Click Help**: Easy access to personalized tutoring support
- **Progress Tracking**: Monitor improvement over time

## 🛠️ **Setup Instructions**

### **1. Install Dependencies**
```bash
cd "new frontend"
npm install
```

### **2. Configure API Endpoints**
Update `src/config.js` to ensure it points to your Base_backend:
```javascript
export const API_BASE_URL = "http://localhost:8000";
export const CHAT_API_BASE_URL = "http://localhost:8000";
```

### **3. Start the Frontend**
```bash
npm start
```

The frontend will automatically detect if orchestration is available and enable enhanced features.

## 🎯 **How to Use Enhanced Features**

### **Basic Lesson Generation (Default)**
1. Go to **Subject Explorer** page
2. Select a subject and enter a topic
3. Click **"Explore Subject"**
4. Get basic AI-generated lesson content

### **Enhanced Lesson Generation (Orchestration)**
1. Ensure the **"AI Enhanced"** indicator is visible (green dot)
2. Toggle **"Enhanced Mode"** is enabled (amber button)
3. Generate lessons as normal
4. Notice the **"🚀 Enhanced with AI Orchestration"** banner
5. See additional features:
   - **📚 RAG Enhanced**: Content from 6,224+ documents
   - **⚡ Triggers**: Automatic intervention detection
   - **📖 Sources**: Number of source documents used

### **User Progress Dashboard**
1. **Log in** (required for progress tracking)
2. Click **"View Progress"** button in Subject Explorer
3. See your learning analytics:
   - **Overall Performance**: Average quiz scores and status
   - **Lessons Completed**: Total learning activity
   - **Trend Analysis**: Performance improvement/decline
   - **Quiz Score History**: Visual progress chart
   - **Personalized Recommendations**: AI suggestions

### **Intervention System**
1. When quiz scores drop below 60%, you'll see:
   - **Amber alert banner**: "Intervention Recommended"
   - **"Get Help"** button with trigger count
2. Click **"Get Support"** to trigger interventions
3. System automatically:
   - Calls your Karthikeya tutoring service
   - Provides personalized learning recommendations
   - Tracks intervention effectiveness

## 🔧 **Technical Implementation**

### **New API Integration**
The frontend now includes:
- **`orchestrationApiSlice.js`**: New API slice for orchestration endpoints
- **Enhanced Redux Store**: Includes orchestration state management
- **Smart Fallbacks**: Graceful degradation when orchestration unavailable

### **Key Components Added**
- **`UserProgressDashboard.jsx`**: Comprehensive progress visualization
- **Enhanced `Subjects.jsx`**: Orchestration-aware lesson generation
- **Smart UI Indicators**: Visual feedback for orchestration status

### **API Endpoints Used**
```javascript
// Enhanced lesson generation
POST /lessons/enhanced

// User progress tracking
GET /user-progress/{user_id}

// User analytics
GET /user-analytics/{user_id}

// Trigger interventions
POST /trigger-intervention/{user_id}

// Integration status
GET /integration-status
```

## 📊 **Visual Indicators**

### **Orchestration Status**
- **🟢 "AI Enhanced"**: Orchestration system is active
- **🟡 "Enhanced Mode"**: Using orchestration for lesson generation
- **🔴 "Basic Mode"**: Fallback to simple lesson generation

### **Lesson Enhancement Indicators**
- **🚀 Enhanced with AI Orchestration**: Lesson uses orchestration
- **📚 RAG Enhanced**: Content from vector database
- **⚡ X Triggers**: Number of interventions detected
- **📖 X Sources**: Number of source documents used

### **Progress Dashboard**
- **🟢 Excellent (80%+)**: High performance
- **🔵 Good (70-79%)**: Solid performance  
- **🟡 Average (60-69%)**: Room for improvement
- **🔴 Needs Help (<60%)**: Intervention recommended

## 🧪 **Testing the Integration**

### **1. Test Basic Functionality**
```bash
# Start backend
cd Backend/Base_backend
python api.py

# Start frontend
cd "new frontend"
npm start
```

### **2. Test Enhanced Features**
1. **Check Integration Status**:
   - Visit Subject Explorer
   - Look for "AI Enhanced" indicator
   - Toggle between "Enhanced Mode" and "Basic Mode"

2. **Test Enhanced Lesson Generation**:
   - Generate a lesson with Enhanced Mode enabled
   - Verify orchestration enhancement banner appears
   - Check for RAG enhancement indicators

3. **Test Progress Dashboard**:
   - Log in with a user account
   - Click "View Progress"
   - Verify dashboard loads with mock data

4. **Test Intervention System**:
   - Simulate low quiz score (if available)
   - Check for intervention alerts
   - Test "Get Support" functionality

### **3. Test Fallback Behavior**
1. **Stop Orchestration System**:
   - Lessons should still generate (basic mode)
   - Progress dashboard should show "unavailable" message
   - No orchestration indicators should appear

2. **Network Issues**:
   - Frontend should gracefully handle API failures
   - Toast notifications should inform users of issues
   - Basic functionality should remain available

## 🚨 **Troubleshooting**

### **Common Issues**

1. **"AI Enhanced" indicator not showing**:
   - Check if Backend orchestration system is running
   - Verify Gemini API keys are configured
   - Check browser console for API errors

2. **Progress Dashboard not loading**:
   - Ensure user is logged in (not guest-user)
   - Check if orchestration system is available
   - Verify user has some learning history

3. **Enhanced lessons not generating**:
   - Check orchestration system status
   - Verify vector stores are initialized
   - Check backend logs for errors

4. **Intervention system not working**:
   - Ensure user has quiz score data
   - Check if triggers are properly configured
   - Verify sub-agent URLs are correct

### **Debug Commands**
```bash
# Check API status
curl http://localhost:8000/health
curl http://localhost:8000/integration-status

# Check browser console
# Look for orchestration API calls and responses

# Check Redux DevTools
# Monitor orchestration state changes
```

## 🎯 **Expected User Experience**

### **For New Users**
1. **First Visit**: Basic lesson generation available immediately
2. **Enhanced Features**: Automatically enabled if orchestration available
3. **Progress Tracking**: Starts after first lesson completion

### **For Returning Users**
1. **Personalized Experience**: Progress dashboard shows learning history
2. **Smart Recommendations**: AI suggests areas for improvement
3. **Proactive Support**: Automatic interventions when struggling

### **For Struggling Students**
1. **Early Detection**: System identifies performance issues quickly
2. **Immediate Support**: One-click access to tutoring help
3. **Progress Monitoring**: Track improvement after interventions

---

**🎓 Your frontend now provides an intelligent, adaptive learning experience that grows with each student!**
