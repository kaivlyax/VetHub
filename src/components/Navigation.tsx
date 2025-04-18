
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Link } from "react-router-dom";

const Navigation = () => {
  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <Tabs defaultValue="home" className="w-full">
          <TabsList className="w-full justify-start">
            <TabsTrigger value="home" asChild>
              <Link to="/">Home</Link>
            </TabsTrigger>
            <TabsTrigger value="about" asChild>
              <Link to="/about">About Us</Link>
            </TabsTrigger>
            <TabsTrigger value="services" asChild>
              <Link to="/services">Our Services</Link>
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </div>
    </header>
  );
};

export default Navigation;
