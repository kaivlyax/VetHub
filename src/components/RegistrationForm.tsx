
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";

interface RegistrationData {
  name: string;
  email: string;
  phone: string;
}

const RegistrationForm = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [formData, setFormData] = useState<RegistrationData>({
    name: "",
    email: "",
    phone: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Store user data in localStorage for demo purposes
    localStorage.setItem("userData", JSON.stringify(formData));
    toast({
      title: "Registration successful!",
      description: "You will be redirected to the diagnosis page.",
    });
    // Redirect to diagnosis page after registration
    setTimeout(() => navigate("/diagnosis"), 1500);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Register to Use Our Service</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Full Name</Label>
            <Input
              id="name"
              name="name"
              required
              placeholder="Enter your full name"
              value={formData.name}
              onChange={handleChange}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              required
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="phone">Phone Number</Label>
            <Input
              id="phone"
              name="phone"
              type="tel"
              required
              placeholder="Enter your phone number"
              value={formData.phone}
              onChange={handleChange}
            />
          </div>
          <Button type="submit" className="w-full">
            Register & Continue
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default RegistrationForm;
