import React, { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "../hooks/useGSAP";

/**
 * GlassButton - Modern glassmorphic button with GSAP animations
 * Props: icon, children, className, variant, ...props
 */
export default function GlassButton({
  icon: Icon,
  children,
  className = "",
  variant = "default", // default, primary, accent
  ...props
}) {
  // Refs for GSAP animations
  const buttonRef = useRef(null);
  const iconRef = useRef(null);
  const textRef = useRef(null);

  // Define variant-specific styles
  const getStyles = () => {
    const baseStyles = {
      background: "rgba(255, 255, 255, 0.15)",
      backdropFilter: "blur(12px)",
      WebkitBackdropFilter: "blur(12px)",
      border: "1px solid rgba(255, 255, 255, 0.25)",
      boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
      color: "#fff",
    };

    switch (variant) {
      case "primary":
        return {
          ...baseStyles,
          background: "rgba(255, 153, 51, 0.25)",
          border: "1px solid rgba(255, 215, 0, 0.4)",
          color: "#FFD700",
          fontWeight: 600,
        };
      case "accent":
        return {
          ...baseStyles,
          background: "rgba(93, 0, 30, 0.25)",
          border: "1px solid rgba(93, 0, 30, 0.5)",
          color: "#fff",
          fontWeight: 600,
        };
      default:
        return baseStyles;
    }
  };

  // Initialize GSAP animations
  useGSAP(() => {
    // Initial entrance animation
    gsap.fromTo(
      buttonRef.current,
      { opacity: 0, y: 10, scale: 0.95 },
      { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power2.out" }
    );
  }, []);

  // Handle hover animations
  const handleMouseEnter = () => {
    // Button glow effect
    gsap.to(buttonRef.current, {
      scale: 1.05,
      boxShadow:
        variant === "primary"
          ? "0 8px 24px rgba(255, 153, 51, 0.3), 0 0 12px rgba(255, 215, 0, 0.3)"
          : variant === "accent"
          ? "0 8px 24px rgba(93, 0, 30, 0.3), 0 0 12px rgba(93, 0, 30, 0.3)"
          : "0 8px 24px rgba(255, 255, 255, 0.2), 0 0 12px rgba(255, 255, 255, 0.2)",
      duration: 0.3,
      ease: "power2.out",
    });

    // Icon and text animations
    if (iconRef.current) {
      gsap.to(iconRef.current, {
        scale: 1.1,
        rotate: 5,
        duration: 0.3,
        ease: "power2.out",
      });
    }

    gsap.to(textRef.current, {
      scale: 1.03,
      duration: 0.3,
      ease: "power2.out",
    });
  };

  // Handle mouse leave animations
  const handleMouseLeave = () => {
    // Reset button
    gsap.to(buttonRef.current, {
      scale: 1,
      boxShadow:
        variant === "primary"
          ? "0 4px 12px rgba(0, 0, 0, 0.15)"
          : variant === "accent"
          ? "0 4px 12px rgba(0, 0, 0, 0.15)"
          : "0 4px 12px rgba(0, 0, 0, 0.15)",
      duration: 0.3,
      ease: "power2.out",
    });

    // Reset icon and text
    if (iconRef.current) {
      gsap.to(iconRef.current, {
        scale: 1,
        rotate: 0,
        duration: 0.3,
        ease: "power2.out",
      });
    }

    gsap.to(textRef.current, {
      scale: 1,
      duration: 0.3,
      ease: "power2.out",
    });
  };

  // Handle click animation
  const handleClick = (e) => {
    // Click animation
    gsap.to(buttonRef.current, {
      scale: 0.95,
      duration: 0.15,
      ease: "power2.inOut",
      onComplete: () => {
        gsap.to(buttonRef.current, {
          scale: 1,
          duration: 0.15,
          ease: "power2.inOut",
        });
      },
    });

    // If there's an onClick handler in props, call it
    if (props.onClick) {
      props.onClick(e);
    }
  };

  return (
    <button
      ref={buttonRef}
      className={`
        flex items-center justify-center gap-2 rounded-xl
        px-6 py-3 font-semibold
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFD700]/30 focus:ring-offset-transparent
        ${className}
      `}
      style={{
        ...getStyles(),
        fontFamily: "Nunito, sans-serif",
      }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
      {...props}
    >
      {Icon && <Icon ref={iconRef} className="w-5 h-5" />}
      <span ref={textRef}>{children}</span>
    </button>
  );
}
