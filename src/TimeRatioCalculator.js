import React, { useState } from "react";

export default function TimeRatioCalculator() {
  const [totalTime, setTotalTime] = useState(0);
  const [ratios, setRatios] = useState(["", ""]);
  const [results, setResults] = useState([]);

  const handleRatioChange = (index, value) => {
    const newRatios = [...ratios];
    newRatios[index] = value;
    setRatios(newRatios);
  };

  const addRatio = () => {
    setRatios([...ratios, ""]);
  };

  const toHHMM = (minutes) => {
    const h = Math.floor(minutes / 60);
    const m = Math.round(minutes % 60);
    return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}`;
  };

  const calculate = () => {
    const ratioNumbers = ratios.map((r) => parseFloat(r) || 0);
    const totalRatio = ratioNumbers.reduce((a, b) => a + b, 0);

    if (totalRatio === 0 || totalTime <= 0) {
      setResults([]);
      return;
    }

    const calculated = ratioNumbers.map((r) => {
      const minutes = (r / totalRatio) * totalTime;
      return { raw: minutes, hhmm: toHHMM(minutes) };
    });
    setResults(calculated);
  };

  const copyToClipboard = () => {
    if (results.length === 0) return;
    const text = results
      .map((res) => res.hhmm) 
      .join("\n");
    navigator.clipboard.writeText(text).then(() => {
      alert("時間をコピーしました！");
    });
  };

  const copySingleTime = (time) => {
    navigator.clipboard.writeText(time).then(() => {
      alert("時間をコピーしました！");
    });
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">⏱ 時間割合計算ツール</h1>
      <div className="bg-white shadow-md rounded-2xl p-6 w-full max-w-lg">
        <label className="block mb-4">
          <span className="font-medium">全体の時間 (分)</span>
          <input
            type="number"
            className="mt-1 p-2 w-full border rounded"
            value={totalTime}
            onChange={(e) => setTotalTime(Number(e.target.value))}
          />
        </label>

        <h2 className="font-medium mb-2">割合のセット</h2>
        {ratios.map((ratio, index) => (
          <div key={index} className="flex gap-2 mb-2">
            <input
              type="number"
              className="p-2 border rounded flex-1"
              placeholder={`割合 ${index + 1}`}
              value={ratio}
              onChange={(e) => handleRatioChange(index, e.target.value)}
            />
          </div>
        ))}

        <button
          onClick={addRatio}
          className="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600 mb-4"
        >
          ➕ 割合を追加
        </button>

        <div className="flex gap-2">
          <button
            onClick={calculate}
            className="flex-1 px-4 py-2 bg-green-500 text-white rounded shadow hover:bg-green-600"
          >
            計算する
          </button>
          {results.length > 0 && (
            <button
              onClick={copyToClipboard}
              className="flex-1 px-4 py-2 bg-gray-600 text-white rounded shadow hover:bg-gray-700"
            >
              全時間をコピー
            </button>
          )}
        </div>

        {results.length > 0 && (
          <div className="mt-6">
            <h3 className="font-semibold mb-4">📊 計算結果</h3>
            <div className="space-y-3">
              {results.map((res, i) => (
                <div key={i} className="bg-gray-50 p-4 rounded-lg border">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-medium text-gray-700">作業{i + 1}</div>
                      <div className="text-sm text-gray-600">
                        割合 {ratios[i]} → {res.hhmm} (約 {res.raw.toFixed(2)} 分)
                      </div>
                    </div>
                    <button
                      onClick={() => copySingleTime(res.hhmm)}
                      className="px-3 py-1 bg-blue-500 text-white text-sm rounded shadow hover:bg-blue-600"
                    >
                      時間をコピー
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}