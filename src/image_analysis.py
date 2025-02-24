import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops

class ImageAnalyzer:
    def __init__(self, image):
        self.image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
    def analyze_colors(self):
        """Extract color features from the image"""
        colors = ('b', 'g', 'r')
        color_stats = {}
        
        for i, col in enumerate(colors):
            hist = cv2.calcHist([self.image], [i], None, [256], [0, 256])
            color_stats[col] = {
                'mean': np.mean(self.image[:,:,i]),
                'std': np.std(self.image[:,:,i]),
                'dominant_values': np.argmax(hist)
            }
        return color_stats

    def analyze_texture(self):
        """Analyze texture features"""
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        glcm = graycomatrix(gray, [1], [0], symmetric=True, normed=True)
        
        return {
            'contrast': graycoprops(glcm, 'contrast')[0,0],
            'homogeneity': graycoprops(glcm, 'homogeneity')[0,0],
            'energy': graycoprops(glcm, 'energy')[0,0]
        }

    def analyze_composition(self):
        """Analyze image composition"""
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        return {
            'edge_density': np.mean(edges) / 255,
            'symmetry_score': self._calculate_symmetry(gray)
        }
    
    def _calculate_symmetry(self, gray_image):
        height, width = gray_image.shape
        mid = width // 2
        left = gray_image[:, :mid]
        right = np.fliplr(gray_image[:, mid:mid*2])
        return np.mean(np.abs(left - right)) 