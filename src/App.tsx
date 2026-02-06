// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Team from './pages/Team';
import WeatherPage from './pages/WeatherPage';
import FashionPage from './pages/FashionPage'; // 임포트 추가
import StylistPage from './pages/StylistPage'; // AI 스타일리스트 페이지 임포트


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="team" element={<Team />} />
          {/* 날씨 페이지 경로 추가 */}
          <Route path="weather" element={<WeatherPage />} />
          {/* 패션 추천 페이지 경로 추가 */}
          <Route path="fashion" element={<FashionPage />} />
          {/* AI 스타일리스트 페이지 경로 추가 */}
          <Route path="stylist" element={<StylistPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
