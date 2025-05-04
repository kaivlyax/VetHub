
import Navigation from "@/components/Navigation";
import ImageUploader from "@/components/ImageUploader";
import DiagnosisResult from "@/components/DiagnosisResult";
import { useState } from "react";
import { classifyImage } from "@/lib/modelService";
import { Brain, Activity } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

const Diagnosis = () => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [diagnosis, setDiagnosis] = useState<any | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const { toast } = useToast();

  const handleImageUpload = (file: File, url: string) => {
    setImageFile(file);
    setImageUrl(url);
    setDiagnosis(null);
  };

  const analyzeImage = async () => {
    if (!imageUrl) return;

    try {
      setIsAnalyzing(true);
      
      const result = await classifyImage(imageUrl);
      setDiagnosis(result);
      
      toast({
        title: "Analysis Complete",
        description: `Detected: ${result.disease} with ${Math.round(result.confidence * 100)}% confidence`,
      });
    } catch (err) {
      console.error(err);
      toast({
        title: "Analysis Failed",
        description: "Something went wrong during the image analysis.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-muted to-background">
      <Navigation />
      <div className="container px-4 py-8 mx-auto max-w-6xl">
        <div className="grid md:grid-cols-2 gap-8 items-start">
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm p-6 border">
              <h2 className="text-2xl font-semibold mb-4 flex items-center">
                <Brain className="mr-2 h-6 w-6 text-primary" />
                Dog Skin Condition Analysis
              </h2>
              
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
            </div>
          </div>

          <div>
            <DiagnosisResult diagnosis={diagnosis} isLoading={isAnalyzing} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Diagnosis;
