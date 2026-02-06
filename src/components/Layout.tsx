// src/components/Layout.tsx
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';

const Layout = () => {
    return (
        <div className="min-h-screen bg-white text-slate-900 selection:bg-indigo-500/30 selection:text-indigo-900">
            <Navbar />
            <main className="pt-20 md:pt-32 pb-10 md:pb-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <Outlet />
                </div>
            </main>
            <Footer />
        </div>
    );
};

export default Layout;
