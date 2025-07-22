# Comprehensive Backend API Documentation

This document provides complete API documentation for all backend services in the Gurukul system with curl command examples.

## Service Overview

| Service | Port | Base URL | Description |
|---------|------|----------|-------------|
| API Data Service | 8001 | http://localhost:8001 | RAG, Chat, PDF/Image processing, Video generation |
| Financial Simulator | 8002 | http://localhost:8002 | LangGraph-based financial simulation |
| Memory Management | 8003 | http://localhost:8003 | Memory storage and retrieval |
| Agent Mind-Auth-Memory | 8004 | http://localhost:8004 | Authentication and memory integration |
| Lesson Generator | 8000 | http://localhost:8000 | AI lesson generation and TTS |

---

## 1. API Data Service (Port 8001)

### Health Check
```bash
curl -X GET "http://localhost:8001/health"
```

### Subject Management
```bash
# Get all subjects
curl -X GET "http://localhost:8001/subjects"
```

### Lecture Management
```bash
# Get all lectures
curl -X GET "http://localhost:8001/lectures"
```

### Test Management
```bash
# Get all tests
curl -X GET "http://localhost:8001/tests"
```

### Lesson Generation
```bash
# Generate lesson (GET)
curl -X GET "http://localhost:8001/generate_lesson?subject=mathematics&topic=algebra&include_wikipedia=true&use_knowledge_store=true"

# Create lesson (POST)
curl -X POST "http://localhost:8001/lessons" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "mathematics",
    "topic": "algebra",
    "user_id": "user123",
    "include_wikipedia": true,
    "force_regenerate": false
  }'
```

### Chat System
```bash
# Send chat message
curl -X POST "http://localhost:8001/chatpost" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "timestamp": "2025-01-10T12:00:00Z",
    "type": "chat_message"
  }'

# Get chat response
curl -X GET "http://localhost:8001/chatbot"
```

### PDF Processing
```bash
# Process PDF file
curl -X POST "http://localhost:8001/process-pdf" \
  -F "file=@document.pdf"

# Get PDF summary
curl -X GET "http://localhost:8001/summarize-pdf"
```

### Image Processing
```bash
# Process image file
curl -X POST "http://localhost:8001/process-img" \
  -F "file=@image.jpg"

# Get image summary
curl -X GET "http://localhost:8001/summarize-img"
```

### Audio Streaming
```bash
# Stream audio file
curl -X GET "http://localhost:8001/api/stream/filename.mp3"

# Download audio file
curl -X GET "http://localhost:8001/api/audio/filename.mp3" -o audio.mp3
```

### Video Generation (AnimateDiff Proxy)
```bash
# Generate video
curl -X POST "http://localhost:8001/proxy/vision" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "negative_prompt": "blurry, low quality",
    "num_frames": 16,
    "guidance_scale": 7.5,
    "steps": 25,
    "seed": 333,
    "fps": 8
  }'

# Test video generation
curl -X POST "http://localhost:8001/test-generate-video" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test video generation",
    "num_frames": 8
  }'
```

### Video Storage and Retrieval
```bash
# Upload video with metadata
curl -X POST "http://localhost:8001/receive-video" \
  -F "video=@video.mp4" \
  -F 'metadata={"title":"Test Video","description":"Sample video"}'

# Get video by ID
curl -X GET "http://localhost:8001/videos/video-id-here"

# Get video info
curl -X GET "http://localhost:8001/videos/video-id-here/info"

# List all videos
curl -X GET "http://localhost:8001/videos"
```

---

## 2. Financial Simulator (Port 8002)

### Simulation Management
```bash
# Start simulation
curl -X POST "http://localhost:8002/start-simulation" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "user_name": "John Doe",
    "income": 5000.0,
    "expenses": [
      {"name": "rent", "amount": 1500.0},
      {"name": "food", "amount": 800.0}
    ],
    "total_expenses": 2300.0,
    "goal": "Save for house down payment",
    "financial_type": "conservative",
    "risk_level": "low"
  }'

# Get simulation status
curl -X GET "http://localhost:8002/simulation-status/task-id-here"

# Get simulation results
curl -X GET "http://localhost:8002/simulation-results/task-id-here"
```

