import { useState, useEffect } from 'react';
import { FaMoon, FaSun, FaChevronDown } from 'react-icons/fa';
import { FiArrowUp } from "react-icons/fi";
import { GoSidebarExpand, GoSidebarCollapse } from "react-icons/go";
import './App.css'; // For animation styles

// Logos and backgrounds
import generalF1Logo from './assets/logos/generalf1_logo.png';
import f1logoResized from './assets/logos/f1_logo_resized.png';
import f1logoWhite from './assets/logos/f1_logo_white.png';
import f1logo from './assets/logos/f1_logo.png';
import ferrariLogo from './assets/logos/ferrari_logo.png';
import mercedesLogo from './assets/logos/mercedes_logo.png';
import redBullLogo from './assets/logos/redbull_logo.png';
import mclarenLogo from './assets/logos/mclaren_logo.png';
import astonMartinLogo from './assets/logos/astonmartin_logo.png';
import alpineLogo from './assets/logos/alpine_logo.png';
import williamsLogo from './assets/logos/williams_logo.png';
import rbLogo from './assets/logos/rb_logo.png';
import kickSauberLogo from './assets/logos/kicksauber_logo.png';
import haasLogo from './assets/logos/haas_logo.png';

import generalF1Bg from './assets/backgrounds/f1_bg.jpg';
import ferrariBg from './assets/backgrounds/ferrari_bg.jpg';
import mercedesBg from './assets/backgrounds/mercedes_bg.jpg';
import redBullBg from './assets/backgrounds/redbull_bg.jpg';
import mclarenBg from './assets/backgrounds/mclaren_bg.jpg';
import astonMartinBg from './assets/backgrounds/astonmartin_bg.jpg';
import alpineBg from './assets/backgrounds/alpine_bg.jpg';
import williamsBg from './assets/backgrounds/williams_bg.jpg';
import rbBg from './assets/backgrounds/rb_bg.jpg';
import kickSauberBg from './assets/backgrounds/kicksauber_bg.jpg';
import haasBg from './assets/backgrounds/haas_bg.jpg';

const themes = [
  { name: "General F1", color: "#FF0033", logo: f1logoResized, background: generalF1Bg },
  { name: "Ferrari", color: "#861316", logo: ferrariLogo, background: ferrariBg },
  { name: "Mercedes", color: "#00d2be", logo: mercedesLogo, background: mercedesBg },
  { name: "Red Bull", color: "#0600ef", logo: redBullLogo, background: redBullBg },
  { name: "McLaren", color: "#ff8700", logo: mclarenLogo, background: mclarenBg },
  { name: "Aston Martin", color: "#006f62", logo: astonMartinLogo, background: astonMartinBg },
  { name: "Alpine", color: "#0090ff", logo: alpineLogo, background: alpineBg },
  { name: "Williams", color: "#005aff", logo: williamsLogo, background: williamsBg },
  { name: "RB", color: "#2b4562", logo: rbLogo, background: rbBg },
  { name: "Kick Sauber", color: "#101218", logo: kickSauberLogo, background: kickSauberBg },
  { name: "Haas", color: "#ffffff", logo: haasLogo, background: haasBg },
];

