
// Define disease database for dog skin conditions
const diseaseDatabase = {
  "Allergy": {
    symptoms: [
      "Itching and scratching",
      "Red, inflamed skin",
      "Hair loss",
      "Skin rash or hives",
      "Recurring ear infections",
      "Paw licking or chewing",
      "Rubbing face on surfaces"
    ],
    treatment: "Treatment typically involves identifying and eliminating the allergen if possible. Medications like antihistamines, steroids, or immunotherapy may be prescribed. Special shampoos and dietary changes can also help manage symptoms. Regular bathing with hypoallergenic shampoos can provide relief."
  },
  "Infection": {
    symptoms: [
      "Redness and swelling",
      "Pus or discharge",
      "Foul odor",
      "Excessive scratching or licking of affected area",
      "Pain when touched",
      "Crusty or scabby skin",
      "Hot spots (acute moist dermatitis)"
    ],
    treatment: "Bacterial infections usually require antibiotics, either topical, oral, or both. Fungal infections need antifungal medications. The affected area should be kept clean and dry. In some cases, medicated shampoos or sprays may be recommended. Complete the full course of medication even if symptoms improve."
  },
  "Mange": {
    symptoms: [
      "Intense itching",
      "Hair loss in patches or widespread",
      "Red, inflamed skin",
      "Crusty or scaly skin",
      "Sores and lesions",
      "Thickened skin (in chronic cases)",
      "Secondary infections"
    ],
    treatment: "Treatment depends on the type of mange (demodectic or sarcoptic). Medications like ivermectin, milbemycin, or selamectin may be prescribed. Medicated dips or shampoos containing benzoyl peroxide can help. The living environment needs to be thoroughly cleaned to prevent reinfestation."
  },
  "Normal": {
    symptoms: [
      "No visible skin abnormalities",
      "Regular coat appearance",
      "No excessive scratching or biting",
      "Skin is supple and elastic",
      "No redness or inflammation",
      "No unusual odor",
      "Normal shedding patterns"
    ],
    treatment: "Regular grooming, balanced diet, and routine veterinary check-ups are recommended to maintain healthy skin and coat. Use dog-appropriate shampoos when bathing. Monitor for any changes in skin condition."
  },
  "Tumor": {
    symptoms: [
      "Visible lump or growth on or under the skin",
      "Change in size, shape, or color of existing growth",
      "Sores that don't heal",
      "Bleeding or discharge from a growth",
      "Pain or tenderness in affected area",
      "Loss of appetite or weight loss",
      "Difficulty breathing or swallowing (if tumor affects these areas)"
    ],
    treatment: "Treatment depends on the type, size, and location of the tumor. Options include surgical removal, chemotherapy, radiation therapy, or a combination approach. Early detection and treatment significantly improve the prognosis. Regular follow-up examinations are essential to monitor for recurrence."
  }
};

// Interface for our diagnosis result
export interface DiagnosisResult {
  disease: string;
  confidence: number;
  symptoms: string[];
  treatment: string;
}

// Function to classify an uploaded image using the Flask backend
export const classifyImage = async (imageDataUrl: string): Promise<DiagnosisResult> => {
  try {
    // Convert data URL to blob
    const imageBlob = await fetch(imageDataUrl).then(r => r.blob());
    
    // Create form data for API request
    const formData = new FormData();
    formData.append('image', imageBlob, 'image.jpg');
    
    // Send to backend API
    console.log("Sending image to backend for classification...");
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
    }
    
    // Parse the JSON response
    const data = await response.json();
    console.log("Received classification result:", data);
    
    // Match the disease with our database
    const diseaseName = data.disease;
    const diseaseInfo = diseaseDatabase[diseaseName as keyof typeof diseaseDatabase];
    
    if (!diseaseInfo) {
      throw new Error(`Unknown disease: ${diseaseName}`);
    }
    
    return {
      disease: diseaseName,
      confidence: data.confidence,
      symptoms: diseaseInfo.symptoms,
      treatment: diseaseInfo.treatment
    };
  } catch (error) {
    console.error("Classification error:", error);
    throw new Error("Failed to classify image");
  }
};
