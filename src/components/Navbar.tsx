// src/components/Navbar.tsx
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();

    const isActive = (path: string) => location.pathname === path;

    const navLinks = [
        { name: 'Home', path: '/' },
        { name: 'Team', path: '/team' },
        { name: 'Weather', path: '/weather' },
        { name: 'Fashion', path: '/fashion' },
    ];



    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-xl border-b border-slate-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16 md:h-20">
                    <div className="flex items-center">
                        <Link to="/" className="text-xl md:text-2xl font-black tracking-tighter text-slate-900">
                            TEAM
                        </Link>
                    </div>
                    <div className="hidden md:block">
                        <div className="flex items-center space-x-8">
                            {navLinks.map((link) => (
                                <Link
                                    key={link.path}
                                    to={link.path}
                                    className={`text-sm font-bold transition-all duration-300 ${isActive(link.path)
                                        ? 'text-indigo-600'
                                        : 'text-slate-600 hover:text-indigo-500'
                                        }`}
                                >
                                    {link.name}
                                </Link>
                            ))}
                        </div>
                    </div>
                </div>

            </div>
        </nav>
    );
};

export default Navbar;
