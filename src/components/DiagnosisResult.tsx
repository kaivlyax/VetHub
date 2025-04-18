
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertCircle } from "lucide-react";

export interface DiagnosisInfo {
  disease: string;
  confidence: number;
  symptoms: string[];
  treatment: string;
}

interface DiagnosisResultProps {
  diagnosis: DiagnosisInfo | null;
  isLoading: boolean;
}

const DiagnosisResult = ({ diagnosis, isLoading }: DiagnosisResultProps) => {
  if (isLoading) {
    return (
      <Card className="w-full mt-6">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg text-center">Analyzing Image...</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center py-6">
            <div className="h-8 w-8 rounded-full border-t-2 border-primary animate-spin mb-4"></div>
            <p className="text-muted-foreground">This may take a few moments</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!diagnosis) return null;

  return (
    <Card className="w-full mt-6">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl">Diagnosis Result</CardTitle>
          <Badge variant={diagnosis.confidence > 0.7 ? "default" : "secondary"}>
            {Math.round(diagnosis.confidence * 100)}% Confidence
          </Badge>
        </div>
        <CardDescription>
          Based on the uploaded image
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-primary mb-2">Disease Identified</h3>
            <p className="text-xl">{diagnosis.disease}</p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-primary mb-2">Common Symptoms</h3>
            <ul className="list-disc pl-5 space-y-1">
              {diagnosis.symptoms.map((symptom, index) => (
                <li key={index}>{symptom}</li>
              ))}
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-primary mb-2">Treatment Suggestions</h3>
            <p>{diagnosis.treatment}</p>
          </div>
          
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mt-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <AlertCircle className="h-5 w-5 text-yellow-400" />
              </div>
              <div className="ml-3">
                <p className="text-sm text-yellow-700">
                  This is an automated diagnosis and should not replace professional medical advice. 
                  Please consult a healthcare professional for proper diagnosis and treatment.
                </p>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default DiagnosisResult;
