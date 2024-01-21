from json.tool import main
from unittest import result
from PIL import Image
import torch
from torchvision import transforms


def model_identify(model_path, img_path):
    model = torch.load(model_path)
    img = Image.open(img_path)
    min_pixel = min(img.size)
    transform = transforms.Compose([transforms.CenterCrop(min_pixel),
                                    transforms.Resize((224, 224)),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.485, 0.456, 0.406], [
                                                         0.229, 0.224, 0.225])
                                    ])
    img = transform(img)
    img = img.unsqueeze(0)
    with torch.no_grad():
        device = torch.device("cuda:2" if torch.cuda.is_available() else "cpu")
        model.to(device).eval()
        img = img.to(device)
        pre = model(img)
        predicted_disease_index = torch.argmax(pre).tolist()

    return predicted_disease_index


def front_model_identify(img_path):
    index_diseases_dict = {
        0: "anthracnose",
        1: "leaf_blight",
        2: "health_f",
        3: "leaf_blight",
        4: "angular_leaf_spot",
        5: "lepidoptera_larvae",
        6: "tetranychus"
    }

    model_path = "./functions/model_path/Strawberry_model_front_side.pth"
    return index_diseases_dict[model_identify(model_path, img_path)]


def back_model_identify(img_path):
    index_diseases_dict = {
        0: "health_r",
        1: "leaf_blight",
        2: "angular_leaf_spot"
    }
    model_path = "./functions/model_path/Strawberry_model_back_side.pth"

    return index_diseases_dict[model_identify(model_path, img_path)]


if __name__ == '__main__':
    img_path = '2022_Strawberry_LINEBot/static/chatbot_default_images/health_r.jpg'
    result = back_model_identify(img_path)
    print(result)
    print(type(result))