### Teacher Agent (Learning)
```bash
# Send learning query (synchronous)
curl -X POST "http://localhost:8002/user/learning" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "query": "Explain compound interest",
    "wait": true
  }'

# Send learning query (asynchronous)
curl -X POST "http://localhost:8002/user/learning" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "query": "What is portfolio diversification?",
    "pdf_id": "pdf-id-here",
    "wait": false
  }'

# Get learning task status
curl -X GET "http://localhost:8002/user/learning/learning-task-id-here"
```

### PDF Management for Learning
```bash
# Upload PDF for learning
curl -X POST "http://localhost:8002/pdf/chat" \
  -F "user_id=user123" \
  -F "pdf_file=@financial_document.pdf"

# Remove PDF data
curl -X POST "http://localhost:8002/pdf/removed" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "pdf_id": "pdf-id-here"
  }'

# List user PDFs
curl -X GET "http://localhost:8002/pdf/list?user_id=user123"
```

---

## 3. Memory Management API (Port 8003)

### Authentication Required
All endpoints require authentication header:
```bash
-H "Authorization: Bearer your-jwt-token"
```

### Health Check
```bash
curl -X GET "http://localhost:8003/memory/health"
```

### Memory Storage
```bash
# Create memory chunk
curl -X POST "http://localhost:8003/memory" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "user_id": "user123",
    "persona_id": "persona456",
    "content": "User prefers morning study sessions",
    "content_type": "preference",
    "metadata": {
      "tags": ["study", "schedule"],
      "importance": "medium",
      "topic": "learning_preferences"
    }
  }'

# Create interaction
curl -X POST "http://localhost:8003/memory/interaction" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "user_id": "user123",
    "persona_id": "persona456",
    "user_message": "I want to learn about calculus",
    "agent_response": "I can help you with calculus. Let me start with derivatives.",
    "context": {
      "session_id": "session789",
      "domain": "mathematics",
      "intent": "learning_request"
    },
    "metadata": {
      "response_time": 1.5,
      "confidence": 0.95
    }
  }'
```

### Memory Retrieval
```bash
# Get memories by persona
curl -X GET "http://localhost:8003/memory?persona=persona456&limit=10&offset=0" \
  -H "Authorization: Bearer your-jwt-token"

# Get recent interactions
curl -X GET "http://localhost:8003/memory?recent_interactions=true&limit=5" \
  -H "Authorization: Bearer your-jwt-token"

# Get specific memory
curl -X GET "http://localhost:8003/memory/memory-id-here" \
  -H "Authorization: Bearer your-jwt-token"

# Get persona memory summary
curl -X GET "http://localhost:8003/memory/persona/persona456/summary" \
  -H "Authorization: Bearer your-jwt-token"
```

### Memory Search
```bash
# Search memories
curl -X GET "http://localhost:8003/memory/search?query=calculus&persona_id=persona456&limit=20" \
  -H "Authorization: Bearer your-jwt-token"
```

### Memory Management
```bash
# Update memory
curl -X PUT "http://localhost:8003/memory/memory-id-here" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "content": "Updated memory content",
    "metadata": {
      "tags": ["updated", "important"],
      "importance": "high"
    }
  }'

# Delete memory (soft delete)
curl -X DELETE "http://localhost:8003/memory/memory-id-here" \
  -H "Authorization: Bearer your-jwt-token"

# Delete memory (hard delete)
curl -X DELETE "http://localhost:8003/memory/memory-id-here?hard_delete=true" \
  -H "Authorization: Bearer your-jwt-token"
```

---

## 4. Agent Mind-Auth-Memory Link (Port 8004)

### Authentication Required
All endpoints require Supabase JWT token:
```bash
-H "Authorization: Bearer supabase-jwt-token"
```

### Health Check
```bash
# Basic health check
curl -X GET "http://localhost:8004/"

# Detailed health check
curl -X GET "http://localhost:8004/health"
```

### Chat with Authentication
```bash
# Send authenticated chat message
curl -X POST "http://localhost:8004/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer supabase-jwt-token" \
  -d '{
    "message": "Hello, I need help with mathematics",
    "include_history": true,
    "max_history_messages": 10,
    "tts_enabled": false
  }'
```

