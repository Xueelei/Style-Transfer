from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from styletrans.models import Picture
from styletrans.forms import PictureForm
# import generate
import re
import os.path
import os
import torch
from torchvision import transforms
from PIL import Image
from styletrans.transformer_net import *

device = 'cuda' if torch.cuda.is_available() else 'cpu'


def home_action(request):
    
    context = {'form':PictureForm()}
    return render(request, 'styletrans/home.html', context)

class G:
    # store the uploaded picture
    picture = None

def add_picture_action(request):
    global picture
    if request.method == 'POST':
        context = {}
        new_profile = Picture()
        form = PictureForm(request.POST, request.FILES, instance=new_profile)
        # Validates the form.
        if not form.is_valid():
            return render(request, 'styletrans/home.html', context)
        else:
            input_picture = form.cleaned_data['picture']
            if input_picture:
                Pic = Picture(picture = input_picture,
                              content_type = input_picture.content_type)
                Pic.save()

                G.picture = Pic
     
    context['picture'] = Pic
    context['form'] = PictureForm()
    return render(request, 'styletrans/home.html', context)

def select_action(request):
    
    context={}

    if 'style' in request.POST:

        selected_style = request.POST['style']      #return style name (str)
        
        print(G.picture.picture)
        generate(selected_style, G.picture.picture)
        res_path = '../static/res/out.jpg'
        context['result'] = res_path
    return render(request, 'styletrans/show_result.html', context)

def _load_test_img(path):
    img = Image.open(path)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    return transform(img)


def generate(selected_style, img_path):
    # return generated img
    model = TransformerNet().to(device)
    BASE = os.path.dirname(os.path.abspath(__file__))   #styletrans
    style_path = os.path.join(BASE, 'style_transfer_models/'+selected_style+'.pth')
    # print(style_path)
    state_dict = torch.load(style_path)  # -----
    for k in list(state_dict.keys()):
        if re.search(r'in\d+\.running_(mean|var)$', k):
            del state_dict[k]
    # print('load state')
    model.load_state_dict(state_dict)
    model.to(device)
    content_img = _load_test_img(img_path)
    content_img = content_img.unsqueeze(0).to(device)
    model.eval()
    out = model(content_img).detach().cpu()
    data = out[0]
    img = data.clone().clamp(0, 255).numpy()
    img = img.transpose(1, 2, 0).astype('uint8')
    img = Image.fromarray(img)

    save_path = os.path.join(BASE, 'static/res/out.jpg')
    img.save(save_path)
    return None


def get_photo(request, id):
    pic = get_object_or_404(Picture, id=id)
    
    if not pic.picture:
        raise Http404
    
    return HttpResponse(pic.picture, content_type=pic.content_type)
    







