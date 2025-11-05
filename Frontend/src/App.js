
import React from 'react';
import ChatBox from './components/ChatBox';

function App() {
  return (
    <div style={{ maxWidth: 500, margin: '40px auto', fontFamily: 'Arial' }}>
      <h2>Incidents Chatbot</h2>
      <ChatBox />
    </div>
  );
}

export default App;
