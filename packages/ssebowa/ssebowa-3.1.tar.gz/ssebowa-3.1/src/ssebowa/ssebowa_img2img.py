import base64
import requests


class ssebowa_img2img:

    def generate_image(self,image_path, prompt):
        url = 'https://api5.ssebowa.chat/ssebowavlm'
        
        # Create the payload with the prompt and image
        payload = {
            'prompt': prompt,
        }
        files = {
            'image': (image_path, open(image_path, 'rb'))
        }
        print("Please wait a minute, your image is generating")
        # Send the POST request
        response = requests.post(url, data=payload, files=files)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the response JSON
            return response.json()
        else:
            return "There is issue with your image or prompt"