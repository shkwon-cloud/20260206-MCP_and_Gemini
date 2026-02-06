// src/components/Footer.tsx
const Footer = () => {
    return (
        <footer className="border-t border-slate-100 py-12 bg-slate-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">

                <p className="text-slate-600 text-sm">
                    &copy; {new Date().getFullYear()} Team Introduction Project. Handcrafted with passion and precision.
                </p>
            </div>
        </footer>
    );
};

export default Footer;
