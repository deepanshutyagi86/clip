import React, { useState } from 'react';
import { LayoutGrid, GraduationCap, PieChart, Users, FileText, Settings, LogOut, AlertCircle } from 'lucide-react';

const Sidebar = () => {
  const [activeItem, setActiveItem] = useState('Overview');
  const [showWIPAlert, setShowWIPAlert] = useState(false);

  const navItems = [
    { icon: <LayoutGrid className="w-5 h-5" />, label: 'Overview' },
    { icon: <GraduationCap className="w-5 h-5" />, label: 'Classes' },
    { icon: <PieChart className="w-5 h-5" />, label: 'Grades' },
    { icon: <Users className="w-5 h-5" />, label: 'Teachers' },
    { icon: <FileText className="w-5 h-5" />, label: 'Notes' },
  ];

  const handleNavClick = (label) => {
    setActiveItem(label);
    setShowWIPAlert(true);
    setTimeout(() => setShowWIPAlert(false), 3000);
  };

  return (
    <div className="w-64 bg-white border-r border-gray-200 p-4 flex flex-col relative">
      <div className="flex items-center space-x-3 mb-8">
        <img 
          src="/api/placeholder/40/40" 
          alt="Profile" 
          className="w-10 h-10 rounded-full"
        />
        <div>
          <h3 className="font-medium">John Smith</h3>
          <p className="text-sm text-gray-500">j.smith@student.io</p>
        </div>
      </div>
      
      <nav className="flex-1 space-y-1">
        {navItems.map((item) => (
          <button 
            key={item.label}
            onClick={() => handleNavClick(item.label)}
            className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${
              activeItem === item.label
                ? 'bg-gray-100 text-gray-900' 
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            }`}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="border-t border-gray-200 pt-4 space-y-1">
        <button 
          onClick={() => handleNavClick('Settings')}
          className="w-full flex items-center space-x-3 p-3 rounded-lg text-gray-600 hover:bg-gray-50 hover:text-gray-900"
        >
          <Settings className="w-5 h-5" />
          <span>Settings</span>
        </button>
        <button 
          onClick={() => handleNavClick('Logout')}
          className="w-full flex items-center space-x-3 p-3 rounded-lg text-gray-600 hover:bg-gray-50 hover:text-gray-900"
        >
          <LogOut className="w-5 h-5" />
          <span>Log out</span>
        </button>
      </div>

      {/* Work in Progress Alert */}
      {showWIPAlert && (
        <div className="absolute bottom-4 left-4 right-4 bg-blue-50 text-blue-800 px-4 py-2 rounded-lg flex items-center space-x-2 animate-slide-up">
          <AlertCircle className="w-4 h-4" />
          <span className="text-sm">This feature is coming soon!</span>
        </div>
      )}
    </div>
  );
};

export default Sidebar;