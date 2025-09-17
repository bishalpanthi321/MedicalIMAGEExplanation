// import React from "react";
// import ReactDOM from "react-dom/client";
// import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
// import "./index.css";
// import Dashboard from "./pages/Dashboard";
// import Upload from "./pages/Upload";
// import PatientDetail from "./pages/PatientDetail";

// function App() {
//   return (
//     <BrowserRouter>
//       <div className="min-h-screen">
//         <header className="bg-white border-b">
//           <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
//             <Link to="/" className="font-semibold text-xl text-primary">MedxAI</Link>
//             <nav className="space-x-4">
//               <Link to="/" className="text-slate-700">Dashboard</Link>
//               <Link to="/upload" className="text-slate-700">Upload</Link>
//             </nav>
//           </div>
//         </header>
//         <main className="max-w-6xl mx-auto px-4 py-6">
//           <Routes>
//             <Route path="/" element={<Dashboard />} />
//             <Route path="/upload" element={<Upload />} />
//             <Route path="/patients/:id" element={<PatientDetail />} />
//           </Routes>
//         </main>
//       </div>
//     </BrowserRouter>
//   );
// }

// ReactDOM.createRoot(document.getElementById("root")!).render(<App />);