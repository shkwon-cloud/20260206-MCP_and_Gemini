// src/pages/TeamPage.tsx
import { useTeam } from '../hooks/useTeam';
import TeamCard from '../components/TeamCard';
import FilterSection from '../components/FilterSection';

import WeatherWidget from '../components/WeatherWidget';


const Team = () => {
    // 소스코드에 포함된 자체 정보를 사용하여 팀원 목록을 표시합니다.
    const { members, onlyOnline, toggleFilter, loading, error } = useTeam();

    if (loading) return <div className="py-20 text-center text-slate-500">Loading members...</div>;
    if (error) return <div className="py-20 text-center text-red-500">{error}</div>;

    return (
        <div className="space-y-12 animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="text-center space-y-4 max-w-2xl mx-auto">
                <h2 className="text-4xl md:text-5xl font-black tracking-tight text-slate-900">Our Experts</h2>
                <p className="text-slate-400 text-lg">
                    Meet Alex and Sarah — our world-class professionals.
                </p>
            </div>

            <FilterSection onlyOnline={onlyOnline} onToggle={toggleFilter} />

            {members.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
                    {members.map((member) => (
                        <TeamCard key={member.id} member={member} />
                    ))}
                </div>
            ) : (
                <div className="py-20 text-center space-y-4">
                    <div className="text-slate-300 text-6xl">∅</div>
                    <p className="text-slate-500 font-medium text-lg">No online members found at the moment.</p>
                </div>
            )}

            {/* 여기에도 부착! */}
            <WeatherWidget />

        </div>
    );
};

export default Team;