### Progress Management
```bash
# Save progress
curl -X POST "http://localhost:8004/api/v1/save_progress" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer supabase-jwt-token" \
  -d '{
    "chat_history": [
      {
        "role": "user",
        "content": "What is calculus?",
        "timestamp": "2025-01-10T12:00:00Z"
      },
      {
        "role": "assistant", 
        "content": "Calculus is a branch of mathematics...",
        "timestamp": "2025-01-10T12:00:05Z"
      }
    ],
    "session_metadata": {
      "topic": "mathematics",
      "difficulty": "beginner"
    }
  }'

# Get chat history
curl -X GET "http://localhost:8004/api/v1/chat_history?limit=20" \
  -H "Authorization: Bearer supabase-jwt-token"

# Delete user data (GDPR compliance)
curl -X DELETE "http://localhost:8004/api/v1/user_data" \
  -H "Authorization: Bearer supabase-jwt-token"
```

---

## 5. Lesson Generator API (Port 8000)

### Health Check
```bash
# Root endpoint
curl -X GET "http://localhost:8000/"

# LLM status check
curl -X GET "http://localhost:8000/llm_status"
```

### Lesson Management
```bash
# Get existing lesson
curl -X GET "http://localhost:8000/lessons/mathematics/algebra"

# Create new lesson (async)
curl -X POST "http://localhost:8000/lessons" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "mathematics",
    "topic": "calculus",
    "user_id": "user123",
    "include_wikipedia": true,
    "force_regenerate": true
  }'

# Check lesson generation status
curl -X GET "http://localhost:8000/lessons/status/task-id-here"

# List active generation tasks
curl -X GET "http://localhost:8000/lessons/tasks"

# Search lessons
curl -X GET "http://localhost:8000/search_lessons?query=algebra"
```

### TTS Generation
```bash
# Generate TTS for lesson
curl -X POST "http://localhost:8000/lessons/generate-tts" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "lesson-task-id",
    "user_id": "user123",
    "include_sections": ["title", "explanation", "question"],
    "format_style": "complete"
  }'

# Generate TTS from text
curl -X POST "http://localhost:8000/tts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Welcome to our mathematics lesson on algebra.",
    "user_id": "user123",
    "description": "Introduction audio"
  }'
```

### Data Forwarding
```bash
# Forward data to external server
curl -X POST "http://localhost:8000/forward_data" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "lesson_title": "Algebra Basics",
      "content": "Introduction to algebraic concepts..."
    },
    "endpoint": "/api/receive_lesson",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json"
    },
    "timeout": 30,
    "user_id": "user123",
    "description": "Sending lesson to external system"
  }'
```

---

## Common Response Formats

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": { /* response data */ }
}
```

### Error Response
```json
{
  "status": "error", 
  "message": "Error description",
  "detail": "Detailed error information",
  "error_code": "ERROR_CODE"
}
```

### Pagination Response
```json
{
  "data": [ /* array of items */ ],
  "total_count": 100,
  "page": 1,
  "page_size": 20,
  "has_next": true,
  "has_previous": false
}
```

---

## Environment Variables Required

### API Data Service (8001)
- `GROQ_API_KEY`: Groq API key for LLM
- `OPENAI_API_KEY`: OpenAI API key (optional)
- `MONGODB_URI`: MongoDB connection string

### Financial Simulator (8002)
- `OPENAI_API_KEY`: OpenAI API key
- `MONGODB_URI`: MongoDB Atlas connection string

### Memory Management (8003)
- `MONGODB_URI`: MongoDB connection string
- `API_KEY`: API key for authentication

### Agent Mind-Auth-Memory (8004)
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `MONGODB_URI`: MongoDB connection string

### Lesson Generator (8000)
- `OPENAI_API_KEY`: OpenAI API key
- `CHROMA_PERSIST_DIRECTORY`: Vector store directory path

---

## Error Codes and Troubleshooting

### Common HTTP Status Codes
- `200`: Success
- `201`: Created successfully
- `400`: Bad request (invalid parameters)
- `401`: Unauthorized (missing/invalid auth)
- `404`: Resource not found
- `408`: Request timeout
- `500`: Internal server error
- `503`: Service unavailable

### Authentication Issues
- Ensure JWT tokens are valid and not expired
- Check that required headers are included
- Verify API keys are correctly configured

### Connection Issues
- Verify services are running on correct ports
- Check MongoDB connections are established
- Ensure external services (AnimateDiff, TTS) are accessible

---

## Testing Workflow

1. **Start all services** using the startup scripts
2. **Test health endpoints** to verify services are running
3. **Test authentication** with valid tokens
4. **Test core functionality** with sample data
5. **Monitor logs** for any errors or issues

For complete testing, use the provided test scripts in each service directory.

---

## Advanced Usage Examples

### Chaining API Calls

#### Complete Lesson Generation with TTS
```bash
# Step 1: Create lesson
TASK_ID=$(curl -s -X POST "http://localhost:8000/lessons" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "mathematics",
    "topic": "derivatives",
    "user_id": "user123",
    "include_wikipedia": true
  }' | jq -r '.task_id')

