import React, { useState, useEffect, useRef } from "react";
import { useNavigate, NavLink, useLocation } from "react-router-dom";
import { supabase } from "../supabaseClient";
import gsap from "gsap";
import { useGSAP } from "../hooks/useGSAP";
import "../styles/header.css";

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();
  const [avatarUrl, setAvatarUrl] = useState("");

  // Refs for GSAP animations
  const headerRef = useRef(null);
  const logoRef = useRef(null);
  const aboutLinkRef = useRef(null);
  const logoutBtnRef = useRef(null);

  // We'll use CSS hover effects instead of GSAP for better reliability

  // Initial animation when component mounts
  useGSAP(() => {
    // Initial animation for header
    gsap.fromTo(
      headerRef.current,
      { y: -100, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }
    );

    // Staggered animation for header elements
    gsap.fromTo(
      [logoRef.current, aboutLinkRef.current, logoutBtnRef.current],
      { y: -20, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.6,
        stagger: 0.1,
        ease: "power2.out",
        delay: 0.3,
      }
    );
  }, []);

  // Setup Sign Out button hover animation in a separate useEffect
  useEffect(() => {
    const logoutBtn = logoutBtnRef.current;
    if (!logoutBtn) return;

    // Set initial state with simple styling
    gsap.set(logoutBtn, {
      border: "2px solid transparent",
      borderRadius: "24px",
      boxSizing: "border-box",
      position: "relative",
      overflow: "visible",
    });

    // Simple hover handlers using GSAP for smooth transitions
    const handleMouseEnter = () => {
      // Border color and background change to orange
      gsap.to(logoutBtn, {
        borderColor: "#FF9933", // Orange border
        backgroundColor: "rgba(255, 153, 51, 0.3)", // More vibrant orange background
        duration: 0.15,
        ease: "power2.out",
      });
    };

    const handleMouseLeave = () => {
      gsap.killTweensOf(logoutBtn);

      // Simple fade out
      gsap.to(logoutBtn, {
        borderColor: "transparent",
        backgroundColor: "rgba(255, 255, 255, 0.12)", // Reset to original background
        duration: 0.15,
        ease: "power2.out",
      });
    };

    // Add event listeners
    logoutBtn.addEventListener("mouseenter", handleMouseEnter);
    logoutBtn.addEventListener("mouseleave", handleMouseLeave);

    // Return cleanup function
    return () => {
      if (logoutBtn) {
        logoutBtn.removeEventListener("mouseenter", handleMouseEnter);
        logoutBtn.removeEventListener("mouseleave", handleMouseLeave);
      }
    };
  }, []);

  // Border animation for active link
  useEffect(() => {
    // Capture current refs to use in cleanup function
    const aboutLink = aboutLinkRef.current;

    // Reset border animation
    if (aboutLink) {
      gsap.set(aboutLink, {
        borderColor: "transparent",
        borderWidth: "2px",
        borderStyle: "solid",
        boxSizing: "border-box",
      });
    }

    // Apply border animation if about page is active
    if (location.pathname === "/about" && aboutLink) {
      const tl = gsap.timeline();

      // Start from bottom
      tl.to(aboutLink, {
        borderBottomColor: "#FFA94D",
        duration: 0.15,
        ease: "power2.inOut",
      })
        // Then left side
        .to(aboutLink, {
          borderLeftColor: "#FFA94D",
          duration: 0.15,
          ease: "power2.inOut",
        })
        // Then top
        .to(aboutLink, {
          borderTopColor: "#FFA94D",
          duration: 0.15,
          ease: "power2.inOut",
        })
        // Then right side
        .to(aboutLink, {
          borderRightColor: "#FFA94D",
          duration: 0.15,
          ease: "power2.inOut",
        });

      // No text glow effect as requested
    }

    // Cleanup function
    return () => {
      if (aboutLink) {
        // Kill all animations
        gsap.killTweensOf(aboutLink);

        // Reset border
        gsap.set(aboutLink, {
          borderColor: "transparent",
          borderWidth: "2px",
          borderStyle: "solid",
          boxSizing: "border-box",
        });

        // No text glow to reset
      }
    };
  }, [location.pathname]);

  useEffect(() => {
    const fetchAvatar = async (session) => {
      const user = session?.user;
      if (!user) {
        setAvatarUrl("");
        return;
      }
      setAvatarUrl(
        user.user_metadata?.avatar_url ||
          "https://ui-avatars.com/api/?name=User"
      );
    };

    // Get current session using the newer API
    supabase.auth.getSession().then(({ data }) => {
      fetchAvatar(data.session);
    });

    // Use the newer auth state change API
    const { data: listener } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        fetchAvatar(session);
      }
    );
    return () => {
      if (listener && listener.unsubscribe) listener.unsubscribe();
    };
  }, []);

  const handleLogout = async () => {
    // Click animation - faster and smoother
    if (logoutBtnRef.current) {
      gsap.to(logoutBtnRef.current, {
        scale: 0.97,
        duration: 0.07,
        ease: "power2.in",
        onComplete: async () => {
          if (logoutBtnRef.current) {
            gsap.to(logoutBtnRef.current, {
              scale: 1,
              duration: 0.1,
              ease: "power2.out",
            });
          }
          await supabase.auth.signOut();
          navigate("/signin");
        },
      });
    } else {
      // If button ref is not available, just sign out
      await supabase.auth.signOut();
      navigate("/signin");
    }
  };

  const handleLogoClick = () => {
    // Click animation - faster and smoother
    if (logoRef.current) {
      gsap.to(logoRef.current, {
        scale: 0.97,
        duration: 0.07,
        ease: "power2.in",
        onComplete: () => {
          if (logoRef.current) {
            gsap.to(logoRef.current, {
              scale: 1,
              duration: 0.1,
              ease: "power2.out",
            });
          }
          navigate("/");
        },
      });
    } else {
      // If logo ref is not available, just navigate
      navigate("/");
    }
  };

  return (
    <header ref={headerRef} className="header glassy-header">
      <div className="header-left">
        <span
          ref={logoRef}
          className="logo hover-effect"
          onClick={handleLogoClick}
        >
          Gurukul
        </span>
      </div>
      <div className="header-right">
        <NavLink
          ref={aboutLinkRef}
          to="/about"
          className={({ isActive }) =>
            isActive
              ? "about-link hover-effect active"
              : "about-link hover-effect"
          }
        >
          <span>About</span>
        </NavLink>
        <button
          ref={logoutBtnRef}
          className="logout-btn hover-effect"
          onClick={handleLogout}
        >
          <span className="logout-text">
            <span>Sign Out</span>
          </span>
          {avatarUrl && (
            <img
              src={avatarUrl}
              alt="avatar"
              className="avatar"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "https://ui-avatars.com/api/?name=User";
              }}
            />
          )}
        </button>
      </div>
    </header>
  );
}
