# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from transformers import AutoImageProcessor, AutoModelForImageClassification
# from PIL import Image, UnidentifiedImageError
# import io
# import numpy as np
# from skimage.metrics import structural_similarity as ssim

# # Load pre-trained model and processor
# model_name = "facebook/deit-base-distilled-patch16-224"
# processor = AutoImageProcessor.from_pretrained(model_name)
# model = AutoModelForImageClassification.from_pretrained(model_name)

# # FastAPI app
# app = FastAPI()

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # Frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Store the first uploaded image
# previous_image = None

# def preprocess_image(image):
#     """Converts an image to grayscale and numpy array for comparison."""
#     image = image.convert("L").resize((224, 224))  # Convert to grayscale and resize
#     return np.array(image)

# @app.post("/predict/")
# async def predict(file: UploadFile = File(...)):
#     global previous_image
#     try:
#         print(f"Received file: {file.filename}")

#         if not file.content_type.startswith("image/"):
#             raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

#         try:
#             image = Image.open(io.BytesIO(await file.read()))
#             processed_image = preprocess_image(image)
#         except UnidentifiedImageError:
#             raise HTTPException(status_code=400, detail="Invalid image file.")

#         if previous_image is None:
#             previous_image = processed_image
#             return JSONResponse({"message": "First image uploaded successfully. Upload another image to compare."})

#         # Calculate SSIM (Structural Similarity Index)
#         similarity = ssim(previous_image, processed_image)
#         similarity_percent = round(similarity * 100, 2)

#         # Reset previous image for next comparison
#         previous_image = processed_image

#         return JSONResponse({"similarity": f"{similarity_percent}%", "message": "Image comparison complete."})

#     except HTTPException as e:
#         print(f"HTTP Error: {e.detail}")
#         return JSONResponse({"error": e.detail}, status_code=e.status_code)
#     except Exception as e:
#         print(f"Error during prediction: {e}")
#         return JSONResponse({"error": "An unexpected error occurred."}, status_code=500)


from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image, UnidentifiedImageError
import io
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Load pre-trained model and processor
model_name = "facebook/deit-base-distilled-patch16-224"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust if frontend is hosted elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def preprocess_image(image):
    """Converts an image to grayscale and numpy array for comparison."""
    image = image.convert("L").resize((224, 224))  # Convert to grayscale and resize
    return np.array(image)

@app.post("/predict/")
async def predict(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        print(f"Received files: {file1.filename}, {file2.filename}")

        # Validate file types
        if not (file1.content_type.startswith("image/") and file2.content_type.startswith("image/")):
            raise HTTPException(status_code=400, detail="Both uploaded files must be images.")

        # Read and process images
        try:
            image1 = Image.open(io.BytesIO(await file1.read()))
            image2 = Image.open(io.BytesIO(await file2.read()))
            processed_image1 = preprocess_image(image1)
            processed_image2 = preprocess_image(image2)
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="One or both uploaded files are not valid images.")

        # Calculate SSIM (Structural Similarity Index)
        similarity = ssim(processed_image1, processed_image2)
        similarity_percent = round(similarity * 100, 2)

        return JSONResponse({
            "similarity": f"{similarity_percent}%",
            "message": "Image comparison complete."
        })

    except HTTPException as e:
        print(f"HTTP Error: {e.detail}")
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return JSONResponse({"error": "An unexpected error occurred."}, status_code=500)
