import { useState, useCallback } from 'react';

const useNotification = () => {
  const [notifications, setNotifications] = useState([]);

  const addNotification = useCallback((notification) => {
    const id = Date.now() + Math.random();
    const newNotification = {
      id,
      type: 'success',
      duration: 5000,
      ...notification
    };

    setNotifications(prev => [...prev, newNotification]);
    return id;
  }, []);

  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  }, []);

  const showSuccess = useCallback((title, message, duration = 5000) => {
    return addNotification({
      type: 'success',
      title,
      message,
      duration
    });
  }, [addNotification]);

  const showError = useCallback((title, message, duration = 7000) => {
    return addNotification({
      type: 'error',
      title,
      message,
      duration
    });
  }, [addNotification]);

  const showWarning = useCallback((title, message, duration = 6000) => {
    return addNotification({
      type: 'warning',
      title,
      message,
      duration
    });
  }, [addNotification]);

  const showInfo = useCallback((title, message, duration = 5000) => {
    return addNotification({
      type: 'info',
      title,
      message,
      duration
    });
  }, [addNotification]);

  const clearAll = useCallback(() => {
    setNotifications([]);
  }, []);

  return {
    notifications,
    addNotification,
    removeNotification,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    clearAll
  };
};

export default useNotification;
