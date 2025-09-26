from diffusers import DiffusionPipeline
import torch
torch.cuda.empty_cache()

def load_model(model_path="dreamlike-art/dreamlike-diffusion-1.0"):
    pipe = DiffusionPipeline.from_pretrained(model_path)

    return pipe
# Makoto Shinkai, Hatsune Miku, Akira anime, Pop art anime style, Shounen manga style, Manga sketch style
def predict(pipe, prompt, default_='', negative_prompt=''):
    default_ = "A close-up portrait,  fictional anime character. No realistic {entry}" 

    negative_prompt = "low quality, blurry, deformed, poorly drawn, out of frame, worst quality, poorly drawn hands, poorly drawn face, extra limbs, extra fingers, text, watermark, complex background, messy, rough texture, 3d, nsfw, distorted perspective"

    max_prompt_length = 40
    with torch.no_grad():
        full_prompt =  default_.format(entry=prompt[:max_prompt_length])
        image = pipe(full_prompt, negative_prompt=negative_prompt,  num_inference_steps=15).images[0]
    return image