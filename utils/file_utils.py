import os
import datetime

class FileUtils:

    def save_file(self, file):
        time_data = datetime.datetime.now()
        image_name = f'{file.filename[:-4]}_{time_data.strftime("%d-%m-%y_%H:%M:%S")}.jpg'
        file.save(image_name)
        return image_name

    def delete_file(self, file_name):
        os.remove(file_name)

