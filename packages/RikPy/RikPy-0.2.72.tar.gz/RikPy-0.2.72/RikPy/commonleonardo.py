import requests
import os
import time
from dotenv import load_dotenv
from RikPy.commonfunctions import rfplogger

model_id_default = "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3" #Default model
model_id_anime = "1aa0f478-51be-4efd-94e8-76bfc8f533af" #Anime pastel dream (Marie Angel default). Pastel anime styling. Use with PMv3 and the anime preset for incredible range. 
model_id_AlbedoBase_XL = "2590401b-a844-4b79-b0fa-8c44bb54eda0" #A great generalist model that tends towards more CG artistic outputs. By alebdobond
model_id_Leonardo_Vision_XL ="5c232a9e-9061-4777-980a-ddc8e65647c6" #A versatile model that excels at realism and photography. Better results with longer prompts.
model_id_Leonardo_Diffusion_XL= "1e60896f-3c26-4296-8ecc-53e2afecc132" #The next phase of the core Leonardo model. Stunning outputs, even with short prompts.
model_id_DreamShaper_v5 = "d2fb9cf9-7999-4ae5-8bfe-f0df2d32abf8" #A versatile model great at both photorealism and anime, includes noise offset training, 
model_id_Marie = "4602459c-315a-4044-9d84-99fe7898fb0f"

load_dotenv()  # This loads the environment variables from .env
leonardo_key = os.getenv("LEONARDO_KEY")
negative_prompt = "long neck, deformed, long cloth, long dress, dark skin, ugly hands, bad hands"
    
def check_generation_status(generation_id):
     # API reference: https://docs.leonardo.ai/reference/getgeneration
    url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {leonardo_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if 'generations_by_pk' in response_data and 'status' in response_data['generations_by_pk']:
            generation_status = response_data['generations_by_pk']['status']
            return generation_status
        else:
            print("Status field not found in response.")
            return None
    else:
        print(f"Failed to get generation status. Status code: {response.status_code}")
        return None

# Image Retrieval
def Leonardo_retrieve_image(generation_id):
    if generation_id is None:
        print("No generation ID provided.")
        return

    url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {leonardo_key}"
    }

    response = requests.get(url, headers=headers)
    rfplogger(response)
    
    if response.status_code == 200:
        print("Image retrieval successful.")
        # Extract the array of image URLs and metadata
        image_array = response.json()
        image_urls=[]
        for image in image_array['generations_by_pk']['generated_images']:
            image_urls.append(image['url'])
        # generated_images_url = image_array['generations_by_pk']['generated_images']
        rfplogger(response.json())
        return image_urls  # Returns the full image array from the response
    else:
        print(f"Image retrieval failed. Status code: {response.status_code}")
        print("Response:", response.text)
        return []
    
def Leonardo_list_all_models():
 
    url = "https://cloud.leonardo.ai/api/rest/v1/platformModels"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {leonardo_key}"
    }
    response = requests.get(url, headers=headers)
    print(response.text)

# Image Generation
def Leonardo_generate_image(model_id, prompt, height, width, payload="", number_images=1):
    # API reference https://docs.leonardo.ai/reference/creategeneration
    # models https://docs.leonardo.ai/docs/elements-and-model-compatibility
    
    engine_model_id=model_id_default
    if model_id=="model_id_anime": engine_model_id=model_id_anime
    if model_id=="model_id_AlbedoBase_XL": engine_model_id=model_id_AlbedoBase_XL
    if model_id=="model_id_Leonardo_Vision_XL": engine_model_id=model_id_Leonardo_Vision_XL
    if model_id=="model_id_Leonardo_Diffusion_XL": engine_model_id=model_id_Leonardo_Diffusion_XL
    if model_id=="model_id_DreamShaper_v5": engine_model_id=model_id_DreamShaper_v5
    if model_id=="model_id_Marie": engine_model_id=model_id_Marie

    url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    if payload=="":
        payload = {
            "height": height,
            "width": width,
            "modelId": f"{engine_model_id}",
            "prompt": f"{prompt}",
            #"negative_prompt": "",
            "num_images": number_images,
            "alchemy": False,
            "contrastRatio": 1,
            "guidance_scale": 7,
            "photoReal": False,
            #"photoRealStrength": 0.5,
            "presetStyle": "LEONARDO",
            "promptMagic": True,
            "promptMagicStrength": 0.4,
            "promptMagicVersion": "v2",
            "public": False
        }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {leonardo_key}"
    }

    # response = requests.post(url, json=payload, headers=headers)
    
    # time.sleep(30)  # Wait for the image to be generated
    #################################################################3
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Image generation initiated.")
        response_data = response.json()
        generation_id = response_data.get('sdGenerationJob', {}).get('generationId')  # Adjust this according to the actual response structure
        if generation_id is None:
            print("Generation ID not found in response.")
            return None
        # Check the status of the generation job periodically until it's completed
        while True:
            status = check_generation_status(generation_id)
            if status == 'COMPLETE':
                print("Image generation completed.")
                break
            elif status == 'PENDING':
                print("Waiting for image generation to complete...")
                time.sleep(5)
            else: 
                print("Image generation failed.")
                return None
        return generation_id
    else:
        print(f"Image generation failed. Status code: {response.status_code}")
        rfplogger(response.text)
        print("Response:", response.text)
        return None