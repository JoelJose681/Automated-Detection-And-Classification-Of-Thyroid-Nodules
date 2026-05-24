# 🚀 Quick Start Guide

Get the Thyroid Nodule Detection system running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 8GB RAM minimum
- ~2GB free disk space

## Installation (Linux/Mac/Windows)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ThyroidNoduleProject.git
cd ThyroidNoduleProject
```

### 2. Create Virtual Environment
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Application
```bash
python launch.py
```

The application will start at: **http://localhost:5000**

## 🎯 First Steps

### 1. Upload an Image
1. Open http://localhost:5000 in your browser
2. Click "Upload Image"
3. Select an ultrasound image with thyroid nodules
4. Click "Analyze"

### 2. View Results
The system will show:
- **Detection**: Bounding boxes around detected nodules
- **Classification**: Benign/Malignant prediction
- **Confidence**: Prediction confidence score

### 3. Create Account (Optional)
1. Click "Sign Up" in the top-right
2. Enter email, name, and password
3. Log in with your credentials
4. Your analyses will be saved to your history

## 📊 Example Workflows

### Analyze Single Image
```bash
python inference.py path/to/image.jpg
```

### Batch Analysis
```python
from inference import load_model, predict

model, device = load_model()
results = predict(model, device, "path/to/image.jpg")
print(results['classification'])
```

### API Usage
```bash
# Get authentication token
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"password"}' \
  | jq -r '.token')

# Analyze image
curl -X POST http://localhost:5000/api/predict \
  -H "Authorization: Bearer $TOKEN" \
  -F "image=@nodule.jpg" \
  | jq '.'
```

## 🔧 Configuration

### Change Detection Settings
Edit `backend/config.py`:
```python
DETECTION_CONFIDENCE_THRESHOLD = 0.25  # Lower = more detections
DETECTION_IOU_THRESHOLD = 0.45         # Lower = fewer duplicates
```

### Change Classification Threshold
```python
CONFIG['threshold'] = 0.78  # Adjust in inference.py
```

### Use CPU Instead of GPU
```python
DEVICE = 'cpu'  # In config.py or inference.py
```

## 🐛 Common Issues

### Error: "ModuleNotFoundError: No module named 'torch'"
```bash
# Reinstall PyTorch
pip install --upgrade torch torchvision
```

### Error: "CUDA out of memory"
```python
# In config.py, reduce batch size
BATCH_SIZE = 16  # Was 32
```

### Port 5000 Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9  # Linux/Mac

# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

### Model Download Failing
```bash
# Manually download from Hugging Face / Roboflow
# Place in: checkpoints/best_model_balanced.pt
# Then restart: python launch.py
```

## 📚 Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **API Reference**: See [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md)
3. **Train Models**: See [Training Guide](#training-models)
4. **Deploy**: See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

## 🏋️ Training Models

### Prepare Your Dataset
```bash
python backend/prepare_classification_data.py \
  --dataset-path "Thyroid Dataset/" \
  --output-path "dataset/processed/"
```

### Train Classification Model
```bash
python backend/train.py \
  --epochs 50 \
  --batch-size 32 \
  --learning-rate 0.001 \
  --output-model "checkpoints/my_model.pt"
```

### Train Detection Model
```bash
python backend/train_detector.py \
  --dataset-path "thyroid det.v1i.yolov8/" \
  --epochs 100 \
  --device 0
```

## 🚀 Deployment

### Docker (Recommended)
```bash
docker build -t thyroid-detection .
docker run -p 5000:5000 thyroid-detection
```

### Cloud Deployment
- **Heroku**: See deployment guide
- **AWS**: Lambda + API Gateway
- **Google Cloud**: Cloud Run
- **Azure**: App Service

## 📊 Performance Tips

| Optimization | Speed Improvement | Memory Usage |
|--------------|-------------------|--------------|
| GPU (CUDA)   | 5-10x faster      | Similar     |
| Batch size 1 | 1x (baseline)     | 2GB         |
| Batch size 32| 4x slower (but efficient) | 8GB |
| Image resize 256x256 | 2x faster  | 50% less    |
| Model quantization | 3x faster   | 50% less    |

## 📧 Need Help?

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ThyroidNoduleProject/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ThyroidNoduleProject/discussions)

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Application starts without errors
- [ ] Web interface loads at http://localhost:5000
- [ ] Can upload an image
- [ ] Detection and classification work
- [ ] Results display correctly
- [ ] (Optional) Sign up and login work
- [ ] (Optional) Analysis saved to history

## 🎓 Learning Resources

- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [ResNet Paper](https://arxiv.org/abs/1512.03385)
- [Medical Imaging Basics](https://en.wikipedia.org/wiki/Medical_imaging)

---

**Congratulations! You're ready to detect thyroid nodules! 🎉**

For more detailed information, see [README.md](README.md)
