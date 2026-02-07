"use client";
import { useState } from "react";

export default function Home() {
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("Electronics");
  const [tone, setTone] = useState("Professional");

  const [activeTab, setActiveTab] = useState("blog");
  const [loading, setLoading] = useState(false);

  const [blog, setBlog] = useState("");
  const [video, setVideo] = useState("");
  const [history, setHistory] = useState([]);

  const handleGenerate = () => {
    setLoading(true);

    // Fake AI delay
    const handleGenerate = async () => {
  setLoading(true);

  try {
    const response = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        description,
        category,
        tone,
      }),
    });

    const data = await response.json();

    setBlog(data.blog);
    setVideo(data.video);

    setHistory((prev) => [
      {
        description,
        category,
        tone,
        time: new Date().toLocaleTimeString(),
      },
      ...prev,
    ]);
  } catch (error) {
    console.error("Error generating content:", error);
    alert("Backend error. Is FastAPI running?");
  } finally {
    setLoading(false);
  }
};

  };

  const copyText = (text) => {
    navigator.clipboard.writeText(text);
    alert("Copied to clipboard!");
  };

  const downloadText = (text, filename) => {
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
  };

  return (
    <div className="flex min-h-screen bg-black text-white">
      {/* History Sidebar */}
      <aside className="w-72 border-r border-gray-800 p-6 hidden md:block">
        <h3 className="text-lg font-semibold mb-4">🕒 History</h3>
        <div className="space-y-3 text-sm text-gray-400">
          {history.length === 0 && "No history yet"}
          {history.map((item, i) => (
            <div key={i} className="border-b border-gray-800 pb-2">
              <p className="font-medium text-white truncate">
                {item.description || "Untitled Product"}
              </p>
              <p>{item.category} · {item.tone}</p>
              <p className="text-xs">{item.time}</p>
            </div>
          ))}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-10 max-w-6xl mx-auto space-y-12">

        {/* Input Section */}
        <section className="card p-8 space-y-6">
          <h2 className="text-2xl font-semibold">Product Details</h2>

          <textarea
            rows="4"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe your product..."
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <select value={category} onChange={(e) => setCategory(e.target.value)}>
              <option>Electronics</option>
              <option>Fashion</option>
              <option>Food</option>
              <option>SaaS</option>
            </select>

            <select value={tone} onChange={(e) => setTone(e.target.value)}>
              <option>Professional</option>
              <option>Funny</option>
              <option>Emotional</option>
              <option>Persuasive</option>
            </select>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="btn-primary"
          >
            {loading ? "Generating..." : "🚀 Generate Campaign"}
          </button>
        </section>

        {/* Tabs */}
        <section className="space-y-6">
          <div className="flex gap-6 border-b border-gray-800 pb-3">
            {["blog", "image", "video"].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`capitalize ${
                  activeTab === tab
                    ? "text-indigo-400 border-b-2 border-indigo-400"
                    : "text-gray-400"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Blog Tab */}
          {activeTab === "blog" && (
            <div className="card p-6 space-y-4">
              {loading ? (
                <div className="animate-pulse space-y-3">
                  <div className="h-4 bg-gray-700 rounded w-3/4" />
                  <div className="h-4 bg-gray-700 rounded w-full" />
                  <div className="h-4 bg-gray-700 rounded w-5/6" />
                </div>
              ) : (
                <>
                  <p className="muted">{blog || "Blog will appear here..."}</p>
                  {blog && (
                    <div className="flex gap-4">
                      <button onClick={() => copyText(blog)}>📋 Copy</button>
                      <button onClick={() => downloadText(blog, "blog.txt")}>
                        ⬇ Download
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>
          )}

          {/* Image Tab */}
          {activeTab === "image" && (
            <div className="card p-6">
              {loading ? (
                <div className="h-48 bg-gray-700 animate-pulse rounded-xl" />
              ) : (
                <div className="h-48 bg-gray-800 flex items-center justify-center text-gray-500 rounded-xl">
                  Image preview
                </div>
              )}
            </div>
          )}

          {/* Video Tab */}
          {activeTab === "video" && (
            <div className="card p-6 space-y-4">
              {loading ? (
                <div className="animate-pulse space-y-3">
                  <div className="h-4 bg-gray-700 rounded w-2/3" />
                  <div className="h-4 bg-gray-700 rounded w-full" />
                </div>
              ) : (
                <>
                  <p className="muted">{video || "Video script will appear here..."}</p>
                  {video && (
                    <div className="flex gap-4">
                      <button onClick={() => copyText(video)}>📋 Copy</button>
                      <button onClick={() => downloadText(video, "video-script.txt")}>
                        ⬇ Download
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
