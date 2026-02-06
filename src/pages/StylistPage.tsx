import { useState } from 'react';
import axios from 'axios';

export default function StylistPage() {
    const [query, setQuery] = useState('');
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);

    const askAgent = async () => {
        if (!query) return;

        setLoading(true);
        setAnswer('');

        try {
            // ⭐ 8004번 포트로 요청을 보냅니다!
            const res = await axios.post('http://localhost:8004/chat', {
                query: query
            });

            setAnswer(res.data.response);
        } catch (error) {
            console.error(error);
            setAnswer('AI 스타일리스트 연결에 실패했습니다. 😅');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8 max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold mb-4">🤖 AI 스타일리스트</h2>

            <div className="flex gap-2 mb-4">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="예: ideabong에게 오늘 날씨에 맞춰 옷 추천해줘"
                    className="flex-1 p-2 border rounded"
                />
                <button
                    onClick={askAgent}
                    disabled={loading}
                    className="bg-purple-600 text-white px-4 py-2 rounded disabled:bg-gray-400"
                >
                    {loading ? '생각 중...' : '물어보기'}
                </button>
            </div>

            {answer && (
                <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
                    <h3 className="font-bold text-purple-700 mb-2">추천 결과:</h3>
                    <p className="whitespace-pre-wrap leading-relaxed text-gray-700">{answer}</p>
                </div>
            )}
        </div>
    );
}