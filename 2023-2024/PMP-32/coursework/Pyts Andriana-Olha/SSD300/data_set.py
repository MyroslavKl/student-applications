import torch
from torch.utils.data import Dataset
import json
import os
from PIL import Image
from utils import transform

# Клас набору даних PyTorch для використання в завантажувачі даних PyTorch для створення пакетів.
class PascalVOCDataset(Dataset):
    def __init__(self, data_folder, split, keep_difficult=False):
        self.split = split.upper()
        assert self.split in {'TRAIN', 'TEST'}
        self.data_folder = data_folder
        self.keep_difficult = keep_difficult

        # Читання файлів даних
        with open(os.path.join(data_folder, self.split + '_images.json'), 'r') as j:
            self.images = json.load(j)
        with open(os.path.join(data_folder, self.split + '_objects.json'), 'r') as j:
            self.objects = json.load(j)
        assert len(self.images) == len(self.objects)

    # Витягує i-й зразок з набору даних.
    def __getitem__(self, i):
        image = Image.open(self.images[i], mode='r')
        image = image.convert('RGB')

        # Прочитайте об’єкти на цьому зображенні
        objects = self.objects[i]
        boxes = torch.FloatTensor(objects['boxes'])  
        labels = torch.LongTensor(objects['labels'])  
        difficulties = torch.ByteTensor(objects['difficulties'])  

        # Відмовтеся від складних предметів, якщо хочете
        if not self.keep_difficult:
            boxes = boxes[1 - difficulties]
            labels = labels[1 - difficulties]
            difficulties = difficulties[1 - difficulties]
        # Застосувати перетворення
        image, boxes, labels, difficulties = transform(image, boxes, labels, difficulties, split=self.split)
        return image, boxes, labels, difficulties
    
    # Отримує i-й семплПовертає кількість семплів у файлі dataset.ple з набору даних.
    def __len__(self):
        return len(self.images)

    # Об'єднує тензори різних розмірів, використовуючи списки.
    def collate_fn(self, batch):
        images = list()
        boxes = list()
        labels = list()
        difficulties = list()

        for b in batch:
            images.append(b[0])
            boxes.append(b[1])
            labels.append(b[2])
            difficulties.append(b[3])

        images = torch.stack(images, dim=0)
        return images, boxes, labels, difficulties  