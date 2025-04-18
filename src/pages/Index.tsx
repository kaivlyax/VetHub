
import Navigation from "@/components/Navigation";
import RegistrationForm from "@/components/RegistrationForm";
import { MicroscopeIcon, Brain, Activity } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-muted to-background">
      <Navigation />
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
            Advanced medical image analysis powered by AI for accurate disease classification
          </p>
        </header>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold flex items-center">
              <Brain className="mr-2 h-6 w-6 text-primary" />
              Our Goals
            </h2>
            <div className="space-y-4">
              <p className="text-muted-foreground">
                We aim to revolutionize medical diagnosis through advanced AI technology,
                making it more accessible, accurate, and efficient for healthcare professionals.
              </p>
              <ul className="space-y-2 list-disc pl-5 text-muted-foreground">
                <li>Quick and accurate disease classification</li>
                <li>Comprehensive symptom analysis</li>
                <li>Evidence-based treatment suggestions</li>
                <li>Support for healthcare professionals</li>
              </ul>
            </div>
          </div>
          
          <div>
            <RegistrationForm />
          </div>
        </div>

        <footer className="text-center text-sm text-muted-foreground mt-16">
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
