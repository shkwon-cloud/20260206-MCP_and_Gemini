import { useState, useMemo } from 'react';
import type { TeamMember } from '../types/team.ts';

// main.py의 데이터를 프론트엔드 소스코드에 직접 포함
const STATIC_MEMBERS: TeamMember[] = [
    {
        "id": 1,
        "name": "Alex Rivera",
        "role": "Lead Architect",
        "bio": "Specializes in cloud infrastructure and distributed systems.",
        "imageUrl": "https://i.pravatar.cc/300?u=alex",
        "isOnline": true
    },
    {
        "id": 2,
        "name": "Sarah Chen",
        "role": "UI/UX Designer",
        "bio": "Passionate about creating intuitive and beautiful user interfaces.",
        "imageUrl": "https://i.pravatar.cc/300?u=sarah",
        "isOnline": false
    }
];

export const useTeam = () => {
    const [onlyOnline, setOnlyOnline] = useState(false);

    // 로딩과 에러 상태는 이제 더 이상 필요하지 않지만 인터페이스 유지를 위해 남겨둠
    const loading = false;
    const error = null;

    const filteredMembers = useMemo(() => {
        return onlyOnline
            ? STATIC_MEMBERS.filter(member => member.isOnline)
            : STATIC_MEMBERS;
    }, [onlyOnline]);

    const toggleFilter = () => setOnlyOnline(prev => !prev);

    return {
        members: filteredMembers,
        onlyOnline,
        toggleFilter,
        loading,
        error
    };
};
