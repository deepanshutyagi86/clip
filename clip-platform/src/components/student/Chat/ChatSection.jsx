// src/components/student/Chat/ChatSection.jsx
import React, { useState } from 'react';
import { Send, ChevronDown } from 'lucide-react';

const ChatSection = () => {
  const [messages, setMessages] = useState([
    { 
      id: 1, 
      sender: 'Ben Mojsej', 
      time: '9:28 AM', 
      text: 'I need help with this topic', 
      isUser: false,
      avatar: '/api/placeholder/32/32'
    },
    { 
      id: 2, 
      sender: 'Mark Spring', 
      time: '9:29 AM', 
      text: 'Is computer science also a science?', 
      isUser: false,
      avatar: '/api/placeholder/32/32'
    },
    { 
      id: 3, 
      sender: 'You', 
      time: '9:30 AM', 
      text: 'Listen carefully to the lecture to understand', 
      isUser: true,
      avatar: '/api/placeholder/32/32'
    },
  ]);

  const [newMessage, setNewMessage] = useState('');

  const handleSend = () => {
    if (newMessage.trim()) {
      setMessages([...messages, {
        id: messages.length + 1,
        sender: 'You',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        text: newMessage,
        isUser: true,
        avatar: '/api/placeholder/32/32'
      }]);
      setNewMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-80 bg-white border-l border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200 flex justify-between items-center">
        <h2 className="text-lg font-semibold">Live Chat</h2>
        <button className="p-1 hover:bg-gray-100 rounded-lg transition-colors">
          <ChevronDown className="w-5 h-5" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(message => (
          <div key={message.id} className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}>
            {!message.isUser && (
              <img
                src={message.avatar}
                alt={message.sender}
                className="w-8 h-8 rounded-full mr-2 flex-shrink-0"
              />
            )}
            <div className={`max-w-[80%] ${
              message.isUser ? 'bg-pink-100' : 'bg-gray-100'
            } rounded-lg p-3`}>
              <div className="flex items-center space-x-2 mb-1">
                <span className="text-sm font-medium">{message.sender}</span>
                <span className="text-xs text-gray-500">{message.time}</span>
              </div>
              <p className="text-sm">{message.text}</p>
            </div>
            {message.isUser && (
              <img
                src={message.avatar}
                alt={message.sender}
                className="w-8 h-8 rounded-full ml-2 flex-shrink-0"
              />
            )}
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200">
        <div className="relative">
          <textarea
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your question or message here..."
            className="w-full pl-4 pr-10 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            rows="1"
          />
          <button 
            onClick={handleSend}
            className="absolute right-2 top-2 text-gray-500 hover:text-gray-700 p-1"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatSection;