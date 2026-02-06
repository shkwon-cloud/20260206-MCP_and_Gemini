// src/pages/FashionPage.tsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import useWeather from '../hooks/useWeather';

interface Member {
    username?: string;
    id?: number;
    name: string;
}

interface MemberDetail {
    username: string;
    name: string;
    location: string;
    style: string;
    gender: string;
    role: string;
    imageUrl?: string;
}

export default function FashionPage() {
    const [members, setMembers] = useState<Member[]>([]);
    const [selectedUsername, setSelectedUsername] = useState<string>('');
    const [memberDetail, setMemberDetail] = useState<MemberDetail | null>(null);
    const { currentTemp, aiRecommendation, loading: weatherLoading, fetchWeather } = useWeather();
    const [listLoading, setListLoading] = useState(true);

    // 1. 초기 멤버 목록 가져오기
    useEffect(() => {
        const fetchMembers = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/members');
                console.log("멤버 데이터 수신:", response.data);

                const data = Array.isArray(response.data) ? response.data : response.data.members || [];
                setMembers(data);
                if (data.length > 0) {
                    setSelectedUsername(data[0].username || data[0].id?.toString() || '');
                }
            } catch (err) {
                console.error("멤버 목록 로드 실패:", err);
            } finally {
                setListLoading(false);
            }
        };
        fetchMembers();
    }, []);

    // 2. 멤버 선택 시 세부 정보 및 날씨 가져오기
    useEffect(() => {
        if (!selectedUsername) return;

        const fetchMemberInfo = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/members/${selectedUsername}`);
                const detail = response.data;
                setMemberDetail(detail);
                fetchWeather(detail.location, detail.style, detail.gender);
            } catch (err) {
                console.error("멤버 상세 정보 로드 실패:", err);
            }
        };
        fetchMemberInfo();
    }, [selectedUsername]);

    return (
        <div className="flex flex-col md:flex-row h-screen bg-[#fafaf9] text-slate-900 font-serif overflow-hidden">
            {/* Sidebar / Archive Navigator */}
            <aside className="w-full md:w-72 bg-white border-r border-slate-200 p-8 flex flex-col h-full sticky top-0 z-10">
                <div className="mb-6">
                    <span className="text-[10px] font-sans font-black uppercase tracking-[0.4em] text-slate-400 block mb-2">Volume 01 / Archive</span>
                    <h2 className="text-3xl font-black mb-4 tracking-tighter uppercase leading-[0.85] border-b-4 border-black pb-4">
                        Fashion<br />Intelligence
                    </h2>
                </div>

                <div className="space-y-4 flex-1">
                    <div className="group">
                        <label className="text-[10px] font-sans font-bold uppercase tracking-widest text-slate-500 mb-2 block group-hover:text-black transition-colors">Select Subject</label>
                        <div className="relative">
                            <select
                                value={selectedUsername}
                                onChange={(e) => setSelectedUsername(e.target.value)}
                                className="w-full bg-slate-50 border-2 border-slate-100 rounded-none py-3 px-4 font-sans appearance-none focus:outline-none focus:border-black transition-all cursor-pointer text-xs font-bold tracking-tight"
                            >
                                {listLoading ? (
                                    <option>Loading Database...</option>
                                ) : (
                                    members.map(m => (
                                        <option key={m.username || m.id} value={m.username || m.id}>{m.name}</option>
                                    ))
                                )}
                            </select>
                            <div className="pointer-events-none absolute inset-y-0 right-3 flex items-center text-slate-900">
                                <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                    <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div className="pt-4 border-t border-slate-100 mt-4">
                        <p className="text-[11px] font-sans text-slate-400 leading-relaxed italic">
                            Bespoke aesthetic recommendations synthesized from real-time meteorological data.
                        </p>
                    </div>
                </div>

                <div className="mt-4 pt-4 border-t border-slate-200">
                    <div className="flex justify-between items-end">
                        <div className="space-y-1">
                            <span className="block text-[9px] font-bold font-sans uppercase text-slate-400">© 2024 AI Fashion Lab.</span>
                        </div>
                        <span className="text-xl font-black italic">01</span>
                    </div>
                </div>
            </aside>

            {/* Main Content / The Page */}
            <main className="flex-1 p-6 md:p-10 h-full overflow-hidden bg-white/50 backdrop-blur-sm">
                {memberDetail ? (
                    <div className="max-w-6xl mx-auto h-full flex flex-col animate-in fade-in slide-in-from-right-12 duration-1000">
                        {/* Hero Header */}
                        <header className="mb-6 grid grid-cols-1 md:grid-cols-12 gap-6 items-end border-b border-black pb-6">
                            <div className="md:col-span-9">
                                <span className="inline-block px-2 py-0.5 bg-black text-white text-[9px] font-sans font-black uppercase tracking-widest mb-3">Editorial Feature</span>
                                <h1 className="text-5xl md:text-6xl font-black tracking-tighter leading-[0.8] uppercase mb-4">
                                    {memberDetail.name}
                                </h1>
                                <div className="flex items-center gap-4">
                                    <div className="h-px w-12 bg-black"></div>
                                    <p className="text-lg text-slate-600 font-serif italic">
                                        The {memberDetail.role}
                                    </p>
                                </div>
                            </div>
                            <div className="md:col-span-3 text-left md:text-right">
                                {weatherLoading ? (
                                    <div className="space-y-1 animate-pulse">
                                        <div className="h-10 bg-slate-100 w-20 ml-auto"></div>
                                        <div className="h-3 bg-slate-100 w-28 ml-auto"></div>
                                    </div>
                                ) : (
                                    <div className="flex flex-col md:items-end">
                                        <span className="text-5xl font-sans font-black tracking-tighter">{currentTemp}°</span>
                                        <span className="text-[10px] font-sans font-black uppercase tracking-widest mt-1">{memberDetail.location}</span>
                                    </div>
                                )}
                            </div>
                        </header>

                        {/* Content Grid */}
                        <section className="grid grid-cols-1 lg:grid-cols-12 gap-x-8 gap-y-6 flex-1 min-h-0 items-stretch">
                            {/* Portrait (Left - Row 1) */}
                            <div className="lg:col-span-4 flex flex-col min-h-0">
                                <div className="flex-1 bg-slate-100 border-4 border-black relative group shadow-xl overflow-hidden">
                                    <div className="absolute inset-2 border border-white/20 z-10"></div>
                                    <div className="absolute inset-0 bg-gradient-to-br from-slate-200 to-white flex items-center justify-center">
                                        <span className="text-slate-200 font-black text-6xl -rotate-45 uppercase opacity-30 select-none">Portrait</span>
                                    </div>
                                    {memberDetail.imageUrl && (
                                        <img src={memberDetail.imageUrl} alt={memberDetail.name} className="absolute inset-0 w-full h-full object-cover grayscale mix-blend-multiply opacity-80 group-hover:grayscale-0 group-hover:opacity-100 group-hover:mix-blend-normal transition-all duration-700" />
                                    )}
                                </div>
                            </div>

                            {/* AI Recommendation (Right - Row 1 & 2 Span) */}
                            <div className="lg:col-span-8 lg:row-span-2 flex flex-col min-h-0">
                                <div className="relative flex-1 min-h-0 flex flex-col">
                                    <span className="absolute -top-6 -left-4 text-7xl font-black text-slate-50 select-none z-[-1]">AI</span>
                                    <div className="bg-white p-6 md:p-8 border-4 border-black shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] flex flex-col h-4/5 overflow-hidden">
                                        <h3 className="text-[10px] font-sans font-black uppercase tracking-[0.4em] mb-4 flex items-center gap-4 border-b border-slate-100 pb-4">
                                            날씨에 따른 추천의상
                                        </h3>

                                        <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
                                            {weatherLoading ? (
                                                <div className="space-y-3">
                                                    <div className="h-6 bg-slate-100 animate-pulse w-full"></div>
                                                    <div className="h-6 bg-slate-100 animate-pulse w-5/6"></div>
                                                    <div className="h-6 bg-slate-100 animate-pulse w-4/6"></div>
                                                </div>
                                            ) : (
                                                <div className="relative pt-2">
                                                    <span className="text-3xl text-slate-100 absolute -top-1 -left-2 font-serif select-none">“</span>
                                                    <p className="text-sm leading-[1.5] text-slate-800 font-serif font-medium italic relative z-10 text-balance">
                                                        {aiRecommendation}
                                                    </p>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Style/Gender Bar (Left - Row 2) */}
                            <div className="lg:col-span-4">
                                <div className="grid grid-cols-2 gap-px bg-slate-200 border border-slate-200">
                                    <div className="bg-white p-3">
                                        <span className="block text-[8px] font-sans font-black uppercase text-slate-400 mb-1">Style</span>
                                        <span className="text-xs font-bold font-sans uppercase tracking-tight">{memberDetail.style}</span>
                                    </div>
                                    <div className="bg-white p-3">
                                        <span className="block text-[8px] font-sans font-black uppercase text-slate-400 mb-1">Gender</span>
                                        <span className="text-xs font-bold font-sans uppercase tracking-tight">{memberDetail.gender}</span>
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                ) : (
                    <div className="flex h-full items-center justify-center flex-col gap-6 opacity-20">
                        <div className="text-8xl font-black tracking-tighter uppercase">Select</div>
                        <p className="font-sans font-black tracking-[0.2em] uppercase text-[9px]">Select a subject from the archive</p>
                    </div>
                )}
            </main>
        </div>
    );
}
