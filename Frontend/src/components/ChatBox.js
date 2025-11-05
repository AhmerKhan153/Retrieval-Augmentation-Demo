
import React, { useState, useRef, useEffect } from 'react';

function Loader() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', margin: '8px 0' }}>
      <div style={{ width: 24, height: 24, marginRight: 8 }}>
        <svg viewBox="0 0 50 50" style={{ width: '100%', height: '100%' }}>
          <circle cx="25" cy="25" r="20" fill="none" stroke="#888" strokeWidth="5" strokeDasharray="31.4 31.4" strokeLinecap="round">
            <animateTransform attributeName="transform" type="rotate" from="0 25 25" to="360 25 25" dur="1s" repeatCount="indefinite" />
          </circle>
        </svg>
      </div>
      <span style={{ color: '#888' }}>Bot is typing...</span>
    </div>
  );
}

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  async function sendMessage(e) {
    e.preventDefault();
    if (!input.trim()) return;
    setLoading(true);
    setMessages(prev => [...prev, { sender: 'user', text: input }]);
    try {
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await response.json();
      setMessages(prev => [...prev, { sender: 'bot', text: data.response }]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Error connecting to server.' }]);
    }
    setInput('');
    setLoading(false);
  }

  return (
    <div style={{ maxWidth: 420, margin: 'auto', padding: 24, border: '1px solid #ccc', borderRadius: 12, background: '#f5f7fa', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
      <div style={{ height: 340, overflowY: 'auto', marginBottom: 16, background: '#fff', padding: 16, borderRadius: 8, boxShadow: '0 1px 4px rgba(0,0,0,0.03)' }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ display: 'flex', justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start', margin: '10px 0' }}>
            <span style={{
              background: msg.sender === 'user' ? 'linear-gradient(90deg,#d1e7dd,#bfe9ff)' : 'linear-gradient(90deg,#e2e3e5,#f7f7fa)',
              color: '#222',
              padding: '10px 18px',
              borderRadius: msg.sender === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
              maxWidth: '70%',
              boxShadow: '0 1px 4px rgba(0,0,0,0.04)',
              fontSize: '1rem',
              wordBreak: 'break-word',
              border: msg.sender === 'user' ? '1px solid #bfe9ff' : '1px solid #e2e3e5',
              marginLeft: msg.sender === 'user' ? 'auto' : 0,
              marginRight: msg.sender === 'user' ? 0 : 'auto',
            }}>
              {msg.text}
            </span>
          </div>
        ))}
        {loading && <Loader />}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={sendMessage} style={{ display: 'flex', gap: 8 }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
          style={{ flex: 1, padding: 12, borderRadius: 8, border: '1px solid #ccc', fontSize: '1rem' }}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()} style={{ padding: '12px 20px', borderRadius: 8, background: '#1976d2', color: '#fff', border: 'none', fontWeight: 'bold', fontSize: '1rem', cursor: loading ? 'not-allowed' : 'pointer' }}>
          {loading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default ChatBox;