const App = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [currentTheme, setCurrentTheme] = useState(themes[0]);
  const [nextTheme, setNextTheme] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [darkMode, setDarkMode] = useState(true);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [showWelcome, setShowWelcome] = useState(true);
  const [showResponseMenu, setShowResponseMenu] = useState(false);
  const [selectedResponses, setSelectedResponses] = useState({
    "Response 1 (SQL)": false,
    "Response 2 (Best)": true,
    "Response 3 (Test)": false
  });

  // Update the fetchBotResponse function to send selectedResponses to the backend
  const fetchBotResponse = async (userMessage) => {
    try {
      // Use environment variable for API URL
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userMessage,
          selectedResponses: selectedResponses // Send selected responses
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      // Process the responses based on what was selected
      let botResponses = [];
      if (data.responses && data.responses.length > 0) {
        // Combine all selected responses
        botResponses = data.responses.map(res => ({ type: res.type, text: res.content }));
      } else {
        botResponses = [{ type: 'bot', text: "I couldn't generate a response. Please try again." }];
      }

      return botResponses;

    } catch (error) {
      console.error('Error fetching bot response:', error);
      return [{ type: 'bot', text: "Sorry, I'm having trouble connecting to the server. Please try again later." }];
    }
  };

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  useEffect(() => {
    const chatContainer = document.querySelector('.overflow-y-auto');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [messages]);

  // Update the sendMessage function to handle multiple bot responses
  const sendMessage = async () => {
    if (inputMessage.trim()) {
      const userMessage = inputMessage;
      setMessages([
        ...messages,
        { type: 'user', text: userMessage }
      ]);
      setInputMessage('');
      setShowWelcome(false);

      // Get bot responses from API
      const botResponses = await fetchBotResponse(userMessage);
      setMessages(prev => [
        ...prev,
        ...botResponses.map(res => ({ type: 'bot', text: res.text }))
      ]);
    }
  };

  const handleThemeChange = (theme) => {
    if (theme.name === currentTheme.name || isTransitioning) return;
    setIsTransitioning(true);
    setNextTheme(theme);
    setTimeout(() => {
      setCurrentTheme(theme);
      setIsTransitioning(false);
    }, 3000); // animation duration
  };

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);
  const toggleDarkMode = () => setDarkMode(!darkMode);
  const toggleResponseMenu = () => setShowResponseMenu(!showResponseMenu);

  const handleResponseSelection = (response) => {
    setSelectedResponses({
      ...selectedResponses,
      [response]: !selectedResponses[response]
    });
  };

  return (
    <div className={`relative flex h-screen transition-all duration-300 ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      {/* THEME TRANSITION ANIMATION */}
      {isTransitioning && nextTheme && (
        <div className="absolute inset-0 z-50 flex items-center justify-center overflow-hidden bg-black bg-opacity-90 animate-fade">
          <div className="stripes-animation" />
          <img src={nextTheme.logo} className="fade-logo h-32 object-contain z-50" alt="logo" />
        </div>
      )}

      {/* Sidebar */}
      <div className={`${isSidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-gray-100 dark:bg-gray-900 text-white overflow-hidden`}>
        <div className="flex justify-center mt-4 p-2 min-w-[16rem]">
          <span className={`${darkMode ? 'text-white' : 'text-gray-800'} font-medium`}>Select Theme</span>
        </div>
        <div className="space-y-2 p-4 min-w-[16rem]">
          {themes.map((theme, index) => (
            <div
              key={index}
              className={`p-1 rounded-lg w-full flex justify-center items-center transition-colors cursor-pointer
                ${theme.name === currentTheme.name ? 'bg-gray-400' : ''}
                ${darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-300 hover:bg-gray-200'}
              `}
              onClick={() => handleThemeChange(theme)}
            >
              <div className="h-10 w-10 flex items-center justify-center">
                <img src={theme.logo} alt={theme.name} className="max-w-full max-h-full object-contain" />
              </div>
            </div>
          ))}
        </div>
        <button className={`${darkMode ? 'bg-gray-800' : 'bg-gray-100'} w-full py-2 text-center dark:bg-gray-900 hover:bg-gray-600 dark:hover:bg-gray-700 text-white`}>
          <span className={`${darkMode ? 'text-gray-100' : 'text-gray-700'} text-xs font-bold`}>By Hizem</span>
        </button>
      </div>

      {/* Toggle Sidebar Button */}
      <button
        onClick={toggleSidebar}
        className={`fixed top-5 left-4 z-50 p-1 rounded-xl ${darkMode ? 'text-white hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-200'}`}
      >
        {isSidebarOpen ? <GoSidebarExpand size={25} /> : <GoSidebarCollapse size={25} />}
      </button>

      {/* Main content area */}
      <div
        className="flex-1 flex flex-col h-screen overflow-hidden"
        style={{
          backgroundImage: `url(${currentTheme.background})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* Header */}
        <div className="bg-white dark:bg-gray-800 p-4 shadow-md flex justify-between items-center">
  <div className="flex items-center space-x-2">
    <button
      onClick={toggleResponseMenu}
      className={`flex items-center space-x-1 ${darkMode ? 'text-white' : 'text-gray-800'}`}
    >
      {/* Use white logo in dark mode, colored logo in light mode for now disabled */}
      <img 
        src={darkMode ? f1logo : f1logo} 
        className={`max-h-10 max-w-full delay-100 ${isSidebarOpen ? 'ml-0' : 'ml-12'}`} 
        alt="F1 Logo"
      />
      <FaChevronDown 
        size={14} 
        className={`transition-transform ${showResponseMenu ? 'rotate-180' : ''} ${darkMode ? 'text-white' : 'text-gray-800'}`} 
      />
    </button>

            {showResponseMenu && (
              <div
                className={`absolute top-16 z-50 bg-white dark:bg-gray-700 shadow-lg rounded-md p-2 w-48 ${isSidebarOpen ? 'left-64' : 'left-16'
                  }`}
              >
                {Object.keys(selectedResponses).map((response) => (
                  <div
                    key={response}
                    className={`p-2 hover:bg-gray-100 dark:hover:bg-gray-600 rounded cursor-pointer flex items-center ${selectedResponses[response] ? 'bg-blue-100 dark:bg-blue-900' : ''
                      } ${darkMode ? 'text-white' : 'text-gray-800'}`}
                    onClick={() => handleResponseSelection(response)}
                  >
                    <input
                      type="checkbox"
                      checked={selectedResponses[response]}
                      readOnly
                      className="mr-2"
                    />
                    {response}
                  </div>
                ))}
              </div>
            )}
          </div>
          <button onClick={toggleDarkMode} className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-yellow-500">
            {darkMode ? <FaSun size={20} /> : <FaMoon size={20} />}
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-100 dark:bg-gray-700 bg-opacity-40 dark:bg-opacity-70 flex flex-col items-center">
          {showWelcome && (
            <div className="w-full max-w-2xl text-center my-auto">
              <h1 className="text-3xl font-bold mb-2 text-gray-800 dark:text-white">Hello, I am your F1 Assistant 🏎️</h1>
              <p className="text-lg text-gray-600 dark:text-gray-300">How can I assist you today?</p>
            </div>
          )}
          <div className="w-full max-w-2xl space-y-4">
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className="flex items-start space-x-2 max-w-[80%]">
                  {message.type === 'bot' && (
                    <div className="flex-shrink-0 mt-1">
                      <div className="w-8 h-8 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center text-lg">
                        🏎️
                      </div>
                    </div>
                  )}
                  <div
                    className={`p-3 rounded-2xl shadow-md text-white text-sm whitespace-pre-wrap`}
                    style={{ backgroundColor: message.type === 'user' ? currentTheme.color : '#445466' }}
                  >
                    {message.text}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Message Input */}
        <div className="bg-white dark:bg-gray-800 px-4 py-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex flex-col items-center w-full max-w-2xl mx-auto">
            <div className="w-full flex items-end bg-gray-100 dark:bg-gray-700 rounded-3xl px-4 py-2 shadow-md focus-within:ring-2 focus-within:ring-gray-400 dark:focus-within:ring-gray-600 transition mb-1">
              {/* Textarea and button remain the same */}
              <textarea
                rows={1}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                  }
                }}
                placeholder="Type your message..."
                className="flex-grow bg-transparent resize-none outline-none text-gray-800 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 text-sm py-2"
                style={{ maxHeight: '200px' }}
              />
              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim()}
                className={`ml-3 p-2 rounded-full text-white ${inputMessage.trim() ? 'bg-blue-500 hover:bg-blue-600' : 'bg-gray-400 cursor-not-allowed'
                  }`}
                style={{ backgroundColor: currentTheme.color }}
              >
                <FiArrowUp size={20} />
              </button>
            </div>
            {/* Centered disclaimer text */}
            <p className="text-xs text-gray-500 dark:text-gray-400 text-center w-full mt-1">
              AI-generated, for reference only
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;