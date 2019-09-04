import re
import torch
from torchvision import transforms
from PIL import Image


from transformer_net import *

device = 'cuda' if torch.cuda.is_available() else 'cpu'


def load_test_img(path):
    img = Image.open(path)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    return transform(img)


def style_transfer(img_path, style_model):
	content_img = load_test_img(img_path)
	content_img = content_img.unsqueeze(0).to(device)
	style_model.eval()
	with torch.no_grad():
		out = style_model(content_img).detach().cpu()
		data = out[0]
		img = data.clone().clamp(0, 255).numpy()
		img = img.transpose(1, 2, 0).astype('uint8')
		img = Image.fromarray(img)
		# img.save(save_path)
		return img


def generate(selected_style, img):
	model = TransformerNet().to(device)
	style_path = f'../style_transfer_models/{selected_style}.pth'
	state_dict = torch.load(style_path)	#-----
	for k in list(state_dict.keys()):
		if re.search(r'in\d+\.running_(mean|var)$', k):
			del state_dict[k]
	# print('load state')
	model.load_state_dict(state_dict)
	model.to(device)
	out_image = style_transfer(img, model)
	return out_image

if __name__ == "__main__":
	img_path = ''
	style_model = ''
	save_path = ''
    generate(img_path, style_model, save_path)
