import React, { useState } from "react";
import axios from "axios";
import { Mail, User } from "lucide-react"; // icons from lucide-react
import { useNavigate } from "react-router-dom";


export default function UserForm() {
  const [formData, setFormData] = useState({ email: "", username: "" });
  const [status, setStatus] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("Submitting...");
    try {
      const response = await axios.post("http://localhost:8000/user", formData);
      console.log(response);

      
      setStatus(response.data.message);
      navigate("/chat_interface");

    } catch (error) {
      setStatus("❌ " + (error.response?.data?.message || "Something went wrong."));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center ">
      <div className=" bg-grey-800 border border-white/20 shadow-xl rounded-2xl p-8 w-full max-w-md animate-fade-in">
        <h2 className="text-3xl font-roboto  mb-10 text-center">Indian AI Finance Assistant</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block  mb-1">Email</label>
            <div className="flex items-center bg-white/20  rounded px-3 py-2">
              <Mail className=" w-5 h-5 mr-2" />
              <input
                type="email"
                name="email"
                className="bg-transparent focus:outline-none  w-full"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          <div>
            <label className="block  mb-1">Username</label>
            <div className="flex  items-center bg-black-200 rounded px-3 py-2">
              <User className=" w-5 h-5 mr-2" />
              <input
                type="text"
                name="username"
                className=" focus:outline-none  w-full"
                placeholder="yourname"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full bg-green-400 text-white font-semibold py-2 rounded hover:bg-indigo/30 transition duration-200"
          >
            Submit
          </button>
        </form>
        {status && (
          <p className="mt-4 text-sm text-green-400 text-center">{status}</p>
        )}
      </div>
    </div>
  );
}
