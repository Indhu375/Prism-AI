export const metadata = {
  title: "Prism AI",
  description: "Turn one product idea into a full marketing campaign",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {/* App Wrapper */}
        <div className="min-h-screen flex flex-col">
          {/* Navbar */}
          <header className="border-b border-gray-800">
            <div className="max-w-6xl mx-auto px-6 py-6 flex items-center justify-between">
              <h1 className="text-2xl font-bold">
                Prism AI 🎨
              </h1>
            </div>
          </header>

          {/* Page Content */}
          <main className="flex-1">
            {children}
          </main>

          {/* Footer */}
          <footer className="border-t border-gray-800">
            <div className="max-w-6xl mx-auto px-6 py-6 text-sm text-gray-500 text-center">
              © {new Date().getFullYear()} Prism AI — AI Marketing Engine
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
