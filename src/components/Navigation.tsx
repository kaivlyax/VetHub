
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

const Navigation = () => {
  return (
    <header className="border-b bg-[#f5f5eb] backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6">
          <Link to="/" className="text-2xl font-serif">PawDiagnosis</Link>
          <nav className="hidden md:flex gap-6">
            <Link to="/" className="text-lg hover:text-primary transition-colors">Home</Link>
            <Link to="/about" className="text-lg hover:text-primary transition-colors">About</Link>
            <Link to="/contact" className="text-lg hover:text-primary transition-colors">Contact</Link>
          </nav>
        </div>
        <Link to="/register">
          <Button variant="outline" className="bg-[#d1ded9] hover:bg-[#c1cec9] border-0 text-lg font-serif">
            Get Started
          </Button>
        </Link>
      </div>
    </header>
  );
};

export default Navigation;