# Step 2: Wait and check status
sleep 30
curl -X GET "http://localhost:8000/lessons/status/$TASK_ID"

# Step 3: Generate TTS for completed lesson
curl -X POST "http://localhost:8000/lessons/generate-tts" \
  -H "Content-Type: application/json" \
  -d "{
    \"task_id\": \"$TASK_ID\",
    \"user_id\": \"user123\",
    \"format_style\": \"complete\"
  }"
```

#### Financial Simulation with Learning
```bash
# Step 1: Start financial simulation
SIM_TASK_ID=$(curl -s -X POST "http://localhost:8002/start-simulation" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "user_name": "John Doe",
    "income": 5000.0,
    "expenses": [{"name": "rent", "amount": 1500.0}],
    "total_expenses": 1500.0,
    "goal": "Emergency fund",
    "financial_type": "conservative",
    "risk_level": "low"
  }' | jq -r '.task_id')

# Step 2: Upload financial education PDF
curl -X POST "http://localhost:8002/pdf/chat" \
  -F "user_id=user123" \
  -F "pdf_file=@financial_planning.pdf"

# Step 3: Ask learning question about simulation
curl -X POST "http://localhost:8002/user/learning" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "query": "Based on my simulation, how can I optimize my emergency fund strategy?",
    "wait": true
  }'
```

### Batch Operations

#### Process Multiple PDFs
```bash
#!/bin/bash
for pdf in *.pdf; do
  echo "Processing $pdf..."
  curl -X POST "http://localhost:8001/process-pdf" \
    -F "file=@$pdf" \
    -o "result_$(basename "$pdf" .pdf).json"
  sleep 2
done
```

#### Generate Multiple Videos
```bash
#!/bin/bash
prompts=("A sunset over mountains" "Ocean waves crashing" "Forest in autumn")
for prompt in "${prompts[@]}"; do
  echo "Generating video for: $prompt"
  curl -X POST "http://localhost:8001/proxy/vision" \
    -H "Content-Type: application/json" \
    -d "{
      \"prompt\": \"$prompt\",
      \"num_frames\": 16,
      \"fps\": 8
    }" \
    -o "video_$(echo "$prompt" | tr ' ' '_').mp4"
done
```

---

## Error Handling Examples

### Retry Logic for Failed Requests
```bash
#!/bin/bash
retry_request() {
  local url=$1
  local max_attempts=3
  local attempt=1

  while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt of $max_attempts"

    response=$(curl -s -w "%{http_code}" -X GET "$url")
    http_code="${response: -3}"

    if [ "$http_code" -eq 200 ]; then
      echo "Success!"
      echo "${response%???}" # Remove last 3 chars (HTTP code)
      return 0
    else
      echo "Failed with HTTP code: $http_code"
      if [ $attempt -eq $max_attempts ]; then
        echo "Max attempts reached. Giving up."
        return 1
      fi
      sleep $((attempt * 2)) # Exponential backoff
    fi

    ((attempt++))
  done
}

# Usage
retry_request "http://localhost:8000/llm_status"
```

### Handling Async Operations
```bash
#!/bin/bash
wait_for_completion() {
  local task_id=$1
  local service_url=$2
  local max_wait=300 # 5 minutes
  local elapsed=0

  while [ $elapsed -lt $max_wait ]; do
    status=$(curl -s "$service_url/lessons/status/$task_id" | jq -r '.status')

    case $status in
      "completed")
        echo "Task completed successfully!"
        return 0
        ;;
      "failed")
        echo "Task failed!"
        return 1
        ;;
      "in_progress"|"pending")
        echo "Task status: $status (${elapsed}s elapsed)"
        sleep 10
        elapsed=$((elapsed + 10))
        ;;
      *)
        echo "Unknown status: $status"
        return 1
        ;;
    esac
  done

  echo "Timeout waiting for task completion"
  return 1
}

# Usage
TASK_ID="your-task-id-here"
wait_for_completion "$TASK_ID" "http://localhost:8000"
```

---

## Performance Optimization

### Concurrent Requests
```bash
#!/bin/bash
# Process multiple lessons concurrently
subjects=("mathematics" "physics" "chemistry")
topics=("basics" "advanced" "applications")

