import { createContext, useContext } from 'react';
import useNotification from '../hooks/useNotification';

const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const notificationMethods = useNotification();

  return (
    <NotificationContext.Provider value={notificationMethods}>
      {children}
    </NotificationContext.Provider>
  );
};

export const useNotificationContext = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotificationContext deve ser usado dentro de NotificationProvider');
  }
  return context;
};
