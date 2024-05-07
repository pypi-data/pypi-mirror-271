from diffusers import StableDiffusionPipeline, UniPCMultistepScheduler,DPMSolverMultistepScheduler,DDPMScheduler,DDIMScheduler
from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import retrieve_timesteps, rescale_noise_cfg
from accelerate import Accelerator
from .static_globals import *
import torch
import random
import string
import nltk
import os
nltk.download('words')
from nltk.corpus import words
from training_loops import loop_vanilla,loop_general
from inference import call_vanilla_with_dict
import random
import ImageReward as image_reward
import string
def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
reward_cache="/scratch/jlb638/reward_symbolic/"+generate_random_string(10)
from transformers import CLIPProcessor, CLIPModel,ViTImageProcessor, ViTModel
import numpy as np
from numpy.linalg import norm
import gc
from aesthetic_reward import get_aesthetic_scorer
from custom_pipelines import T5UnetPipeline,T5TransformerPipeline,LlamaUnetPipeline
from transformers import Blip2Processor, Blip2ForConditionalGeneration,pipeline,Blip2Model
from PIL import Image
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim as cos_sim_st

def cos_sim(vector_i,vector_j)->float:
    return np.dot(vector_i,vector_j)/(norm(vector_i)*norm(vector_j))

def get_caption(image:Image,blip_processor: Blip2Processor,blip_conditional_gen: Blip2ForConditionalGeneration):
    caption_inputs = blip_processor(image, "", return_tensors="pt")
    for name in ["pixel_values","input_ids"]:
        caption_inputs[name]=caption_inputs[name].to(blip_conditional_gen.device)
    caption_out=blip_conditional_gen.generate(**caption_inputs)
    return blip_processor.decode(caption_out[0],skip_special_tokens=True).strip()

def get_metric_dict(evaluation_prompt_list:list, evaluation_image_list:list,image_list:list,accelerator:Accelerator=None):
    metric_dict={}
    
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    if accelerator is not None:
        clip_model.to(accelerator.device)
        clip_model=accelerator.prepare(clip_model)
    
    clip_inputs=clip_processor(text=evaluation_prompt_list, images=evaluation_image_list+image_list, return_tensors="pt", padding=True)
    clip_inputs["input_ids"]=clip_inputs["input_ids"].to(clip_model.device)
    clip_inputs["pixel_values"]=clip_inputs["pixel_values"].to(clip_model.device)

    clip_outputs = clip_model(**clip_inputs)
    src_image_n=len(image_list)
    text_embed_list=clip_outputs.text_embeds.cpu().detach().numpy()
    image_embed_list=clip_outputs.image_embeds.detach().cpu().numpy()[:-src_image_n]
    src_image_embed_list=clip_outputs.image_embeds.detach().cpu().numpy()[-src_image_n:]
    ir_model=image_reward.load("/scratch/jlb638/reward-blob",med_config="/scratch/jlb638/ImageReward/med_config.json")

    identity_consistency_list=[]
    target_similarity_list=[]
    prompt_similarity_list=[]
    for i in range(len(image_embed_list)):
        image_embed=image_embed_list[i]
        text_embed=text_embed_list[i]
        for src_image_embed in src_image_embed_list:
            target_similarity_list.append(cos_sim(image_embed,src_image_embed))
        prompt_similarity_list.append(cos_sim(image_embed, text_embed))
        for j in range(i+1, len(image_embed_list)):
            #print(i,j)
            vector_j=image_embed_list[j]
            sim=cos_sim(image_embed,vector_j)
            identity_consistency_list.append(sim)

    metric_dict[IDENTITY_CONSISTENCY]=np.mean(identity_consistency_list)
    metric_dict[TARGET_SIMILARITY]=np.mean(target_similarity_list)
    metric_dict[PROMPT_SIMILARITY]=np.mean(prompt_similarity_list)

    blip_processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    blip_conditional_gen = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
    if accelerator is not None:
        blip_conditional_gen.to(accelerator.device)
        blip_conditional_gen=accelerator.prepare(blip_conditional_gen)
    

    src_blip_caption_list=[get_caption(src_image,blip_processor,blip_conditional_gen) for src_image in image_list]
    image_blip_caption_list=[get_caption(image,blip_processor,blip_conditional_gen) for image in evaluation_image_list]
    embedding_model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)
    src_blip_embedding_list=embedding_model.encode(src_blip_caption_list)
    image_blip_embedding_list=embedding_model.encode(image_blip_caption_list)
    evaluation_blip_embedding_list=embedding_model.encode(evaluation_prompt_list)

    metric_dict[BLIP_TARGET_CAPTION_SIMILARITY]=np.mean(cos_sim_st(src_blip_embedding_list, image_blip_embedding_list).cpu().detach().numpy())
    metric_dict[BLIP_PROMPT_CAPTION_SIMILARITY]=np.mean(
        [cos_sim_st(evaluation_blip_embedding, image_blip_embedding).cpu().detach().numpy() for evaluation_blip_embedding, image_blip_embedding in zip(evaluation_blip_embedding_list, image_blip_embedding_list)]
    )

    '''blip_model=Blip2Model.from_pretrained("Salesforce/blip2-opt-2.7b")
    blip_inputs=blip_processor(text=evaluation_prompt_list, images=evaluation_image_list+image_list)
    blip_outputs=blip_model(**blip_inputs)'''




    metric_dict[IMAGE_REWARD]=np.mean(
        [ir_model.score(evaluation_prompt,evaluation_image) for evaluation_prompt,evaluation_image in zip(evaluation_prompt_list, evaluation_image_list) ]
    )
    aesthetic_scorer=get_aesthetic_scorer()
    metric_dict[AESTHETIC_SCORE]=np.mean(
        [aesthetic_scorer(evaluation_image).cpu().numpy()[0] for evaluation_image in evaluation_image_list]
    )
    for metric in METRIC_LIST:
        if metric not in metric_dict:
            metric_dict[metric]=0.0
    return metric_dict