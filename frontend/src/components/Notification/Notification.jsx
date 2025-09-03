import "./Notification.css";
import { useState, useEffect } from "react";

const Notification = ({ 
  type = "success", 
  title, 
  message, 
  isVisible, 
  onClose, 
  duration = 5000 
}) => {
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (isVisible) {
      setIsAnimating(true);
      const timer = setTimeout(() => {
        handleClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [isVisible, duration]);

  const handleClose = () => {
    setIsAnimating(false);
    setTimeout(() => {
      onClose();
    }, 300); // Tempo da animação de saída
  };

  if (!isVisible) return null;

  const getIcon = () => {
    switch (type) {
      case "success":
        return "✅";
      case "error":
        return "❌";
      case "warning":
        return "⚠️";
      case "info":
        return "ℹ️";
      default:
        return "ℹ️";
    }
  };

  const getTypeClass = () => {
    switch (type) {
      case "success":
        return "notification--success";
      case "error":
        return "notification--error";
      case "warning":
        return "notification--warning";
      case "info":
        return "notification--info";
      default:
        return "notification--info";
    }
  };

  return (
    <div className={`notification ${getTypeClass()} ${isAnimating ? 'notification--show' : 'notification--hide'}`}>
      <div className="notification__content">
        <div className="notification__icon">
          {getIcon()}
        </div>
        <div className="notification__text">
          <h4 className="notification__title">{title}</h4>
          <p className="notification__message">{message}</p>
        </div>
        <button 
          className="notification__close" 
          onClick={handleClose}
          aria-label="Fechar notificação"
        >
          ×
        </button>
      </div>
      <div className="notification__progress">
        <div className="notification__progress-bar"></div>
      </div>
    </div>
  );
};

export default Notification;
