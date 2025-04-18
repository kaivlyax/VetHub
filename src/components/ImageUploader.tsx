
import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Upload, Image as ImageIcon } from "lucide-react";

interface ImageUploaderProps {
  onImageUpload: (imageFile: File, imageUrl: string) => void;
}

const ImageUploader = ({ onImageUpload }: ImageUploaderProps) => {
  const [preview, setPreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    processFile(file);
  };

  const processFile = (file: File) => {
    // Check if file is an image
    if (!file.type.match('image.*')) {
      alert('Please upload an image file');
      return;
    }

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const result = e.target?.result as string;
      setPreview(result);
      onImageUpload(file, result);
    };
    reader.readAsDataURL(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      processFile(file);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <Card className={`p-6 w-full max-w-md mx-auto ${isDragging ? 'border-primary border-2' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div className="flex flex-col items-center justify-center gap-4">
        <input 
          type="file" 
          className="hidden" 
          accept="image/*" 
          onChange={handleFileChange}
          ref={fileInputRef}
        />
        
        {preview ? (
          <div className="w-full relative">
            <img src={preview} alt="Preview" className="w-full h-56 object-contain rounded-md" />
            <Button 
              variant="secondary" 
              size="sm" 
              className="mt-2 w-full"
              onClick={triggerFileInput}
            >
              Change Image
            </Button>
          </div>
        ) : (
          <div 
            className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center w-full cursor-pointer hover:bg-muted transition-colors"
            onClick={triggerFileInput}
          >
            <div className="flex flex-col items-center">
              <div className="p-3 rounded-full bg-primary/10 mb-3">
                <Upload className="h-8 w-8 text-primary" />
              </div>
              <h3 className="font-medium text-lg mb-1">Upload an image</h3>
              <p className="text-sm text-muted-foreground mb-3">
                Drag and drop or click to browse
              </p>
              <Button>
                <ImageIcon className="h-4 w-4 mr-2" />
                Select Image
              </Button>
            </div>
          </div>
        )}
      </div>
    </Card>
  );
};

export default ImageUploader;
