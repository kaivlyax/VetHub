
import { useState } from "react";
import { classifyImage } from "@/lib/modelService";
import ImageUploader from "@/components/ImageUploader";
import DiagnosisResult, { DiagnosisInfo } from "@/components/DiagnosisResult";
import { Button } from "@/components/ui/button";
import { MicroscopeIcon, Brain, Activity } from "lucide-react";

const Index = () => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [diagnosis, setDiagnosis] = useState<DiagnosisInfo | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageUpload = (file: File, url: string) => {
    setImageFile(file);
    setImageUrl(url);
    setDiagnosis(null);
    setError(null);
  };

  const analyzeImage = async () => {
    if (!imageUrl) return;

    try {
      setIsAnalyzing(true);
      setError(null);
      
      const result = await classifyImage(imageUrl);
      setDiagnosis(result);
    } catch (err) {
      setError("An error occurred during image analysis. Please try again.");
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-muted to-background">
      <div className="container px-4 py-8 mx-auto max-w-6xl">
        <header className="text-center mb-12">
          <div className="flex justify-center mb-4">
            <div className="p-3 rounded-full bg-primary/10">
              <MicroscopeIcon className="h-12 w-12 text-primary" />
            </div>
          </div>
          <h1 className="text-4xl font-bold mb-3 bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent">
            Medical Image Insight
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Upload medical images for instant disease classification, symptoms identification, and treatment suggestions powered by AI.
          </p>
        </header>

        <div className="grid md:grid-cols-2 gap-8 items-start">
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm p-6 border">
              <h2 className="text-2xl font-semibold mb-4 flex items-center">
                <Brain className="mr-2 h-6 w-6 text-primary" />
                Image Analysis
              </h2>
              <p className="text-muted-foreground mb-6">
                Upload a clear medical image for accurate disease diagnosis.
              </p>
              
              <ImageUploader onImageUpload={handleImageUpload} />
              
              {imageUrl && (
                <div className="mt-6">
                  <Button 
                    className="w-full" 
                    size="lg"
                    onClick={analyzeImage}
                    disabled={isAnalyzing}
                  >
                    <Activity className="mr-2 h-5 w-5" />
                    {isAnalyzing ? "Analyzing..." : "Analyze Image"}
                  </Button>
                </div>
              )}

              {error && (
                <div className="mt-4 p-3 bg-destructive/10 border border-destructive/20 text-destructive rounded-md text-sm">
                  {error}
                </div>
              )}
            </div>

            <div className="bg-white rounded-lg p-6 border shadow-sm">
              <h3 className="font-medium text-lg mb-2">How it works</h3>
              <ol className="space-y-2 list-decimal pl-5 text-muted-foreground">
                <li>Upload a clear medical image</li>
                <li>Our AI analyzes the image using your trained model</li>
                <li>View disease identification, symptoms, and treatment options</li>
                <li>Consult a healthcare professional for confirmation</li>
              </ol>
            </div>
          </div>

          <div>
            <DiagnosisResult diagnosis={diagnosis} isLoading={isAnalyzing} />
            
            {!diagnosis && !isAnalyzing && (
              <div className="bg-white rounded-lg p-6 border shadow-sm">
                <h2 className="text-xl font-semibold mb-4">Ready for Diagnosis</h2>
                <p className="text-muted-foreground">
                  Upload and analyze a medical image to receive an instant diagnosis with detailed information about potential conditions, symptoms, and treatment options.
                </p>
                <div className="mt-6 flex flex-col gap-3">
                  <div className="flex items-start">
                    <div className="bg-primary/10 p-2 rounded-full mr-3">
                      <Activity className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-medium">Accurate Disease Detection</h3>
                      <p className="text-sm text-muted-foreground">Advanced AI models trained on medical datasets</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <div className="bg-primary/10 p-2 rounded-full mr-3">
                      <Brain className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-medium">Comprehensive Information</h3>
                      <p className="text-sm text-muted-foreground">Get symptoms and treatment options in seconds</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        <footer className="mt-16 text-center text-sm text-muted-foreground">
          <p className="mb-2">
            This tool is for educational purposes only and not a substitute for professional medical advice.
          </p>
          <p>
            © {new Date().getFullYear()} Medical Image Insight — Powered by AI
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Index;
