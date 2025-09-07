#!/usr/bin/python3
"""
Object Counting AI Pipeline using SAM and Transformers
Based on the AI Engineering Lab requirements
"""
import os
import logging
import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Optional
import time
import torch
import torch.nn.functional as F
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import torchvision.transforms as tf
from transformers import AutoImageProcessor, AutoModelForImageClassification, pipeline
import urllib.request

# Configure logging
logger = logging.getLogger(__name__)

class ObjectCountingPipeline:
    """
    AI pipeline using SAM (Segment Anything Model) and Transformers
    Based on the Jupyter Notebook from the school project
    """
    
    def __init__(self):
        """Initialize the AI pipeline with SAM and Transformers"""
        self.models_loaded = False
        self.sam_model = None
        self.mask_generator = None
        self.classifier = None
        self.image_processor = None
        self.zero_shot_classifier = None
        self.device = None
        self._load_models()
    
    def _load_models(self):
        """Load SAM and Transformers models"""
        try:
            logger.info("Loading AI models (SAM + Transformers)...")
            
            # Set device (CPU as recommended for school project)
            self.device = "cpu"  # Using CPU as specified in requirements
            logger.info(f"Using device: {self.device}")
            
            # Load SAM model
            self._load_sam_model()
            
            # Load image classification model
            self._load_classifier()
            
            # Load zero-shot classification model
            self._load_zero_shot_classifier()
            
            self.models_loaded = True
            logger.info("AI models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load AI models: {e}")
            self.models_loaded = False
    
    def _load_sam_model(self):
        """Load SAM (Segment Anything Model)"""
        try:
            checkpoint_path = "sam_vit_b_01ec64.pth"
            
            # Download SAM checkpoint if not exists
            if not os.path.exists(checkpoint_path):
                logger.info("Downloading SAM checkpoint...")
                url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
                urllib.request.urlretrieve(url, checkpoint_path)
                logger.info("SAM checkpoint downloaded")
            
            # Load SAM model
            self.sam_model = sam_model_registry["vit_b"](checkpoint_path)
            self.sam_model.to(self.device)
            
            # Create mask generator
            self.mask_generator = SamAutomaticMaskGenerator(
                model=self.sam_model,
                points_per_side=16,
                pred_iou_thresh=0.7,
                stability_score_thresh=0.85,
                min_mask_region_area=500,
            )
            
            logger.info("SAM model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load SAM model: {e}")
            raise
    
    def _load_classifier(self):
        """Load image classification model"""
        try:
            # Using a pre-trained model for image classification
            # This can be customized based on your specific object types
            model_name = "microsoft/resnet-50"  # Good general-purpose classifier
            
            self.image_processor = AutoImageProcessor.from_pretrained(model_name)
            self.classifier = AutoModelForImageClassification.from_pretrained(model_name)
            self.classifier.to(self.device)
            
            logger.info("Image classifier loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load classifier: {e}")
            raise
    
    def _load_zero_shot_classifier(self):
        """Load zero-shot classification model for object type mapping"""
        try:
            # Load zero-shot classification pipeline
            # This maps ResNet-50 predictions to our target object types
            self.zero_shot_classifier = pipeline(
                "zero-shot-classification", 
                model="typeform/distilbert-base-uncased-mnli"
            )
            
            logger.info("Zero-shot classifier loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load zero-shot classifier: {e}")
            raise
    
    def process_image(self, image_path: str, object_type: str) -> Dict:
        """
        Process image with AI pipeline to count specific objects
        
        Args:
            image_path: Path to the image file
            object_type: Type of object to count
            
        Returns:
            Dictionary with processing results
        """
        start_time = time.time()
        
        try:
            if not self.models_loaded:
                raise Exception("AI models not loaded")
            
            # Load and preprocess image
            image = self._load_and_preprocess_image(image_path)
            
            # Run SAM segmentation
            masks, panoptic_map = self._generate_segments(image)
            
            # Classify segments and count objects
            detection_result = self._classify_and_count_segments(image, masks, panoptic_map, object_type)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare response
            result = {
                'success': True,
                'predicted_count': detection_result['count'],
                'confidence': detection_result['confidence'],
                'total_segments': detection_result['segments'],
                'processing_time': processing_time,
                'object_type': object_type,
                'image_dimensions': image.size,
                'detected_objects': detection_result.get('detected_objects', [])
            }
            
            logger.info(f"Image processed successfully: {detection_result['count']} {object_type}s detected")
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ Image processing failed: {e}")
            
            return {
                'success': False,
                'error': str(e),
                'processing_time': processing_time
            }
    
    def process_image_auto(self, image_path: str) -> Dict:
        """
        Process image with AI pipeline to automatically detect and count all objects
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with processing results including all detected objects
        """
        start_time = time.time()
        
        try:
            if not self.models_loaded:
                raise Exception("AI models not loaded")
            
            # Load and preprocess image
            image = self._load_and_preprocess_image(image_path)
            
            # Run SAM segmentation
            masks, panoptic_map = self._generate_segments(image)
            
            # Classify all segments to find different object types
            detected_objects = self._classify_all_segments(image, masks, panoptic_map)
            
            # Calculate totals
            total_count = sum(obj['count'] for obj in detected_objects)
            total_segments = len(masks)
            overall_confidence = np.mean([obj['confidence'] for obj in detected_objects]) if detected_objects else 0.0
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare response
            result = {
                'success': True,
                'predicted_count': total_count,
                'confidence': overall_confidence,
                'total_segments': total_segments,
                'processing_time': processing_time,
                'object_type': 'auto-detected',
                'detected_objects': detected_objects,
                'image_dimensions': image.size
            }
            
            logger.info(f"Auto-detection completed: {total_count} total objects detected across {len(detected_objects)} types")
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ Auto-detection failed: {e}")
            
            return {
                'success': False,
                'error': str(e),
                'processing_time': processing_time
            }
    
    def _load_and_preprocess_image(self, image_path: str) -> Image.Image:
        """Load and preprocess image for AI processing"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            logger.info(f"Image loaded: {image.size[0]}x{image.size[1]}")
            return image
            
        except Exception as e:
            raise Exception(f"Failed to load/preprocess image: {e}")
    
    def _generate_segments(self, image: Image.Image) -> Tuple[List[Dict], torch.Tensor]:
        """Generate segments using SAM model and create panoptic map"""
        try:
            logger.info("Generating segments with SAM...")
            
            # Convert PIL image to numpy array
            image_array = np.array(image)
            height, width = image.size[1], image.size[0]
            
            # Generate masks using SAM
            masks = self.mask_generator.generate(image_array)
            
            # Sort masks by area (largest first)
            masks_sorted = sorted(masks, key=lambda x: x['area'], reverse=True)
            
            # Limit to top segments to avoid overwhelming results
            TOP_N = 20
            masks_sorted = masks_sorted[:TOP_N]
            
            # Create panoptic map (following original notebook approach)
            predicted_panoptic_map = np.zeros((height, width), dtype=np.int32)
            for idx, mask_data in enumerate(masks_sorted):
                predicted_panoptic_map[mask_data['segmentation']] = idx + 1
            
            predicted_panoptic_map = torch.from_numpy(predicted_panoptic_map)
            
            logger.info(f"Generated {len(masks_sorted)} segments")
            return masks_sorted, predicted_panoptic_map
            
        except Exception as e:
            raise Exception(f"SAM segmentation failed: {e}")
    
    def _classify_and_count_segments(self, image: Image.Image, masks: List[Dict], panoptic_map: torch.Tensor, target_object_type: str) -> Dict:
        """Classify segments and count objects of specific type"""
        try:
            logger.info(f"Classifying segments for {target_object_type}...")
            
            count = 0
            confidence_scores = []
            detected_objects = []
            
            for label in panoptic_map.unique():
                if label == 0:  # Skip background
                    continue
                    
                # Extract segment from image
                segment = self._extract_segment(image, None, panoptic_map, label.item())
                if segment is None:
                    continue
                
                # Classify the segment
                classification = self._classify_segment(segment)
                
                # Check if this segment matches our target object type
                if self._is_object_type(classification, target_object_type):
                    count += 1
                    confidence_scores.append(classification['confidence'])
                    
                    detected_objects.append({
                        'type': target_object_type,
                        'count': 1,
                        'confidence': classification['confidence'],
                        'segments': 1,
                        'mask_id': label.item(),
                        'original_class': classification.get('original_class', 'unknown')
                    })
            
            # Calculate average confidence
            avg_confidence = np.mean(confidence_scores) if confidence_scores else 0.0
            
            return {
                'count': count,
                'confidence': avg_confidence,
                'segments': len(masks),
                'detected_objects': detected_objects
            }
            
        except Exception as e:
            raise Exception(f"Segment classification failed: {e}")
    
    def _classify_all_segments(self, image: Image.Image, masks: List[Dict], panoptic_map: torch.Tensor) -> List[Dict]:
        """Classify all segments to find different object types"""
        try:
            logger.info("Classifying all segments...")
            
            object_counts = {}
            object_confidences = {}
            
            for label in panoptic_map.unique():
                if label == 0:  # Skip background
                    continue
                    
                # Extract segment from image
                segment = self._extract_segment(image, None, panoptic_map, label.item())
                if segment is None:
                    continue
                
                # Classify the segment
                classification = self._classify_segment(segment)
                
                # Group by object type
                obj_type = classification['label']
                if obj_type not in object_counts:
                    object_counts[obj_type] = 0
                    object_confidences[obj_type] = []
                
                object_counts[obj_type] += 1
                object_confidences[obj_type].append(classification['confidence'])
            
            # Convert to list format
            detected_objects = []
            for obj_type, count in object_counts.items():
                avg_confidence = np.mean(object_confidences[obj_type])
                detected_objects.append({
                    'type': obj_type,
                    'count': count,
                    'confidence': avg_confidence,
                    'segments': count
                })
            
            return detected_objects
            
        except Exception as e:
            raise Exception(f"All segment classification failed: {e}")
    
    def _extract_segment(self, image: Image.Image, mask_data: Dict, panoptic_map: torch.Tensor, label: int) -> torch.Tensor:
        """Extract a segment from the image using the mask (following original notebook approach)"""
        try:
            # Convert PIL image to tensor
            transform = tf.Compose([tf.PILToTensor()])
            img_tensor = transform(image)
            
            # Get bounding box of the mask
            def get_mask_box(tensor: torch.Tensor) -> tuple:
                """Get bounding box of non-zero elements in a tensor"""
                non_zero_indices = torch.nonzero(tensor, as_tuple=True)[0]
                if non_zero_indices.shape[0] == 0:
                    return None, None
                first_n = non_zero_indices[:1].item()
                last_n = non_zero_indices[-1:].item()
                return first_n, last_n
            
            # Get bounding box coordinates
            y_start, y_end = get_mask_box(panoptic_map == label)
            x_start, x_end = get_mask_box((panoptic_map == label).T)
            
            if y_start is None or x_start is None:
                return None
            
            # Crop the image and mask
            cropped_tensor = img_tensor[:, y_start:y_end+1, x_start:x_end+1]
            cropped_mask = panoptic_map[y_start:y_end+1, x_start:x_end+1] == label
            
            # Apply mask to segment
            segment = cropped_tensor * cropped_mask.unsqueeze(0)
            segment[:, ~cropped_mask] = 188  # Set background to gray
            
            return segment
            
        except Exception as e:
            raise Exception(f"Segment extraction failed: {e}")
    
    def _classify_segment(self, segment: torch.Tensor) -> Dict:
        """Classify a segment using the complete three-step pipeline"""
        try:
            # Step 1: ResNet-50 classification
            inputs = self.image_processor(images=segment, return_tensors="pt")
            outputs = self.classifier(**inputs)
            logits = outputs.logits
            predicted_class_idx = logits.argmax(-1).item()
            predicted_class = self.classifier.config.id2label[predicted_class_idx]
            
            # Step 2: Zero-shot classification to map to our target object types
            candidate_labels = [
                "car", "cat", "tree", "dog", "building", "person", 
                "sky", "ground", "hardware", "vehicle", "animal", "plant"
            ]
            
            result = self.zero_shot_classifier(predicted_class, candidate_labels=candidate_labels)
            final_label = result['labels'][0]
            confidence = result['scores'][0]
            
            return {
                'label': final_label,
                'confidence': confidence,
                'class_id': predicted_class_idx,
                'original_class': predicted_class
            }
            
        except Exception as e:
            raise Exception(f"Segment classification failed: {e}")
    
    def _is_object_type(self, classification: Dict, target_type: str) -> bool:
        """Check if a classification matches the target object type"""
        try:
            # Simple string matching - can be enhanced with more sophisticated logic
            target_lower = target_type.lower()
            label_lower = classification['label'].lower()
            
            # Check for exact match or partial match
            if target_lower in label_lower or label_lower in target_lower:
                return True
            
            # Add some common synonyms
            synonyms = {
                'car': ['vehicle', 'automobile', 'car'],
                'person': ['person', 'human', 'people', 'man', 'woman'],
                'cat': ['cat', 'feline', 'kitten'],
                'dog': ['dog', 'canine', 'puppy'],
                'tree': ['tree', 'plant', 'vegetation'],
                'building': ['building', 'house', 'structure', 'architecture']
            }
            
            if target_lower in synonyms:
                return any(syn in label_lower for syn in synonyms[target_lower])
            
            return False
            
        except Exception as e:
            logger.warning(f"Object type matching failed: {e}")
            return False
    
    def get_model_status(self) -> Dict:
        """Get status of all AI models"""
        return {
            'models_loaded': self.models_loaded,
            'device': self.device,
            'sam_loaded': self.sam_model is not None,
            'classifier_loaded': self.classifier is not None,
            'zero_shot_loaded': self.zero_shot_classifier is not None,
            'total_models': 3  # SAM + ResNet-50 + Zero-shot Classifier
        }
    
    def reload_models(self) -> bool:
        """Reload all AI models"""
        try:
            logger.info("Reloading AI models...")
            self._load_models()
            return self.models_loaded
        except Exception as e:
            logger.error(f"Failed to reload models: {e}")
            return False

# Create global instance
pipeline = ObjectCountingPipeline()