for subject in "${subjects[@]}"; do
  for topic in "${topics[@]}"; do
    {
      echo "Starting $subject/$topic"
      curl -X POST "http://localhost:8000/lessons" \
        -H "Content-Type: application/json" \
        -d "{
          \"subject\": \"$subject\",
          \"topic\": \"$topic\",
          \"user_id\": \"batch_user\",
          \"include_wikipedia\": true
        }" &
    }
  done
done

wait # Wait for all background jobs to complete
echo "All lessons started"
```

### Caching Strategies
```bash
#!/bin/bash
# Cache frequently accessed data
CACHE_DIR="./api_cache"
mkdir -p "$CACHE_DIR"

get_with_cache() {
  local url=$1
  local cache_file="$CACHE_DIR/$(echo "$url" | md5sum | cut -d' ' -f1).json"
  local cache_ttl=300 # 5 minutes

  if [ -f "$cache_file" ] && [ $(($(date +%s) - $(stat -c %Y "$cache_file"))) -lt $cache_ttl ]; then
    echo "Using cached data"
    cat "$cache_file"
  else
    echo "Fetching fresh data"
    curl -s "$url" | tee "$cache_file"
  fi
}

# Usage
get_with_cache "http://localhost:8001/subjects"
```

---

## Monitoring and Logging

### Health Check Script
```bash
#!/bin/bash
services=(
  "8001:API Data Service"
  "8002:Financial Simulator"
  "8003:Memory Management"
  "8004:Agent Mind-Auth-Memory"
  "8000:Lesson Generator"
)

echo "=== Service Health Check ==="
for service in "${services[@]}"; do
  port="${service%%:*}"
  name="${service##*:}"

  if curl -s -f "http://localhost:$port/health" > /dev/null 2>&1 || \
     curl -s -f "http://localhost:$port/" > /dev/null 2>&1; then
    echo "✅ $name (port $port): HEALTHY"
  else
    echo "❌ $name (port $port): UNHEALTHY"
  fi
done
```

### Log Analysis
```bash
#!/bin/bash
# Analyze API logs for errors
analyze_logs() {
  local log_file=$1

  echo "=== Error Summary ==="
  grep -i "error\|exception\|failed" "$log_file" | \
    awk '{print $1, $2, $NF}' | \
    sort | uniq -c | sort -nr

  echo -e "\n=== Response Time Analysis ==="
  grep "Time:" "$log_file" | \
    sed 's/.*Time: \([0-9.]*\)s.*/\1/' | \
    awk '{sum+=$1; count++} END {
      if(count>0) {
        print "Average response time:", sum/count "s"
        print "Total requests:", count
      }
    }'
}

# Usage
analyze_logs "Backend/pipline-24-master/app.log"
```

---

## Security Considerations

### API Key Management
```bash
# Secure way to handle API keys
export GROQ_API_KEY="your-secure-key-here"
export OPENAI_API_KEY="your-openai-key-here"

# Use environment variables in requests
curl -X POST "http://localhost:8001/chatpost" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $GROQ_API_KEY" \
  -d '{"message": "Hello"}'
```

### Input Validation Examples
```bash
# Validate JSON before sending
validate_json() {
  local json_string=$1
  if echo "$json_string" | jq empty 2>/dev/null; then
    echo "Valid JSON"
    return 0
  else
    echo "Invalid JSON"
    return 1
  fi
}

# Usage
json_data='{"subject": "math", "topic": "algebra"}'
if validate_json "$json_data"; then
  curl -X POST "http://localhost:8000/lessons" \
    -H "Content-Type: application/json" \
    -d "$json_data"
fi
```

---

## Integration Patterns

### Webhook Integration
```bash
# Set up webhook endpoint to receive notifications
curl -X POST "http://localhost:8001/webhooks/register" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-app.com/webhook/lesson-complete",
    "events": ["lesson.completed", "lesson.failed"],
    "secret": "your-webhook-secret"
  }'
```

### Event-Driven Architecture
```bash
# Subscribe to events
curl -X POST "http://localhost:8002/events/subscribe" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "simulation.completed",
    "callback_url": "https://your-app.com/handle-simulation",
    "user_id": "user123"
  }'
```

This comprehensive documentation provides complete coverage of all backend APIs with practical examples, error handling, performance optimization, and security considerations.
