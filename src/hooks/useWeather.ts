// src/hooks/useWeather.ts
import { useState } from 'react';
import axios from 'axios';

// 1. Gemini SDK 불러오기
import { GoogleGenerativeAI } from "@google/generative-ai";

export default function useWeather() {
    const [currentTemp, setCurrentTemp] = useState<number | null>(null);
    const [hourlyTemps, setHourlyTemps] = useState<number[]>([]);
    const [aiRecommendation, setAiRecommendation] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // ============================================================
    // 함수 A-1: 지오코딩 (getGeoLocation)
    // 역할: 도시 이름을 위도/경도로 변환
    // ============================================================
    const getGeoLocation = async (location: string) => {
        const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(location)}&count=1&language=ko&format=json`;
        const response = await axios.get(geoUrl);
        if (!response.data.results || response.data.results.length === 0) {
            throw new Error("위치 정보를 찾을 수 없습니다.");
        }
        return response.data.results[0];
    };

    // ============================================================
    // 함수 A-2: 데이터 심부름꾼 (getWeatherData)
    // 역할: 위도/경도를 받아 날씨 데이터를 가져옴
    // ============================================================
    const getWeatherData = async (lat: number, lon: number) => {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=temperature_2m`;
        const response = await axios.get(url);
        return response.data;
    };

    // ============================================================
    // 함수 C: AI 스타일리스트 (getAiRecommendation)
    // 역할: 날씨, 스타일, 성별을 모두 고려해 Gemini에게 옷차림을 물어봄
    // ============================================================
    const getAiRecommendation = async (temp: number, location: string, style?: string, gender?: string) => {
        try {
            const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GEMINI_KEY || "");
            const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash-lite" });

            let prompt = `현재 ${location}의 기온이 섭씨 ${temp}도아. `;
            if (style && gender) {
                prompt += `평소 ${style} 스타일을 선호하는 ${gender}에게 어울리는 구체적인 오늘의 코디를 추천해줘. `;
            } else {
                prompt += `이 날씨에 어울리는 적절한 옷차림을 추천해줘. `;
            }
            prompt += `패션 잡지 에디터처럼 전문적이면서도 세련된 말투로 3~4문장 정도로 정중하게 추천해줘.`;

            const result = await model.generateContent(prompt);
            const response = await result.response;
            const text = response.text();

            setAiRecommendation(text);
        } catch (error: any) {
            console.error("--- AI 추천 시스템 상세 에러 ---");
            console.error("에러 타입:", error?.name);
            console.error("에러 메시지:", error?.message);
            console.error("상세 정보:", error);

            if (error?.message?.includes("API_KEY_INVALID")) {
                setAiRecommendation("API 키가 올바르지 않습니다. 환경 변수를 확인해주세요. 🔑");
            } else if (error?.message?.includes("quota")) {
                setAiRecommendation("API 사용량이 초과되었습니다. 잠시 후 다시 시도해주세요. ⏳");
            } else {
                setAiRecommendation(`AI 추천 중 오류가 발생했습니다: ${error?.message || "알 수 없는 에러"} 😅`);
            }
        }
    };

    // ============================================================
    // 함수 B: 화면 관리자 (fetchWeather)
    // ============================================================
    const fetchWeather = async (locationName: string = "Seoul", style?: string, gender?: string) => {
        try {
            setLoading(true);
            setError(null);
            setAiRecommendation(null);

            // 1. 위치 정보(위도/경도) 가져오기
            const geo = await getGeoLocation(locationName);

            // 2. 날씨 데이터 가져오기
            const data = await getWeatherData(geo.latitude, geo.longitude);

            // 3. 상태 업데이트
            setCurrentTemp(data.current_weather.temperature);
            setHourlyTemps(data.hourly.temperature_2m);

            // 4. AI 추천 의뢰
            getAiRecommendation(data.current_weather.temperature, locationName, style, gender);

        } catch (err: any) {
            setError(err.message || "날씨 데이터를 가져오는데 실패했습니다.");
        } finally {
            setLoading(false);
        }
    };

    return { currentTemp, hourlyTemps, aiRecommendation, loading, error, fetchWeather };
}
