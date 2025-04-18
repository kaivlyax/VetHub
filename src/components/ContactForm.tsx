
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { useToast } from "@/components/ui/use-toast";

const ContactForm = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    message: ""
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    toast({
      title: "Message sent!",
      description: "We'll get back to you soon.",
    });
    setFormData({ name: "", email: "", phone: "", message: "" });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-4xl font-serif text-center mb-8">Get in Touch</h2>
      <p className="text-center mb-12 text-lg">Have questions? We're here to help!</p>
      
      <form onSubmit={handleSubmit} className="grid md:grid-cols-2 gap-6">
        <Input
          placeholder="Name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className="bg-white/80"
          required
        />
        <Input
          placeholder="Phone"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          className="bg-white/80"
          required
        />
        <Input
          placeholder="Email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          className="bg-white/80 md:col-span-2"
          required
        />
        <Textarea
          placeholder="Message"
          name="message"
          value={formData.message}
          onChange={handleChange}
          className="bg-white/80 md:col-span-2"
          rows={6}
          required
        />
        <Button 
          type="submit"
          className="bg-[#d1ded9] hover:bg-[#c1cec9] text-black md:col-span-2 py-6 text-lg"
        >
          Send Message
        </Button>
      </form>
    </div>
  );
};

export default ContactForm;
