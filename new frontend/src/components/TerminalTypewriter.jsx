import React, { useState, useEffect } from "react";

/**
 * TerminalTypewriter - Creates terminal-style typewriter effect for text
 * Displays text character by character with blinking cursor
 */
export default function TerminalTypewriter({ 
  text, 
  speed = 30, 
  onComplete = null,
  className = "",
  showCursor = true 
}) {
  const [displayedText, setDisplayedText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timer = setTimeout(() => {
        setDisplayedText(prev => prev + text[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, speed);

      return () => clearTimeout(timer);
    } else if (!isComplete) {
      setIsComplete(true);
      if (onComplete) {
        onComplete();
      }
    }
  }, [currentIndex, text, speed, onComplete, isComplete]);

  // Reset when text changes
  useEffect(() => {
    setDisplayedText("");
    setCurrentIndex(0);
    setIsComplete(false);
  }, [text]);

  return (
    <span className={className}>
      {displayedText}
      {showCursor && !isComplete && (
        <span className="animate-pulse text-orange-500">
          ▋
        </span>
      )}
    </span>
  );
}

/**
 * TerminalMessage - Wrapper component for terminal-style messages
 */
export function TerminalMessage({
  message,
  isUser = false,
  isTyping = false,
  onTypingComplete = null
}) {
  const [showMessage, setShowMessage] = useState(isUser);

  useEffect(() => {
    if (!isUser && !showMessage) {
      // Small delay before starting AI message typing
      const timer = setTimeout(() => {
        setShowMessage(true);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [isUser, showMessage]);

  if (isUser) {
    return (
      <div className="flex items-start gap-2 mb-2">
        <span className="text-orange-500 font-mono text-xs">{'>'}</span>
        <span className="text-orange-400 font-mono text-xs break-words">
          {message.content}
        </span>
      </div>
    );
  }

  if (!showMessage) {
    return null;
  }

  return (
    <div className="flex items-start gap-2 mb-2">
      <span className="text-orange-500 font-mono text-xs">ॐ</span>
      <div className="text-orange-400 font-mono text-xs break-words flex-1">
        {isTyping ? (
          <TerminalTypewriter
            text={message.content}
            speed={20}
            onComplete={onTypingComplete}
            className="text-orange-400"
          />
        ) : (
          message.content
        )}
      </div>
    </div>
  );
}
