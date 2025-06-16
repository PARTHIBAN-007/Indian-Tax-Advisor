import React, { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";


export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    const trimmedInput = input.trim();
    if (!trimmedInput) return;

    const newMessage = { sender: "user", text: trimmedInput };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmedInput }),
      });

      const data = await response.json();
      const aiText = data?.response || "I'm sorry, something went wrong.";
      setMessages((prev) => [...prev, { sender: "bot", text: aiText }]);
    } catch (error) {
      console.error("Fetch error:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "An error occurred. Please try again later." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = async() => {
    try {
      const response = await axios.post("http://localhost:8000/save_docs");
      console.log(response);
      window.location.reload();

    } catch (error) {
      console.log("❌ " + (error.response?.data?.message || "Something went wrong."));
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="flex flex-col w-4/5 h-9/10 bg-white shadow-lg rounded-3xl overflow-hidden border">
        {/* Header */}
        <header className="flex justify-between items-center px-6 py-4 border-b bg-white shadow-sm">
          <h1 className="text-2xl font-semibold text-gray-800">Indian AI Finance Assistant</h1>
          <button
            onClick={handleNewChat}
            className="bg-emerald-400  text-white text-sm font-medium px-4 py-2 rounded-lg transition"
          >
            + New Chat
          </button>
        </header>

        {/* Chat Body */}
        <main className="flex-1 overflow-y-auto px-6 py-6 space-y-4 bg-gray-50">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-md px-4 py-3 rounded-2xl text shadow-md transition-all ${
                  msg.sender === "user"
                    ? "bg-green-400 text-white rounded-br-none"
                    : "bg-blue-50 text-gray-900 rounded-bl-none border"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="px-4 py-2 bg-blue-50 border rounded-xl text-gray-500 text animate-pulse shadow-sm">
                Typing...
              </div>
            </div>
          )}
        </main>

        {/* Chat Input */}
        <form
          onSubmit={handleSend}
          className="px-6 py-4 bg-white border-t flex items-center gap-3 shadow-inner"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-4 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 transition"
            disabled={loading}
          />
          <button
            type="submit"
            className="bg-emerald-500 text-white text-sm font-medium px-5 py-4 rounded-lg hover:bg-emerald-700 transition disabled:opacity-50"
            disabled={loading || !input.trim()}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
