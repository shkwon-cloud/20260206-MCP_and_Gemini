// src/pages/Home.tsx
import { useWindowSize } from '../hooks/useWindowSize';

import WeatherWidget from '../components/WeatherWidget';

const Home = () => {
    const { width, height } = useWindowSize();

    return (
        <div className="flex flex-col items-center justify-center min-h-[50vh] text-center space-y-8 md:space-y-12 animate-in fade-in zoom-in duration-1000">
            <div className="space-y-4">
                <h1 className="text-4xl sm:text-6xl md:text-8xl font-black tracking-tighter text-slate-900 leading-tight">
                    <span className="text-indigo-500">TEAM ALPHA</span>
                </h1>
                <p className="max-w-xl mx-auto text-slate-400 text-lg md:text-xl font-medium leading-relaxed">
                    Pioneering the future of digital architecture. We build systems that don't just work—they inspire.
                </p>
            </div>

            {/* Browser Size Display */}
            <div className="bg-slate-100 backdrop-blur-md border border-slate-200 p-4 md:p-6 rounded-2xl space-y-2">
                <h2 className="text-base md:text-xl font-bold text-indigo-600 uppercase tracking-widest">Browser Size</h2>
                <div className="flex space-x-4 md:space-x-8 text-xl md:text-2xl font-black text-slate-900">
                    <div>
                        <span className="text-slate-500 text-[10px] md:text-sm block uppercase tracking-tighter text-left">Width</span>
                        {width}px
                    </div>
                    <div className="w-px bg-slate-200" />
                    <div>
                        <span className="text-slate-500 text-[10px] md:text-sm block uppercase tracking-tighter text-left">Height</span>
                        {height}px
                    </div>
                </div>
            </div>




            {/* 여기에도 부착! */}

            <WeatherWidget />
        </div>
    );
};

export default Home;
