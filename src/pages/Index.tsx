
import Navigation from "@/components/Navigation";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { CheckIcon, ShieldCheckIcon, ClockIcon, HeartIcon, BrainIcon } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import ContactForm from "@/components/ContactForm";

const Index = () => {
  return (
    <div className="min-h-screen bg-[#f5f5eb]">
      <Navigation />
      
      {/* Hero Section */}
      <section className="relative py-20 bg-[#e1ebe7]">
        <div className="container max-w-6xl mx-auto px-4">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-serif mb-6">Paw-sitive Insights</h1>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Transforming dog images into health insights. Know your pup's ailments with a click!
            </p>
            <Link to="/diagnosis">
              <Button className="bg-[#d1ded9] hover:bg-[#c1cec9] text-black border-0 px-8 py-6 text-lg">
                Start Now
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="py-20">
        <div className="container max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-serif text-center mb-12">Why Choose Us?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="p-6 bg-white/50 border-0">
                <h3 className="text-xl font-semibold mb-4">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="py-20 bg-[#e1ebe7]">
        <div className="container max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-serif text-center mb-12">Get Started Now</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <div key={index} className="text-center">
                <div className={`w-16 h-16 mx-auto mb-4 rounded-lg flex items-center justify-center ${step.bgColor}`}>
                  {step.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
                <p className="text-gray-600">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20">
        <div className="container max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-serif text-center mb-12">Frequently Asked Questions</h2>
          <div className="max-w-3xl mx-auto">
            <Accordion type="single" collapsible>
              {faqs.map((faq, index) => (
                <AccordionItem key={index} value={`item-${index}`}>
                  <AccordionTrigger className="text-lg">{faq.question}</AccordionTrigger>
                  <AccordionContent>{faq.answer}</AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-20 bg-[#e1ebe7]">
        <div className="container max-w-6xl mx-auto px-4">
          <ContactForm />
        </div>
      </section>
    </div>
  );
};

const features = [
  {
    title: "Smart Analysis",
    description: "Our advanced model analyzes dog images to identify potential health issues. No more guessing games—just accurate insights!"
  },
  {
    title: "User-Friendly",
    description: "Our platform is designed for everyone. No PhD required—just upload a photo and let us do the magic!"
  },
  {
    title: "Community Support",
    description: "Join a community of dog lovers and health enthusiasts. Share experiences, tips, and a few laughs along the way!"
  }
];

const steps = [
  {
    title: "Upload Image",
    description: "Snap a pic of your dog and upload it. Easy peasy!",
    icon: <CheckIcon className="h-8 w-8 text-white" />,
    bgColor: "bg-[#9eb3ac]"
  },
  {
    title: "Receive Diagnosis",
    description: "Get instant feedback on your dog's health status.",
    icon: <BrainIcon className="h-8 w-8 text-white" />,
    bgColor: "bg-[#d4a373]"
  },
  {
    title: "Follow Recommendations",
    description: "Implement the suggested treatments and watch your pup thrive!",
    icon: <HeartIcon className="h-8 w-8 text-white" />,
    bgColor: "bg-[#6b705c]"
  }
];

const faqs = [
  {
    question: "How does the diagnosis work?",
    answer: "Our AI model analyzes images of your dog to identify potential health issues by comparing visual patterns with our extensive database of known conditions."
  },
  {
    question: "Is it accurate?",
    answer: "While our system provides highly accurate insights, it's designed to be a supportive tool and should not replace professional veterinary care."
  },
  {
    question: "Can I trust the treatment suggestions?",
    answer: "Absolutely! Suggestions are based on expert veterinary advice. However, always consult with your vet before starting any new treatment."
  }
];

export default Index;
