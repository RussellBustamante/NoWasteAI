import React, { useState } from 'react';
import placeholder from './images/placeholder.png';
import foodimg from './food.png';


// Define the API key
const OPENAI_API_KEY = "API_KEY";

function App() {
  const [inputText, setInputText] = useState('');
  const [days, setDays] = useState(''); // New state for days input
  const [ppm, setPpm] = useState(''); // New state for ppm input
  const [image, setImage] = useState(placeholder); // Use a local placeholder image
  const [showAnalyzeButton, setShowAnalyzeButton] = useState(false);
  const [showFinalAnalysisButton, setShowFinalAnalysisButton] = useState(false);
  const [visionText, setVisionText] = useState(''); // Store vision API response for later use
  const [gptResponse, setGptResponse] = useState('');
  const [prompt1, setPrompt1] = useState('');
  const [scriptOutput, setScriptOutput] = useState('');

  const convertImageToBase64 = (imageUrl) => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = 'Anonymous';
      img.onload = () => {
        let canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        let ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        const dataURL = canvas.toDataURL("image/png");
        resolve(dataURL);
      };
      img.onerror = error => reject(error);
      img.src = imageUrl;
      if (img.complete || img.complete === undefined) {
        img.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
        img.src = imageUrl;
      }
    });
  };

  const handleCaptureImage = async () => {
    try {
        const response = await fetch('http://localhost:5000/run-script1', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                days: days,
                ppm: ppm,
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log("Received data from Python script:", data);
        
        setPrompt1(data.output);
        setShowAnalyzeButton(true);
        setPpm(data.ppm);
    } catch (error) {
        console.error('Error:', error);
    }
};

const handleSendData = async () => {
  const requestData = {
    days: days,
    ppm: ppm,
    prompt1: prompt1
  }

  try {
    const response = await fetch('http://localhost:5000/run-script1', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const data = await response.json();
    console.log("Received data from Python script:", data);
    setScriptOutput(data.output); // Update state with the script output
  } catch (error) {
    console.error('Error:', error);
    setScriptOutput("Error occurred while fetching data."); // Handle error by updating state
  }
};

  const handleFinalAnalysis = async () => {
    try {
      const gptResponse = await fetch('https://api.openai.com/v1/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
        },
        body: JSON.stringify({
          model: "text-davinci-003",
          prompt: visionText,
          max_tokens: 100,
        }),
      });

      if (!gptResponse.ok) {
        throw new Error('Network response was not ok from GPT API');
      }

      const gptData = await gptResponse.json();
      setGptResponse(gptData.choices[0].text);
      

    } catch (error) {
      console.error('Error:', error);
      setGptResponse("Failed to process the image or get a response.");
    }
  };


  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white shadow-xl rounded-lg p-6 w-full max-w-4xl">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex flex-col space-y-4">
            <textarea
              className="textarea textarea-bordered h-24"
              placeholder="Enter text here..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            ></textarea>
            <input
              type="text"
              className="input input-bordered"
              placeholder="Enter days..."
              value={days}
              onChange={(e) => setDays(e.target.value)}
            />
            <button
              className="btn btn-primary"
              onClick={handleCaptureImage}
            >
              Capture Image
            </button>
            {showAnalyzeButton && (
              <button
                className="btn btn-secondary mt-2"
                onClick={handleSendData}
              >
                Analyze Image
              </button>
            )}
            {showFinalAnalysisButton && (
              <button
                className="btn btn-success mt-2"
                onClick={handleFinalAnalysis}
              >
                Finalize Analysis
              </button>
            )}
          </div>
          <span id='here'>

          </span>
          <div className="flex flex-col items-center space-y-4">
          
            <textarea
              className="textarea textarea-bordered h-24 w-full"
              placeholder="API Response..."
              value={gptResponse}
              readOnly
            ></textarea>
            <img src={foodimg} alt="Dynamic" />
          </div>
          <div className="text-sm mt-4">{scriptOutput}</div>
        </div>
      </div>
    </div>
  );
}

export default App;
