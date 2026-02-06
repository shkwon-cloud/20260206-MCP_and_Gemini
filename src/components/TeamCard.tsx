// src/components/TeamCard.tsx
import type { TeamMember } from '../types/team.ts';

interface TeamCardProps {
    member: TeamMember;
}

const TeamCard = ({ member }: TeamCardProps) => {
    return (
        <div className="group relative bg-white border border-slate-200 rounded-2xl overflow-hidden hover:border-indigo-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-indigo-500/10">
            <div className="aspect-square bg-slate-100 overflow-hidden relative">
                <img
                    src={member.imageUrl}
                    alt={member.name}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className={`absolute top-4 right-4 w-3 h-3 rounded-full border-2 border-slate-900 ${member.isOnline ? 'bg-green-500' : 'bg-slate-500'}`} />
            </div>
            <div className="p-6 space-y-2">
                <div className="flex justify-between items-start">
                    <h3 className="text-xl font-semibold text-slate-900">{member.name}</h3>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full uppercase tracking-tighter ${member.isOnline ? 'bg-green-500/10 text-green-600' : 'bg-slate-100 text-slate-500'}`}>
                        {member.isOnline ? 'Online' : 'Offline'}
                    </span>
                </div>
                <p className="text-sm font-medium text-indigo-600 uppercase tracking-wider">{member.role}</p>
                <p className="text-sm text-slate-400 line-clamp-2">{member.bio}</p>
            </div>
        </div>
    );
};

export default TeamCard;
